import matplotlib.pyplot as plt
import pennylane as qml
import numpy as np
import os

NUM_QUBITS = 5

def equal_superposition(wires):
    for wire in wires:
        qml.Hadamard(wires=wire)


def oracle(wires, omega):
    qml.FlipSign(omega, wires=wires)

# Desired states set to all zeros and all ones
omega = np.array([np.zeros(NUM_QUBITS), np.ones(NUM_QUBITS)])
M = len(omega)
N = 2**NUM_QUBITS
wires = list(range(NUM_QUBITS))
dev = qml.device("default.qubit", wires=NUM_QUBITS)

iterations = int(np.round(np.sqrt(N / M) * np.pi / 4))
@qml.qnode(dev)
def circuit():
    # Initial state preparation
    equal_superposition(wires)

    # Grover's iterator
    for i in range(iterations):
        qml.Snapshot(f"B{i}")

        for omg in omega:
            oracle(wires, omg)        
        qml.Snapshot(f"A{i}")
        qml.templates.GroverOperator(wires)
        qml.Snapshot(f"G{i}")

    return qml.probs(wires=wires)

results = qml.snapshots(circuit)()

for k, result in results.items():
    print(f"{k}: {result}")

for i in range(iterations):
    y1 = np.real(results[f"B{i}"])
    y2 = np.real(results[f"A{i}"])
    y3 = np.real(results[f"G{i}"])
    bit_strings = [f"{x:0{NUM_QUBITS}b}" for x in range(len(y1))]

    bar_width = 1

    rect_1 = np.arange(0, len(y1))
    rect_2 = [x + bar_width for x in rect_1]
    plt.bar(
        rect_1,
        y1,
        width=bar_width,
        edgecolor="white",
        color = "#70CEFF",
        label="Before querying the Oracle",
    )

    plt.bar(
        rect_2,
        y2,
        width=bar_width,
        edgecolor="white",
        color = "#C756B2",
        label="After querying the Oracle",
    )
    plt.bar(
        rect_2,
        y3,
        width=bar_width,
        edgecolor="white",
        color = "#d4d4d4",
        label="After grovers operator",
    )

    plt.xlabel("State label")
    plt.ylabel("Probability Amplitude")
    plt.title("States probabilities amplitudes")

    plt.legend()
    plt.show()
    
y = results["execution_results"]
bit_strings = [f"{x:0{NUM_QUBITS}b}" for x in range(len(y))]

plt.bar(bit_strings, results["execution_results"], color = "#70CEFF")

plt.xticks(rotation="vertical")
plt.xlabel("State label")
plt.ylabel("Probability")
plt.title("States probabilities")

plt.show()