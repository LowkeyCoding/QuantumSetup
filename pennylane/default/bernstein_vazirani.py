import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt
from functools import partial

# Hidden Integer
num = 42 
NUM_QUBITS = int(np.ceil(np.log2(num)))

dev = qml.device("default.qubit", wires=NUM_QUBITS)


@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit(num):
    for i in range(NUM_QUBITS):
        qml.Hadamard(i)
    qml.Barrier()
    for i in range(NUM_QUBITS):
        if num & (1 << i):
            qml.Z(i)
    qml.Barrier()
    for i in range(NUM_QUBITS):
        qml.Hadamard(i)
    return qml.counts()

qml.draw_mpl(circuit)(num)
result = circuit(num)

names = list(result.keys())
values = list(result.values())
fig, ax = plt.subplots()    
ax.bar(names, values)

plt.show()