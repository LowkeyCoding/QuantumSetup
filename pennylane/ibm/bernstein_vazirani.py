import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt
from functools import partial

import os
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator
from dotenv import load_dotenv

load_dotenv()
provider = QiskitRuntimeService(token=os.environ["ibm_token"], channel="ibm_cloud", instance=os.environ["ibm_crn"])
real_backend = provider.least_busy(operational=True, simulator=False)
backend = AerSimulator.from_backend(real_backend)

# Hidden Integer
num = 42 
NUM_QUBITS = int(np.ceil(np.log2(num)))

dev = qml.device("qiskit.remote", wires=NUM_QUBITS, backend=backend)


@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit(num):
    for i in range(NUM_QUBITS):
        qml.Hadamard(i)

    for i in range(NUM_QUBITS):
        if num & (1 << i):
            qml.Z(i)

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