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

# Desired states set to all zeros and all ones
omega = np.array([np.zeros(NUM_QUBITS), np.ones(NUM_QUBITS)])
M = len(omega)
N = 2**NUM_QUBITS
wires = list(range(NUM_QUBITS))
dev = qml.device("qiskit.remote", wires=NUM_QUBITS, backend=backend)


def equal_superposition(wires):
    for wire in wires:
        qml.Hadamard(wires=wire)


def oracle(wires, omega):
    qml.FlipSign(omega, wires=wires)

# Optimal number of iterations given a noise free environment
# iterations = int(np.round(np.sqrt(N / M) * np.pi / 4))
iterations = 1
@qml.qnode(dev)
def circuit():
    # Initial state preparation
    equal_superposition(wires)

    # Grover's iterator
    for i in range(iterations):

        for omg in omega:
            oracle(wires, omg)        
        qml.templates.GroverOperator(wires)

    return qml.probs(wires=wires)

results = circuit()

bit_strings = [f"{x:0{NUM_QUBITS}b}" for x in range(len(results))]

plt.bar(bit_strings, results, color = "#70CEFF")

plt.xticks(rotation="vertical")
plt.xlabel("State label")
plt.ylabel("Probability")
plt.title("States probabilities")

plt.show()