from braket.aws.aws_session import AwsSession 
import boto3
import os 
from dotenv import load_dotenv
from random import randbytes
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

key_len = 16  # for a local backend n can go as up as 23, after that it raises a Memory Error
shots = 100 # Number of times each circuit is executed

qr = QuantumRegister(key_len, name='qr')
cr = ClassicalRegister(key_len, name='cr')

alice = QuantumCircuit(qr, cr, name="a") # Alice circuit
bob = QuantumCircuit(qr, cr, name="b") # Bob circuit

# Create 

alice_key = int.from_bytes(randbytes(int(key_len/8)))
# Cast key to binary for encoding
alice_key = np.binary_repr(alice_key, key_len) # n is the width
# Encode key as alice qubits 
# IBM's qubits are all set to |0> initially
for index, digit in enumerate(alice_key):
    if digit == '1':
        alice.x(qr[index]) # if key has a '1', change state to |1>

def create_basis(qc, qr):
    basis = []
    for index in range(len(qr)):
        if 0.5 < np.random.random():   # 50% chance
            qc.h(qr[index])         # change to diagonal basis
            basis.append('X')    # character for diagonal basis
        else:
            basis.append('Z')
    return basis

# Create basis for Alice and Bob
alice_basis = create_basis(alice, qr)
bob_basis = create_basis(bob, qr)

alice_bob = alice.copy()
alice_bob.compose(bob, inplace=True)
for index in range(len(qr)): 
    alice_bob.measure(qr[index], cr[index])

# Transpile circuit to work with the current backend.
qc_compiled = transpile(alice_bob, backend)
# Run the job
job_sim = backend.run(qc_compiled, shots=shots)
# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts()
for key, count in counts.items():
    bob_key = key[::-1]
    shared_idx = [] # Get the indexes of shared basis
    for idx, basis in enumerate(zip(alice_basis, bob_basis)):
        if basis[0] == basis[1]:
            shared_idx.append(idx)
        
    shared_key_a = [alice_key[idx] for idx in shared_idx]
    shared_key_b = [bob_key[idx] for idx in shared_idx]
    acc = 0
    for bit in zip(shared_key_a, shared_key_b):
        if bit[0] == bit[1]:
            acc += 1
    fails = 0

    if acc != len(shared_key_a): # Check if all bits match
        fails +=1*count

print(f"total executions: {shots}")
print(f"Succ rate: {(shots-fails)/shots}")
print(f"Fail rate: {fails/shots}")

# Plot the result
plot_histogram(counts)
pyplot.show()