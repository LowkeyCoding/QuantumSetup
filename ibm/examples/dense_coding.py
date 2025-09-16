from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from matplotlib import pyplot
from dotenv import load_dotenv
from random import randbytes
import numpy as np
import os
# Section - Setup

load_dotenv()

provider = QiskitRuntimeService(token=os.environ["ibm_token"], channel="ibm_cloud", instance=os.environ["ibm_crn"])

# Selecting a backend
real_backend = provider.least_busy(operational=True, simulator=False)
backend = AerSimulator.from_backend(real_backend)
sampler = Sampler(backend)

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
# Transpile circuit to work with the current backend.
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(circ)
# Run the job
sampler = Sampler(backend)
job = sampler.run([isa_circuit], shots=100)

# Get the result
result = job.result()
counts = result[0].data.meas.get_counts()
# Plot the result
plot_histogram(counts)
pyplot.show()
