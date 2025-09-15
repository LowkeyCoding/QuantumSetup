from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from matplotlib import pyplot
from dotenv import load_dotenv
from random import randbytes
import numpy as np
import os

# Section - Qubit Register and Classical Register Initialization
load_dotenv()

provider = QiskitRuntimeService(token=os.environ["ibm_token"], channel="ibm_cloud", instance=os.environ["ibm_crn"])

# Selecting a backend
real_backend = provider.least_busy(operational=True, simulator=False)
backend = AerSimulator.from_backend(real_backend)
sampler = Sampler(backend)

num_bits = 4 # number of random bits to generate

qr = QuantumRegister(num_bits, name='qr')
cr = ClassicalRegister(num_bits, name='cr')
qrng = QuantumCircuit(qr,cr)

# Section - Superposition State Preparation (Equal weights to all basis states)
for i in range(num_bits):
    qrng.h(qr[i])


qrng.measure(qr, cr)
# Section - Circuit Visualization
qrng.draw("mpl")

# Section - Circuit Execution and Result Analysis
qc_compiled = transpile(qrng, backend)
job_sim = sampler.run([qc_compiled], shots=1024)
result_sim = job_sim.result()
counts = result_sim[0].data.cr.get_counts()

# Plot the result
plot_histogram(counts)
pyplot.show()