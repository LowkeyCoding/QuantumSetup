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

# Braket requires all qubits in the program to be measured.
# The initial bit is the first in the bit string on the graph.
qr = QuantumRegister(9, name='qr')
cr = ClassicalRegister(9, name='cr')

shor = QuantumCircuit(qr,cr)

# Initial Bit Value
#shor.x(qr[0]) # Uncomment to set it to |1>

shor.cx(qr[0],qr[3])
shor.cx(qr[0],qr[6])

shor.h(qr[0])
shor.h(qr[3])
shor.h(qr[6])

shor.cx(qr[0],qr[1])
shor.cx(qr[3],qr[4])
shor.cx(qr[6],qr[7])

shor.cx(qr[0],qr[2])
shor.cx(qr[3],qr[5])
shor.cx(qr[6],qr[8])

shor.barrier(qr)

# Error Part of Circuit Start

shor.x(qr[0]) # Bit flip
shor.z(qr[0]) # Bit phase flip

# Error Part of Circuit End

shor.barrier(qr)
shor.cx(qr[0],qr[1])
shor.cx(qr[3],qr[4])
shor.cx(qr[6],qr[7])

shor.cx(qr[0],qr[2])
shor.cx(qr[3],qr[5])
shor.cx(qr[6],qr[8])

shor.ccx(qr[1],qr[2],qr[0])
shor.ccx(qr[4],qr[5],qr[3])
shor.ccx(qr[8],qr[7],qr[6])

shor.h(qr[0])
shor.h(qr[3])
shor.h(qr[6])

shor.cx(qr[0],qr[3])
shor.cx(qr[0],qr[6])
shor.ccx(qr[6],qr[3],qr[0])

shor.barrier(qr)

shor.measure(qr, cr)

shor.draw("mpl")

# Run shor code circuit
qc_compiled = transpile(shor, backend)
# Run the job
job_sim = backend.run(qc_compiled, shots=1024)
# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts()

# Plot the result
plot_histogram(counts)
pyplot.show()