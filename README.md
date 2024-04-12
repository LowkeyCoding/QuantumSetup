# Quantum Computing Setup Guide

Welcome to the uantum Computing Setup Guide! This repository contains code for setting up python for quantum computing using Qiskit.

## Basic setup

###  Step 1: Download Python 3
Download and install Python 3 from the official Python website: [Python.org](https://www.python.org/downloads/). Follow the installation instructions provided for your operating system.

###  Step 2: Setup Python environment
Go to your desired location and open a terminal or comand prompt and use the following commands to create and activate an environment.

#### Windows
```
py -m venv .venv
.venv\Scripts\activate
```
#### Unix/Mac
```
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Qiskit and Required Packages
In your command prompt/terminal install the required packages in your environment.

#### Windows
```
py -m pip install qiskit matplotlib pylatexenc numpy
```

#### Unix/Mac
```
python3 -m pip install qiskit matplotlib pylatexenc numpy
```

### Step 4: Install the backends you want to use

#### IBM Backend

If you want to use IBM Quantum hardware or simulators provided by IBM, switch to the `ibm_backend` branch. Follow the instructions in that branch's README for setup and usage.

[IBM Backend Branch](https://github.com/LowkeyCoding/QuantumSetup/tree/ibm_backend)

#### AER Backend

If you prefer to use the Aer simulator provided by Qiskit for local simulations, switch to the `aer_backend` branch. Refer to the instructions in that branch's README for setup and usage.

[AER Backend Branch](https://github.com/LowkeyCoding/QuantumSetup/tree/aer_backend)

#### Azure Backend

If you prefer to use the Azure simulator provided by Qiskit for local simulations, switch to the `azure_backend` branch. Refer to the instructions in that branch's README for setup and usage.

[Azure Backend Branch](https://github.com/LowkeyCoding/QuantumSetup/tree/azure_backend)

### Step 5: Optionally install Jupyter
Jupyter is a powerful tool for developing quantum algorithms due to its interactive nature. With Jupyter notebooks, developers can write code interspersed with explanatory text, equations, and visualizations. This makes it easy to experiment with different quantum algorithms, visualize quantum states, and analyze results in real-time.

To install the jupyter python package by running the following command in your terminal.
### Windows
```
py -m pip install jupyter
```
### Unix
```
python3 -m pip install jupyter
```
After installing the Python package, you'll also need to install the Jupyter extension for VSCode. You can do this by searching for "Jupyter" in the Extensions view and installing the "Jupyter" extension. Alternatively go to [Jupyter Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) to install the extension.



## Usage

Once you have selected the appropriate branch, followed the instructions provided in the README of that branch to set up your environment and run the code.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.
