import pennylane as qml
import matplotlib.pyplot as plt
from functools import partial

NUM_QUBITS = 3
dev = qml.device("default.qubit", wires=NUM_QUBITS)

wires = list(range(NUM_QUBITS))

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit():
    for wire in wires:
        qml.Hadamard(wire)
    return qml.sample()

def to_mpl(samples):
    mpl_bins =  []
    for sample in samples:
        s_v = ""
        for v in sample:
            s_v += str(v)
        mpl_bins.append(s_v)
    return mpl_bins

qml.draw_mpl(circuit)()
result = circuit()

names = list(result.keys())
values = list(result.values())

plt.bar(names, values)