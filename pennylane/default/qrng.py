import pennylane as qml
import matplotlib.pyplot as plt
from functools import partial

NUM_QUBITS = 3
dev = qml.device("default.qubit", wires=NUM_QUBITS)

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit():
    for qubit in range(NUM_QUBITS):
        qml.Hadamard(qubit)
    return qml.counts()

qml.draw_mpl(circuit)()
result = circuit()

names = list(result.keys())
values = list(result.values())

fig, ax = plt.subplots()    
ax.bar(names, values)

plt.show()