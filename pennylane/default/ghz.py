import pennylane as qml
import matplotlib.pyplot as plt
from functools import partial

dev = qml.device("default.qubit", wires=3)

@partial(qml.set_shots, shots=1024)
@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    return qml.sample()

def to_mpl(samples):
    mpl_bins =  []
    for sample in samples:
        s_v = ""
        for v in sample:
            s_v += str(v)
        mpl_bins.append(s_v)
    return mpl_bins

result = circuit()
plt.hist(to_mpl(result))
plt.show()