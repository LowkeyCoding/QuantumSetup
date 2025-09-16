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
workspace = Workspace.from_connection_string(os.environ['azure_connection'])
provider = AzureQuantumProvider(workspace)
# Selecting a backend
# Use simulators to test before running it on real hardware.
backend = provider.get_backend("ionq.simulator")

# Input bit string
msg = [0,0]
circ = QuantumCircuit(2)

# Bell state
circ.h(0)
circ.cx(0, 1)
# Message encoding 
if msg[0]:
    circ.x(0)
if msg[1]:
    circ.z(0)
# Message decoding
circ.cx(0, 1)
circ.h(0)
circ.measure_all()

circ.draw('mpl')

# Transpile circuit to work with the current backend.
qc_compiled = transpile(circ, backend)
# Run the job
# This will cause a pop where you have to authenticate with azure.
job_sim = backend.run(qc_compiled, shots=1024)

# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts()

# Plot the result
plot_histogram(counts)
pyplot.show()
