from qiskit import *
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

# Section - Qubit Register and Classical Register Initialization
backend = AerSimulator()

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
job_sim = backend.run(qc_compiled, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)

# Plot the result
plot_histogram(counts)
pyplot.show()