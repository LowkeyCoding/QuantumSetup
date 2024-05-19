# Quantum Computing Setup Guide

Welcome to the Quantum Computing Setup Guide! This repository contains code for setting up python for quantum computing using Qiskit.

## Basic setup

###  Step 1: Download Python 3
Download and install Python 3 from the official Python website: [Python.org](https://www.python.org/downloads/). Follow the installation instructions provided for your operating system.

###  Step 2: Setup Python environment
Go to your deseired folder for your quantum project and open a terminal or comand prompt and use the following commands to create and activate an environment.

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

To enter the project's virtual environment, you'll need to run the second command. It's crucial to ensure you're in the virtual environment, especially when installing packages. This helps prevent conflicts with system-wide packages. Make sure to check if you're in the virtual environment by verifying if `(.venv)` is appended to the current path in the terminal before installing any packages. If you are still unsure, then you can run the second command to enter it.

### Step 3: Install Qiskit and Required Packages
To create a basic setup with a couple of helpful packages for quantum computing, install the following packages for your operating system.

#### Windows
```
py -m pip install qiskit matplotlib pylatexenc numpy python-dotenv
```

#### Unix/Mac
```
python3 -m pip install qiskit matplotlib pylatexenc numpy python-dotenv
```

### Step 4: Environment file
First step is creating an environment file with the name `.env` in your project folder. This file should never be shared, as anyone who has access will be able to spend credits. If you are using `git`, this can be avoided by adding it to the `.gitignore` file, by adding the line `.env`. The environment file operates as a key-value store, utilizing the format `key = value`, with each key on a separate line. In subsequent guides for various backends, we will employ the `.env` file to store login information.

### Step 5: Install the backends you want to use

#### IBM Backend

If you want to use IBM Quantum hardware or simulators provided by IBM, switch to the `ibm_backend` branch. Follow the instructions in that branch's README for setup and usage.

[IBM Backend Branch](https://github.com/LowkeyCoding/QuantumSetup/tree/ibm_backend)

#### Azure Backend

If you want to use Azure Quantum hardware or simulators provided by Azure, switch to the `azure_backend` branch. Refer to the instructions in that branch's README for setup and usage.

[Azure Backend Branch](https://github.com/LowkeyCoding/QuantumSetup/tree/azure_backend)

#### Braket Backend

If you want to use Braket Quantum hardware or simulators provided by Amazon, switch to the `braket_backend` branch. Refer to the instructions in that branch's README for setup and usage.

[Braket Backend Branch](https://github.com/LowkeyCoding/QuantumSetup/tree/braket_backend)

#### AER Backend

If you prefer to use the Aer simulator provided by Qiskit for local simulations, switch to the `aer_backend` branch. Refer to the instructions in that branch's README for setup and usage.

[AER Backend Branch](https://github.com/LowkeyCoding/QuantumSetup/tree/aer_backend)


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


## Helpful resources
* [**Python Documentation**](https://docs.python.org/3.12/)
* [**Qiskit Documentation**](https://docs.quantum.ibm.com/)
* [**Matplotlib Documentation**](https://matplotlib.org/stable/index.html)
* [**Numpy Documentation**](https://numpy.org/devdocs/)

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Authors/Contributers
* [Loke Walsted](https://github.com/Lowkeycoding)
* [Torben Larsen](https://github.com/t-larsen/)
