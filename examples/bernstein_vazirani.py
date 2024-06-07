from qiskit import *
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

backend = AerSimulator()

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


qc_compiled = transpile(circ, backend)
job_sim = backend.run(qc_compiled, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)

# Plot the result
plot_histogram(counts)
pyplot.show()