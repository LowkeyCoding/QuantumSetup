import pennylane as qml
import matplotlib.pyplot as plt
import numpy as np
from functools import partial

NUM_QUBITS=8
dev = qml.device("default.qubit", wires=NUM_QUBITS)

def get_status(acc, key_a, eve=False):
    if len(key_a) == 0:
        return "failed" + (" no shared key found" if eve else "")
    if acc != len(key_a):
        return "failed"  + (" shared keys are not equal (Eve Detected)" if eve else "")
    return "succeeded" + (" Eve was not detected" if eve else "")

def prep_key_state(key):
    for i,x in enumerate(key):
        if x == 1:
            qml.X(wires=i)

def create_basis(basis):
    for i,v in enumerate(basis):
        if v:
            qml.Hadamard(wires=i)
    return basis

def get_shared_key(key_a, key_b, basis_a,basis_b):
    acc = 0
    shared_idx = [] # Get the indexes of shared basis
    for idx, basis in enumerate(zip(basis_a, basis_b)):
        if basis[0] == basis[1]:
            shared_idx.append(idx)
    shared_key_a = [key[idx] for idx in shared_idx]
    shared_key_b = [int(key_b[idx]) for idx in shared_idx] # Converting np.int64 to python int
    for bit in zip(shared_key_a, shared_key_b):
        if bit[0] == bit[1]:
            acc += 1
    return (shared_key_a, shared_key_b, acc)

@partial(qml.set_shots, shots=1)
@qml.qnode(dev)
def circuit(key,basis_a,basis_b):
    prep_key_state(key) # Prep alice's key
    create_basis(basis_a) # Create alice's basis
    create_basis(basis_b) # Create bob's basis
    return qml.sample()

# Alice communicating with Bob
key = [1 if np.random.random() > 0.5 else 0 for i in range(NUM_QUBITS)]
basis_a = [1 if np.random.random() > 0.5 else 0 for i in range(NUM_QUBITS)]
basis_b = [1 if np.random.random() > 0.5 else 0 for i in range(NUM_QUBITS)]

print("State preperation details:")
print(f"Alice's key: {key}")
print(f"Alice's basis: {basis_a}")
print(f"Bob's basis: {basis_b}")
to_int_list = lambda l: list(map(int, l))
key_b = to_int_list(circuit(key,basis_a,basis_b))

(shared_key_a, shared_key_b, acc) = get_shared_key(key, key_b, basis_a, basis_b)
# Result of Alice -> Bob
print("\nBB84 Circuit: Alice -> Bob")
print(qml.draw(circuit)(key,basis_a,basis_b))
qml.draw_mpl(circuit)(key,basis_a,basis_b)

print(f"\nPure Execution without Eve")
print(f"Alice shared key = {shared_key_a}")
print(f"Bob shared key   = {shared_key_b}")
print(f"Key sharing {get_status(acc, shared_key_a)}")

# Alice communicating with Eve
basis_e = [1 if np.random.random() > 0.5 else 0 for i in range(NUM_QUBITS)]
key_e = to_int_list(circuit(key,basis_a,basis_e))
print("\nState preperation details:")
print(f"Alice's key: {key}")
print(f"Alice's basis: {basis_a}")
print(f"Eve's basis: {basis_e}")

print("\nBB84 Circuit: Alice -> Eve")
print(qml.draw(circuit)(key,basis_a,basis_e))
qml.draw_mpl(circuit)(key,basis_a,basis_e)

# Eve communicating with Bob
print("\nState preperation details:")
print(f"Eve's key: {key_e}")
print(f"Eve's basis: {basis_e}")
print(f"Bob's basis: {basis_b}")

key_b = to_int_list(circuit(key_e,basis_e,basis_b))
print("\nBB84 Circuit: Eve -> Bob")
print(qml.draw(circuit)(key_e,basis_e,basis_b))
qml.draw_mpl(circuit)(key_e,basis_e,basis_b)

(shared_key_a, shared_key_b, acc) =  get_shared_key(key, key_b, basis_a, basis_b)
# Result of Alice -> Eve -> Bob
print(f"\nExecution with Eve")
print(f"Alice shared key = {shared_key_a}")
print(f"Bob shared key   = {shared_key_b}")

print(f"Key sharing {get_status(acc, shared_key_a, True)}")
plt.show()
