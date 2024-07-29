# Step 1: Setup the Backend

If you're using Windows, open Command Prompt (cmd.exe) or PowerShell. If you're using Unix-based systems like Linux or macOS, open Terminal.
Run the following command to install the azure backend and other required dependencies:

## Windows
```
.venv\Scripts\activate
py -m pip install azure-quantum azure-quantum[qiskit]
```

## Unix

```
source .venv/bin/activate
python3 -m pip install azure-quantum "azure-quantum[qiskit]" 
```

Unix users may need to install `PyQt5` if they dont use Jupyter to show plots
```
python3 -m pip install PyQt5
```

# Step 2: Get the `Resource ID` and `Location` 
To find the `Resource ID` and `Location` go to [azure portal](https://portal.azure.com/#home) and locate `Quantum workspaces` under services. From there you should be able to see them as shown below.
![Locate Resource ID and Location](https://learn.microsoft.com/en-us/azure/quantum/media/azure-quantum-resource-id.png)

# Step 3: Loginin from python.
To log in, use the Python snippet below, but you must never share the resource_id on GitHub or any other public site. 
```python
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
workspace = Workspace(resource_id="ID HERE", location="LOCATION HERE")
provider = AzureQuantumProvider(workspace)
```
One way to avoid this is by using a `.env` file that is the `.gitignore` to ensure that it is not uploaded to git. The `.env` file should be structured as shown below.
```ini
azure_id=ID HERE
azure_location=LOCATION HERE
```
Loading the new environment variables is done using the `dotenv` package and the `load_dotenv` function.

```python
import os
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()


workspace = Workspace(resource_id=os.environ['azure_id'], location=os.environ['azure_location'])
provider = AzureQuantumProvider(workspace)
```


# Step 4: Listing accesible backends.
To list the currently available backends add the snippet below to the login example.
```python
print("This workspace's targets:")
for backend in provider.backends():
    print("- " + backend.name())
```
This should produce a list like the one below.
```
This workspace's targets:
- ionq.qpu
- ionq.qpu.aria-1
- ionq.simulator
- microsoft.estimator
- quantinuum.hqs-lt-s1
- quantinuum.hqs-lt-s1-apival
- quantinuum.hqs-lt-s2
- quantinuum.hqs-lt-s2-apival
- quantinuum.hqs-lt-s1-sim
- quantinuum.hqs-lt-s2-sim
- quantinuum.qpu.h1-1
- quantinuum.sim.h1-1sc
- quantinuum.sim.h1-1e
- rigetti.sim.qvm
- rigetti.qpu.ankaa-2
```
# Step 5: Running a quantum circuit.
To run a quantum circuit a specific backend has to be chosen from the list of currently available ones. This is done by getting the backend from the provider `backend = provider.get_backend("ionq.simulator")` as seen in the example below. It is important to always test programs on the simulator first and, in general, limit the usage of real hardware as the cost adds up extremely quickly.
```python
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
workspace = Workspace(resource_id=os.environ['azure_id'], location=os.environ['azure_location'])
#workspace = Workspace(resource_id="ID HERE", location="LOCATION HERE")
provider = AzureQuantumProvider(workspace)
# Selecting a backend
# Use simulators to test before running it on real hardware.
backend = provider.get_backend("ionq.simulator")


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
```
