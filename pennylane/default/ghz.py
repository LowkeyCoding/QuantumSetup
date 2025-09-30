import pennylane as qml
import matplotlib.pyplot as plt
from functools import partial

dev = qml.device("default.qubit", wires=3)

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    return qml.sample()

qml.draw_mpl(circuit)()
result = circuit()

names = list(result.keys())
values = list(result.values())

plt.bar(names, values)

plt.show()