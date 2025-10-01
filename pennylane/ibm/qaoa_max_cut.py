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

graph = [(0, 1), (0, 3), (1, 2), (2, 3)]
NUM_QUBITS = max(list(map(max, zip(*graph)))) + 1
dev = qml.device("qiskit.aer", wires=NUM_QUBITS, backend=backend)

def U_B(beta):
    for qubit in range(NUM_QUBITS):
        qml.RX(2*beta, qubit)

def U_G(gamma):
    for edge in graph: 
        qml.CNOT(edge)
        qml.RZ(gamma, wires=edge[1])
        qml.CNOT(edge)

def bitstring_to_int(bit_string_sample):
    return int(2 ** np.arange(len(bit_string_sample)) @ bit_string_sample[::-1])

@qml.qnode(dev)
def circuit(gammas, betas, return_samples=False):
    for qubit in range(NUM_QUBITS):
        qml.Hadamard(qubit)
    
    for gamma, beta in zip(gammas, betas):
        U_G(gamma)
        U_B(beta)
    
    if return_samples:
        return qml.sample()
    
    C = qml.sum(*(qml.Z(w1) @ qml.Z(w2) for w1, w2 in graph))
    return qml.expval(C)

def objective(params):
    # Minimize the negative of the objective function C
    return -0.5 * (len(graph) - circuit(*params))


def qaoa_maxcut(n_layers=1):
    print(f"\np={n_layers:d}")

    # Initialize the parameters near zero
    init_params = 0.01 * np.random.rand(2, n_layers, requires_grad=True)

    # Initialize classical optimizer (Adaptive gradient descent)
    optimizer = qml.AdagradOptimizer(stepsize=0.5)

    # Optimize Gammas and Beta values
    params = init_params.copy()
    steps = 30
    for i in range(steps):
        params = optimizer.step(objective, params)
        if (i + 1) % 5 == 0:
            print(f"Objective after step {i+1:3d}: {-objective(params): .7f}")

    # Sample 100 bitstrings
    bitstrings = circuit(*params, return_samples=True,shots=100)
    # Convert the samples bitstrings to integers
    sampled_ints = [bitstring_to_int(string) for string in bitstrings]

    # Optimized Gamma and Beta vectors and predicted solution
    counts = np.bincount(np.array(sampled_ints))
    most_freq_bit_string = np.argmax(counts)
    print(f"Optimized parameter vectors:\ngamma: {params[0]}\nbeta:  {params[1]}")
    print(f"Most frequently sampled bit string is: {most_freq_bit_string:04b}")

    return -objective(params), sampled_ints

int_samples1 = qaoa_maxcut(n_layers=1)[1]
int_samples2 = qaoa_maxcut(n_layers=2)[1]

xticks = range(0, 16)
xtick_labels = list(map(lambda x: format(x, "04b"), xticks))
bins = np.arange(0, 17) - 0.5

fig, _ = plt.subplots(1, 2, figsize=(8, 4))
for i, samples in enumerate([int_samples1, int_samples2], start=1):
    plt.subplot(1, 2, i)
    plt.title(f"n_layers={i}")
    plt.xlabel("bitstrings")
    plt.ylabel("Counts")
    plt.xticks(xticks, xtick_labels, rotation="vertical")
    plt.hist(samples, bins=bins)
plt.tight_layout()
plt.show()