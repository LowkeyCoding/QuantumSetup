from braket.aws.aws_session import AwsSession 
import boto3
import os 
from qiskit import *
import numpy as np
from qiskit.visualization import plot_histogram
from qiskit_braket_provider import BraketProvider
from matplotlib import pyplot
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

boto_session = boto3.Session(
    aws_access_key_id=os.environ['aws_access'],
    aws_secret_access_key=os.environ['aws_secret'],
    region_name=os.environ['aws_region'],
)
session = AwsSession(boto_session)

provider = BraketProvider()

backend = provider.get_backend("SV1", aws_session = session)

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


# Transpile circuit to work with the current backend.
qc_compiled = transpile(circ, backend)
# Run the job
job_sim = backend.run(qc_compiled, shots=1024)
# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts()

# Plot the result
plot_histogram(counts)
pyplot.show()