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

NUM_QUBITS = 3
dev = qml.device("qiskit.remote", wires=NUM_QUBITS, backend=backend)

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit():
    for wire in range(NUM_QUBITS):
        qml.Hadamard(wire)
    return qml.counts()

qml.draw_mpl(circuit)()
result = circuit()

names = list(result.keys())
values = list(result.values())

fig, ax = plt.subplots() 
ax.bar(names, values)

plt.show()