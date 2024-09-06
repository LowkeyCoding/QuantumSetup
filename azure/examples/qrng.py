from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from matplotlib import pyplot
from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import numpy as np
import os

# Section - Qubit Register and Classical Register Initialization
load_dotenv()
workspace = Workspace.from_connection_string(os.environ['azure_connection'])
provider = AzureQuantumProvider(workspace)
# Selecting a backend
# Use simulators to test before running it on real hardware.
backend = provider.get_backend("rigetti.sim.qvm")

num_bits = 4 # number of random bits to generate

qr = QuantumRegister(num_bits, name='qr')
cr = ClassicalRegister(num_bits, name='cr')
qrng = QuantumCircuit(qr,cr)

# Section - Superposition State Preparation (Equal weights to all basis states)
for i in range(num_bits):
    qrng.h(qr[i])


qrng.measure(qr, cr)
# Section - Circuit Visualization
qrng.draw("mpl")

# Section - Circuit Execution and Result Analysis
qc_compiled = transpile(qrng, backend)
job_sim = backend.run(qc_compiled, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)

# Plot the result
plot_histogram(counts)
pyplot.show()