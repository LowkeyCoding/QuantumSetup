from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from matplotlib import pyplot
from dotenv import load_env
import os

load_env()

provider = QiskitRuntimeService(os.environ["ibm_token"], channel="ibm_quantum")

# Selecting a backend
# Use simulators to test before running it on real hardware.
backend = provider.get_backend("simulator_mps")
# Optionally use where operational means running on hardware.
#backend = provider.least_busy(operational=False, simulator=True)

circuit = QuantumCircuit(3, 3)
circuit.name = "My First Quantum Program"
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0, 1, 2])

circuit.draw('mpl')

# Transpile circuit to work with the current backend.
qc_compiled = transpile(circuit, backend)
# Run the job
# This will cause a pop where you have to authenticate with azure.
job_sim = backend.run(qc_compiled, shots=1024)

# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)

# Plot the result
plot_histogram(counts)
pyplot.show()