> :warning: **Cloud simulators have been deprecated and will be removed on 15 May 2024.**
# Step 1: Setup the Backend

If you're using Windows, open Command Prompt (cmd.exe) or PowerShell. If you're using Unix-based systems like Linux or macOS, open Terminal.
Run the following command to install the azure backend and other required dependencies:

## Windows
```
.venv\Scripts\activate
py -m pip install qiskit-ibm-runtime
```

## Unix

```
source .venv/bin/activate
python3 -m pip install qiskit-ibm-runtime
```

# Step 2: Get API Key from IBM Quantum Dashboard

Go to the IBM Quantum Dashboard website (https://quantum-computing.ibm.com/).
If you don't have an account, sign up for one. Otherwise, log in.
Once logged in, navigate to your dashboard. You'll find your API key there.
Copy your API key. This will be used to authenticate your access to IBM Quantum services.
![alt text](./images/api_key.png "Title")
Paste your API key into the `save_account.py` file then run it. It is important that you never run it on untrusted systems and NEVER publish the `save_account.py` with the api key in it. After running it once on a system the account will automatically be used when using the IBM backend.

With these two steps completed, you'll have Qiskit installed and configured to use IBM Quantum hardware. You can then start experimenting with quantum circuits and running them on real quantum computers provided by IBM.

# Step 3: Listing accesible backends.
To list the currently available backends add the snippet below to the login example.
```python
print("This workspace's targets:")
for backend in provider.backends():
    print("- " + backend.name)
```
This should produce a list like the one below.
```
This workspace's targets:
- simulator_mps
- simulator_statevector
- simulator_stabilizer
- ibm_brisbane
- ibm_osaka
- ibmq_qasm_simulator
- simulator_extended_stabilizer
```
# Step 4: Running a quantum circuit.
To run a quantum circuit a specific backend has to be chosen from the list of currently available ones. This is done by getting the backend from the provider `backend = provider.get_backend("simulator_mps")` as seen in the example below. It is important to always test programs on the simulator first and, in general, limit the usage of real hardware as the cost adds up extremely quickly.
```python
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from matplotlib import pyplot

provider = QiskitRuntimeService()

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
```
The example can also be seen [here](https://github.com/LowkeyCoding/QuantumSetup/blob/ibm_backend/sample.py)

# Step 5: Running simulator after the 15th of may
To access advanced simulation capabilities in Qiskit of IBM systems, the `qiskit-aer` package is required.

## Windows
```
py -m pip install qiskit_aer
```

## Unix
```
python3 -m pip install qiskit_aer
```

To run a simulation, it is required to first load the real hardware backend from IBM as in the previous step and then use the backend to instantiate the Aer simulator.

```python
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from matplotlib import pyplot

provider = QiskitRuntimeService()

# Selecting a backend hardware from ibm.,
real_backend = provider.backend("ibm_brisbane")
# Instantiate Aer simulator with hardware backend.
backend = AerSimulator.from_backend(real_backend)
```

The full example can be seen [here](https://github.com/LowkeyCoding/QuantumSetup/blob/ibm_backend/sample_new.py)