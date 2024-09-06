from sklearn.datasets import load_diabetes
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from qiskit_algorithms.utils import algorithm_globals
from qiskit.circuit.library import ZZFeatureMap
from qiskit.circuit.library import RealAmplitudes
from qiskit_algorithms.optimizers import COBYLA
from matplotlib import pyplot as plt
import time
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as Sampler
from qiskit_algorithms.optimizers import COBYLA

optimizer = COBYLA(maxiter=100)
backend = AerSimulator()
sampler = Sampler()


# Requires the following packages
# - qiskit_machine_learning
# pip install qiskit_machine_learning

diabetes_data = load_diabetes()

print(diabetes_data.DESCR)

features = diabetes_data.data
labels = diabetes_data.target

# Normalize data to the interval 0-1
features = MinMaxScaler().fit_transform(features)

algorithm_globals.random_seed = 123
train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, train_size=0.8, random_state=algorithm_globals.random_seed
)

num_features = features.shape[1]

feature_map = ZZFeatureMap(feature_dimension=num_features, reps=1)
feature_map.decompose().draw(output="mpl", style="clifford", fold=20)

ansatz = RealAmplitudes(num_qubits=num_features, reps=3)
ansatz.decompose().draw(output="mpl", style="clifford", fold=20)


objective_func_vals = []
plt.rcParams["figure.figsize"] = (12, 6)


def callback_graph(weights, obj_func_eval):
    #clear_output(wait=True)
    #objective_func_vals.append(obj_func_eval)
    #plt.title("Objective function value against iteration")
    #plt.xlabel("Iteration")
    #plt.ylabel("Objective function value")
    #plt.plot(range(len(objective_func_vals)), objective_func_vals)
    #plt.show()
    x=1

vqc = VQC(
    sampler=sampler,
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=optimizer,
    callback=callback_graph,
)

# clear objective value history
objective_func_vals = []

start = time.time()
vqc.fit(train_features, train_labels)
elapsed = time.time() - start

print(f"Training time: {round(elapsed)} seconds")

train_score_q4 = vqc.score(train_features, train_labels)
test_score_q4 = vqc.score(test_features, test_labels)

print(f"Quantum VQC on the training dataset: {train_score_q4:.2f}")
print(f"Quantum VQC on the test dataset:     {test_score_q4:.2f}")

