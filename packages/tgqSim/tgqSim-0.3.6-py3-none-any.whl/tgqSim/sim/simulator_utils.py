import numpy as np
import build.tgqSim.utils.dev_tools as dev_tools
import os
import ctypes


def free_state(state):
    lib = get_cuda_lib()
    lib.freeAllMem.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.complex128)
    ]
    lib.freeAllMem.restype = None
    lib.freeAllMem(state)


def get_cuda_lib():
    cuda_version = dev_tools.get_cuda_version().replace(".", "-")
    lib_name = f"cuda_{cuda_version}_tgq_simulator.so"
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    dll_path = os.path.abspath(current_directory + '/lib/' + lib_name)
    lib = ctypes.CDLL(dll_path)
    return lib
