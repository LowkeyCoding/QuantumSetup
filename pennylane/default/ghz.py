import pennylane as qml
import matplotlib.pyplot as plt
import numpy as np
from functools import partial

NUM_QUBITS = 3 
dev = qml.device("default.qubit", wires=NUM_QUBITS)

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    return qml.counts()

qml.draw_mpl(circuit)()
result = circuit()

names = list(result.keys())
values = list(result.values())

fig, ax = plt.subplots()    
ax.bar(names, values)

plt.show()