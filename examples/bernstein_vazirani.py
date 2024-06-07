from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from matplotlib import pyplot
from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import os

load_dotenv()

# It is highly recommended to use environment variables.
workspace = Workspace(resource_id=os.environ['azure_id'], location=os.environ['azure_location'])
provider = AzureQuantumProvider(workspace)
# Selecting a backend
# Use simulators to test before running it on real hardware.
backend = provider.get_backend("quantinuum.sim.h1-1e")

qubits = 6 # The number of physical qubits
a = 42 # the hidden integer

# Ensure it can be represented with the number of specified qubits
a = a % 2**(qubits)

# Setup the registers
qr = QuantumRegister(qubits)
cr = ClassicalRegister(qubits)

circ = QuantumCircuit(qr, cr)
for i in range(qubits):
    circ.h(qr[i])

circ.barrier()

for i in range(qubits):
    if (a & (1 << i)):
        circ.z(qr[i])
    else:
        circ.id(qr[i])
        circ.barrier()

for i in range(qubits):
    circ.h(qr[i])

circ.barrier()
circ.measure(qr,cr)
circ.draw("mpl")


# Transpile circuit to work with the current backend.
qc_compiled = transpile(circ, backend)
# Run the job
job_sim = backend.run(qc_compiled, shots=1024)
# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts()
# Plot the result
plot_histogram(counts)
pyplot.show()