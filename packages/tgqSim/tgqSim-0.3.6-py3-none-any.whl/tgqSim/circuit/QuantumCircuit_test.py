from build.tgqSim.circuit.QuantumCircuit import QuantumCircuit
import numpy as np


if __name__ == '__main__':
    nQubits = 2
    qc = QuantumCircuit(0)
    qc.add_qubits(nQubits, name='qft')
    for i in range(nQubits):
        if nQubits - 2 == i:
            qc.x(i)
        else:
            qc.h(i)
    for i in range(nQubits - 1, -1, -1):
        for j in range(i, -1, -1):
            if j == i:
                qc.h(j)
            else:
                qc.cp(control_qubit=j, target_qubit=i, theta=np.pi / (2 ** (i - j)))
    qc.x(0)
    for i in range(0, nQubits // 2):
        qc.swap(qubit_1=i, qubit_2=nQubits - 1 - i)
    qc.run_statevector()
    print(qc.state)
    print(len(qc.state))
    measure_pos = sorted([1, 0], reverse=True)
    print(qc.measure(measure_bits_list=measure_pos))
    # qc.show_quantum_circuit()