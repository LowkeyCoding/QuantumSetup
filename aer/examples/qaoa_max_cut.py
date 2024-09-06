# This code was update/modified from https://github.com/Qiskit/textbook/blob/main/notebooks/ch-applications/qaoa.ipynb
from qiskit import *
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

# Circuit Specific Imports
from qiskit.circuit import Parameter
from scipy.optimize import minimize

# Section - Backend Setup and Graph Definition
backend = AerSimulator()

# Define a graph representing a square. Each node is identified by an integer.
graph = {
    "nodes": [0,1,2,3],
    "edges": [(0, 1), (1, 2), (2, 3), (3, 0)]
}

NODES = "nodes"
EDGES = "edges"

# Section - Maxcut Cost
def maxcut_cost(solution, graph):
    """Calculates the cost (negative of the number of edges cut) for a given solution.

    Args:
        solution (string): A binary string representing the set assignment of each vertex.
        graph (dict): A dictionary representing the graph, with keys "nodes" and "edges."

    Returns:
        int: The cost (negative of the number of edges cut) for the given solution.
    """
    cost = 0
    for i, j in graph[EDGES]:
        if solution[i] != solution[j]:
            cost -= 1
    return cost
# Section - Expected Value
def compute_expectation(counts, graph):
    """Calculates the expected value of the cost function given measurement results.

    Args:
        counts (dict): A dictionary mapping bitstrings to their counts from quantum circuit execution.
        graph (dict): A dictionary representing the graph, with keys "nodes" and "edges."

    Returns:
        float: The expected value of the cost function.
    """
    avg = 0
    sum_count = 0
    for bit_string, count in counts.items():
        obj = maxcut_cost(bit_string, graph)
        avg += obj * count
        sum_count += count
    return avg/sum_count

# Section - Circuit Creation
def create_qaoa_circ(graph, theta):
    """Constructs a parameterized QAOA circuit for the Max-Cut problem.

    Args:
        graph (dict): A dictionary representing the graph, with keys "nodes" and "edges."
        theta (list): A list of unitary parameters

    Returns:
        QuantumCircuit: The constructed QAOA circuit.
    """
    nqubits = len(graph[NODES]) # Number of Qubits
    n_layers = len(theta)//2    # Number of alternating unitaries
    beta = theta[:n_layers]
    gamma = theta[n_layers:]
    qc = QuantumCircuit(nqubits)

    # Initial_state
    qc.h(range(nqubits))

    for layer_index in range(n_layers):
        # Problem unitary
        for pair in list(graph[EDGES]):
            qc.rzz(2 * gamma[layer_index], pair[0], pair[1])
        # Mixer unitary
        for qubit in range(nqubits):
            qc.rx(2 * beta[layer_index], qubit)
    qc.measure_all()
    return qc

# Section - Calculate Expected Value
def get_expectation(graph, backend, shots=512):
    """Calculates the expected value of the cost function given measurement results.

    Args:
        counts (dict): A dictionary mapping bitstrings to their counts from quantum circuit execution.
        graph (dict): A dictionary representing the graph, with keys "nodes" and "edges."

    Returns:
        float: The expected value of the cost function.
    """
    def execute_circ(theta):
        """Executes the QAOA circuit with given parameters and returns the expectation value."""
        qc = create_qaoa_circ(graph, theta)
        qc_compiled = transpile(qc, backend)
        job_sim = backend.run(qc_compiled, shots=shots)
        counts = job_sim.result().get_counts(qc_compiled)
        return compute_expectation(counts, graph)
    return execute_circ

# Section - Optimizing Circuit
# Get the function to calculate expectation for optimization
expectation = get_expectation(graph, backend)

res = minimize(expectation,
               [1.0, 1.0],      # Initial guess for parameters
               method='COBYLA') # Classical optimization method
# Print the result of the minimization function
print(res)

# Section - Optimized Circuit
# Create the final circuit with optimized parameters
qc_res = create_qaoa_circ(graph, res.x)

# Draw the final circuit
qc_res.draw("mpl")

# Section - Circuit Execution and Result Analysis
# Execute the circuit and visualize results
qc_compiled = transpile(qc_res, backend)
job_sim = backend.run(qc_compiled, shots=512)
counts = job_sim.result().get_counts(qc_compiled)

# Expected spikes at the solutions ["1010", "0101"]
plot_histogram(counts)
pyplot.show()