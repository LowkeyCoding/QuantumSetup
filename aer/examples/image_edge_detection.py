from qiskit import *
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_toolkits.axes_grid1 import ImageGrid

# Selecting a backend
backend = AerSimulator()

SHOTS = 1024
image = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 1, 1, 0, 0],
                   [0, 1, 1, 1, 1, 1, 1, 0],
                   [0, 1, 1, 1, 1, 1, 1, 0],
                   [0, 1, 1, 1, 1, 1, 1, 0],
                   [0, 0, 0, 1, 1, 1, 1, 0],
                   [0, 0, 0, 1, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]])
N = image.shape[0]
M = image.shape[1]
# Function for plotting multiple image using matplotlib
def plot_image_sub(imgs, titles: [str],rows,cols,n):
    fig = plt.figure(n)
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                 nrows_ncols=(rows, cols),  # creates 2x2 grid of Axes
                 axes_pad=0.1,  # pad between Axes.
                 )
    plt.xticks(range(1,imgs[0].shape[0]))
    plt.yticks(range(1,imgs[1].shape[1]))
    for ax, im,title in zip(grid, imgs, titles):
        ax.imshow(im)
        ax.set_title(title)
        # Uncomment to show grid lines
        #ax.grid(True)

# Convert the raw pixel values to probability amplitudes
def amplitude_encode(img_data):
    
    # Calculate the RMS value
    rms = np.sqrt(np.sum(np.sum(img_data**2, axis=1)))
    
    # Create normalized image
    image_norm = []
    for arr in img_data:
        for ele in arr:
            image_norm.append(ele / rms)
        
    # Return the normalized image as a numpy array
    return np.array(image_norm)



# Initialize some global variable for number of qubits
data_qb = 6
anc_qb = 1
total_qb = data_qb + anc_qb

# Initialize the amplitude permutation unitary
D2n_1 = np.roll(np.identity(2**total_qb), 1, axis=1)


def scan_x(image_norm,amp_perm,total_qb, backend, shots):
    # Create the circuit for scanning
    qc = QuantumCircuit(total_qb)
    qc.initialize(image_norm, range(1, total_qb))
    qc.h(0)
    qc.unitary(D2n_1, range(total_qb), label= "Amplitude Permutation")
    qc.h(0)
    qc.measure_all()

    qc.draw("mpl")
    compiled = transpile(qc, backend, optimization_level=3)
    job_sim = backend.run(compiled, shots=shots)
    result_sim = job_sim.result()
    
    return result_sim.get_counts(compiled)

# Get the amplitude ancoded pixel values
# Horizontal: Original image
image_norm_h = amplitude_encode(image)
print(image_norm_h)

# Vertical: Transpose of Original image
image_norm_v = amplitude_encode(image.T)
print(image_norm_v)

counts_v = scan_x(image_norm_v,D2n_1,total_qb, backend,SHOTS)
counts_h = scan_x(image_norm_h,D2n_1,total_qb, backend,SHOTS)

# Get the measurement counts from the result
keys_h = counts_h.keys()
keys_v = counts_v.keys()

edge_scan_h = np.array([counts_h[f'{2*i+1:b}'.zfill(total_qb)] if f'{2*i+1:b}'.zfill(total_qb) in keys_h else 0 for i in range(2**data_qb)]).reshape(M, N)
edge_scan_v = np.array([counts_v[f'{2*i+1:b}'.zfill(total_qb)] if f'{2*i+1:b}'.zfill(total_qb) in keys_v else 0 for i in range(2**data_qb)]).reshape(M, N).T


plot_image_sub([edge_scan_h, edge_scan_v], ['Horizontal scan output','Vertical scan output'],1,2,5)
edge_detected_image = edge_scan_h + edge_scan_v

# Plotting the original and edge-detected images
plot_image_sub([edge_detected_image, image], ['Full Edge Detected Image', 'Original Image'],1,2,6)

plt.show()