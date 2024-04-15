# Step 1: Setup the backend

If you're using Windows, open Command Prompt (cmd.exe) or PowerShell. If you're using Unix-based systems like Linux or macOS, open Terminal.
Run the following command to install Qiskit and other required dependencies:

## Windows
```
.venv\Scripts\activate
py -m pip install qiskit-aer
```

## Unix/Mac

```
source .venv/bin/activate
python3 -m pip install qiskit-aer
```

# Step 2: Running a quantum circuit.
Below you will find a simple bell-state quantum circuit that can be used to test your installation.
```python
from qiskit import *
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

circ = QuantumCircuit(3)

circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)

circ.measure_all()
circ.draw('mpl')

# Setting a backend
backend = AerSimulator()

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

# Step 3: Running with noise
It is possible to run circuits with noise the easiest way to add noise to a simulation is following the setup for the [IBM backend](https://github.com/LowkeyCoding/QuantumSetup/tree/ibm_backend) where in **step 6** there is a guide to adding noise to the Aer simulator

