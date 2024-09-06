from braket.aws.aws_session import AwsSession 
import boto3
import os 
from dotenv import load_dotenv
from qiskit import *
from qiskit_braket_provider import BraketProvider
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

# Section - Backend and Qubit Register Initialization
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
num_bits = 3 # number of random bits to generate

qr = QuantumRegister(num_bits, name='qr')
cr = ClassicalRegister(num_bits, name='cr')
grover = QuantumCircuit(qr,cr)

# Section - Superposition State Preparation
for i in range(num_bits):
    grover.h(qr[i])

# Section - Oracle Definition
oracle = QuantumCircuit(qr, name="Oracle")
oracle.cz(0,2) # | 101>
oracle.cz(1,2) # | 011>
oracle.to_gate()

def create_diffuser(num_bits):
    """
    Creates the diffuser circuit for Grover's algorithm.

    Args:
        num_qubits: The number of qubits in the circuit.

    Returns:
        The diffuser circuit as a QuantumCircuit object.
    """
    diffuser_qr = QuantumRegister(num_bits, name="diffuser_qubits")
    diffuser_qc = QuantumCircuit(diffuser_qr, name="Diffuser")

    # Apply Hadamard gates to all qubits
    diffuser_qc.h(diffuser_qr)

    # Apply X gates to all qubits
    diffuser_qc.x(diffuser_qr)

    # Apply multi-controlled Z gate (with all qubits as controls)
    diffuser_qc.h(num_bits - 1)
    diffuser_qc.mcx(list(range(num_bits - 1)), num_bits - 1)  # Target is the last qubit
    diffuser_qc.h(num_bits - 1)

    # Apply X gates to all qubits
    diffuser_qc.x(diffuser_qr)

    # Apply Hadamard gates to all qubits
    diffuser_qc.h(diffuser_qr)

    return diffuser_qc
# Section - Grover Iteration (Oracle + Diffuser)
diffuser = create_diffuser(num_bits)

grover.append(oracle, qr)
grover.append(diffuser, qr)

# Section - Measurement
grover.measure(qr,cr)
grover.draw("mpl")

# Section - Circuit Execution and Result Analysis

qc_compiled = transpile(grover, backend)
job_sim = backend.run(qc_compiled, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts()

# Plot the result
plot_histogram(counts)
pyplot.show()