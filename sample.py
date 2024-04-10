from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import transpile
from matplotlib import pyplot

workspace = Workspace(  
    resource_id = " ", # Add the resourceID of your workspace
    location = "" # Add the location of your workspace (for example "westus")
)

provider = AzureQuantumProvider(workspace)

backend = provider.get_backend("ionq.simulator")

circuit = QuantumCircuit(3, 3)
circuit.name = "TEST"
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0, 1, 2])

circuit.draw('mpl')
qc_compiled = transpile(circuit, backend)
job_sim = backend.run(qc_compiled, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)

plot_histogram(counts)
pyplot.show()