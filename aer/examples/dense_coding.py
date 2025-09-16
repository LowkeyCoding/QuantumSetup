from qiskit import *
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

backend = AerSimulator()

# Input bit string
msg = [1,0]
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
qc_compiled = transpile(circ, backend)
job_sim = backend.run(qc_compiled, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc_compiled)
plot_histogram(counts)

pyplot.show()