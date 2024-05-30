import os
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit import transpile
from matplotlib import pyplot
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# It is highly recommended to use environment variables.
#provider = AzureQuantumProvider(resource_id="ID HERE", location="LOCATION HERE")
workspace = Workspace(resource_id=os.environ['azure_id'], location=os.environ['azure_location'])
provider = AzureQuantumProvider(workspace)
# Selecting a backend
# Use simulators to test before running it on real hardware.
backend = provider.get_backend("ionq.simulator")


circ = QuantumCircuit(3, 3)
circ.name = "My First Quantum Program"
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure([0,1,2], [0, 1, 2])

circ.draw('mpl')

# Transpile circuit to work with the current backend.
qc_compiled = transpile(circ, backend)
# Run the job
# This will cause a pop where you have to authenticate with azure.
job_sim = backend.run(qc_compiled, shots=1024)

# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)

# Plot the result
plot_histogram(counts)
pyplot.show()