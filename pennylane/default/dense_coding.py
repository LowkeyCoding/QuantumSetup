import pennylane as qml
import matplotlib.pyplot as plt
from functools import partial

NUM_QUBITS = 2
dev = qml.device("default.qubit", wires=NUM_QUBITS)
msg = [0,1]

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit(msg):
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    if msg[0]:
        qml.X(0)
    if msg[1]:
        qml.Z(0)
    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=0)
    return qml.counts(all_outcomes=True)

qml.draw_mpl(circuit)(msg)
result = circuit(msg)

names = list(result.keys())
values = list(result.values())
fig, ax = plt.subplots()    
ax.bar(names, values)

plt.show()