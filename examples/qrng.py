from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from matplotlib import pyplot
from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import os

load_dotenv()

workspace = Workspace(resource_id=os.environ['azure_id'], location=os.environ['azure_location'])
provider = AzureQuantumProvider(workspace)
# Selecting a backend
# Use simulators to test before running it on real hardware.
backend = provider.get_backend("rigetti.sim.qvm")

num_bits = 4 # number of random bits to generate

qr = QuantumRegister(num_bits, name='qr')
cr = ClassicalRegister(num_bits, name='cr')
qrng = QuantumCircuit(qr,cr)

for i in range(num_bits):
    qrng.h(qr[i])

qrng.measure(qr, cr)
qrng.draw("mpl")

# Run shor code circuit
qc_compiled = transpile(qrng, backend)
job_sim = backend.run(qc_compiled, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)

# Plot the result
plot_histogram(counts)
pyplot.show()