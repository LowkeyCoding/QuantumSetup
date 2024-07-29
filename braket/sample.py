from braket.aws.aws_session import AwsSession 
import boto3
import os 
from dotenv import load_dotenv

from qiskit import *
import numpy as np
from qiskit_braket_provider import BraketProvider
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

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

circ = QuantumCircuit(3)

circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)

circ.measure_all()
circ.draw('mpl')

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