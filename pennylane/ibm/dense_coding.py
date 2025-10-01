import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from dotenv import load_dotenv
import os
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator
load_dotenv()
provider = QiskitRuntimeService(token=os.environ["ibm_token"], channel="ibm_cloud", instance=os.environ["ibm_crn"])
real_backend = provider.least_busy(operational=True, simulator=False)
backend = AerSimulator.from_backend(real_backend)

NUM_QUBITS = 2
dev = qml.device("qiskit.remote", wires=NUM_QUBITS, backend=backend)
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