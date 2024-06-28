"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/6/28 14:43
@Function: noise_model.py
@Contact: cuijinghao@tgqs.net
"""

from build.tgqSim.QuantumCircuit import QuantumCircuit
import build.tgqSim.utils.dev_tools as dev_tools
from build.tgqSim.GateSimulation import SingleGate, DoubleGate, TripleGate
# import simulator_utils
import os
from typing import Union
import GPUtil
import ctypes
import numpy as np


class Float2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]


class Double2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double)]


class GateInfo(ctypes.Structure):
    _fields_ = [
        ("gateName", ctypes.c_char_p),
        ("actionPos", ctypes.POINTER(ctypes.c_int)),
        ("theta", ctypes.c_double)
    ]


class SimulationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class QuantumSimulator:
    def setdevice(self, deviceList: Union[int, list]):
        gpus = GPUtil.getGPUs()
        gpuidList = [gpu.id for gpu in gpus]
        if isinstance(deviceList, int):
            deviceList = [deviceList]
        for deviceid in deviceList:
            if deviceid not in gpuidList:
                raise ValueError("设置设备ID不存在")
        self.isgpu = True
        self.deviceid = deviceList

    def _run_with_device(self):
        lib = QuantumSimulator.get_cuda_lib()
        lib.execute_circuit.argtypes = [
            ctypes.POINTER(ctypes.POINTER(Double2)),
            ctypes.POINTER(GateInfo),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]
        lib.execute_circuit.restype = None
        gateInfo = []
        for (gate_pos, gate_info) in self.gate_list:
            if isinstance(gate_pos, int):
                length = 2
                gate_pos = [gate_pos]
            elif isinstance(gate_pos, list):
                length = len(gate_pos) + 1
            else:
                raise TypeError("Type of gate_pos must be int or list")
            gate_obj = GateInfo()
            actionPos = gate_pos + [-1]
            gate_obj.actionPos = (ctypes.c_int * length)(*actionPos)
            if len(gate_info) > 0:
                gate_obj.gateName = gate_info[0].encode(encoding='utf-8')
            if len(gate_info) > 1:
                gate_obj.theta = gate_info[1]
            gateInfo.append(gate_obj)
        gateInfoCData = (GateInfo * len(gateInfo))(*gateInfo)
        deviceIdCData = (ctypes.c_int * len(self.deviceid))(*self.deviceid)
        # 申请内存首地址，不在Python端申请内存
        # 在C语言中申请统一内存，减少多次拷贝动作
        self.state = ctypes.POINTER(Double2)()
        lib.execute_circuit(ctypes.byref(self.state), gateInfoCData, len(gateInfo), self.width, deviceIdCData)
        # iStart = datetime.datetime.now()
        # print(f"start time is {iStart}")
        self.state = np.ctypeslib.as_array(self.state, shape=(2 ** self.width,))
        self.state = self.state.view(np.complex128)
        # print(f"total time of changing type is {(datetime.datetime.now() - iStart).total_seconds()} secs")

    def run_with_noise(self, shots:int=1000):
        noise_type = ["bit_flip", "asymmetric_depolarization", "depolarize", "phase_flip", "phase_damp", "amplitude_damp"]
        result_dict = {}
        tmp_circuit = self.gate_list
        for _ in range(shots):
            new_circuit = []
            for (gate_pos, gate_info) in self.noise_circuit:
                if gate_info[0] in noise_type:
                    noise_gate = QuantumCircuit.parse_noise(noise_type=gate_info[0], gate_pos=gate_pos, error_rate=gate_info[1])
                    # print(noise_gate)
                    if noise_gate is not None:
                        new_circuit.append(noise_gate)
                else:
                    new_circuit.append((gate_pos, gate_info))
            # print("new_circuit:", new_circuit)
            self.gate_list = new_circuit
            result = self.measure(measure_bits_list=[i for i in range(self.width)], shots=1000)

            # print(self.state)
            for key in result.keys():
                if key in result_dict:
                    result_dict[key] += result[key]
                else:
                    result_dict[key] = result[key]
        self.gate_list = tmp_circuit
        self.prob_result = dev_tools.get_normalization(frequency=result_dict)

    def run_statevector(self):
        """
        根据线路的门序列计算末态的量子态
        :return:
        """
        if not self.isgpu:
            self.state = [1 if a == 0 else 0 for a in range(2**self.width)]
            for (gate_pos, gate_info) in self.gate_list:
                gate_type = gate_info[0]
                angle = tuple(gate_info[1:])
                if gate_type in self.base_single_gate:
                    self.state = SingleGate.ActOn_State(self.state, self.width, gate_type, gate_pos, *angle)

                elif gate_type in self.base_double_gate:
                    set_gate_pos = set(gate_pos)
                    if len(set_gate_pos) != len(gate_pos):
                        raise SimulationError(f"Gate position cannot be the same: {gate_pos[0]}, {gate_pos[1]}")
                    self.state = DoubleGate.ActOn_State(self.state, self.width, gate_type, gate_pos, *angle)
                elif gate_type in self.base_triple_gate:
                    set_gate_pos = set(gate_pos)
                    if len(set_gate_pos) != len(gate_pos):
                        raise SimulationError(f"Gate position cannot be the same: "
                                            f"{gate_pos[0]}, {gate_pos[1]} and {gate_pos[2]}")
                    self.state = TripleGate.ActOn_State(self.state, self.width, gate_type, gate_pos, *angle)
                else:
                    raise SimulationError(f"Unkown gate type: {gate_type}")
        else:
            self._run_with_device()



