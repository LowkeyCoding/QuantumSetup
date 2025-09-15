from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from matplotlib import pyplot
from dotenv import load_dotenv
import os

load_dotenv()

provider = QiskitRuntimeService(token=os.environ["ibm_token"], channel="ibm_cloud", instance=os.environ["ibm_crn"])

# Selecting a backend
real_backend = provider.least_busy(operational=True, simulator=False)
backend = AerSimulator.from_backend(real_backend)

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
job_sim = sampler.run([qc_compiled], shots=1024)

# Get the result
result_sim = job_sim.result()
counts = result_sim[0].data.cr.get_counts()

# Plot the result
plot_histogram(counts)
pyplot.show()