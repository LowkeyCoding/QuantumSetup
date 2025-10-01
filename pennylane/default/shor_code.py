import pennylane as qml
import matplotlib.pyplot as plt
from functools import partial

NUM_QUBITS = 9
dev = qml.device("default.qubit", wires=NUM_QUBITS)

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit():
    #qml.X(0) # Uncomment to set the first qubit to |1> (optional)

    qml.CNOT([0,3])
    qml.CNOT([0,6])

    qml.Hadamard(0)
    qml.Hadamard(3)
    qml.Hadamard(6)

    qml.CNOT([0,1])
    qml.CNOT([3,4])
    qml.CNOT([6,7])

    qml.CNOT([0,2])
    qml.CNOT([3,5])
    qml.CNOT([6,8])

    qml.Barrier()
    # Error Part of Circuit Start

    qml.X(0) # Bit flip
    qml.Z(0) # Bit phase flip

    # Error Part of Circuit End
    qml.Barrier()

    qml.CNOT([0,1])
    qml.CNOT([3,4])
    qml.CNOT([6,7])
    
    qml.CNOT([0,2])
    qml.CNOT([3,5])
    qml.CNOT([6,8])

    qml.Toffoli([1,2,0])
    qml.Toffoli([4,5,3])
    qml.Toffoli([8,7,6])

    qml.Hadamard(0)
    qml.Hadamard(3)
    qml.Hadamard(6)

    qml.CNOT([0,3])
    qml.CNOT([0,6])
    qml.Toffoli([6,3,0])

    return qml.probs(wires=[0])

qml.draw_mpl(circuit)()
result = circuit()
fig, ax = plt.subplots()    
ax.bar(result, ['0','1'])
ax.set_xticks([0,1])
plt.show()