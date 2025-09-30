# Pennylane Quantum setup
After running `qproject` and selecting the examples you want to download.

## Running Pennylane examples
The pennylane has [multiple backends](https://pennylane.ai/devices) depending on your setup. With quantum setup to select a specific backend use the `--extra` flag when using `uv`. Currently you can choose between the following backends `cpu,gpu` and `tensor`. However to select the backend you will have to modify the device in the example you want to `qubit.default`, `lightning.gpu` ot `lightning.tensor`. For example running the `qrng` example with `gpu`:
First modify the line:
```
dev = qml.device('default.qubit', wires=NUM_QUBITS) 
```
to the following:
```
dev = qml.device('lightning.gpu', wires=NUM_QUBITS) 
```
and then run the example with `--extra gpu`:
```
uv run --extra gpu qrng.py  
```

## After closing terminal
If you close the terminal you will no longer be in you projects virutal environment. Therefore to re-enter the virtual environment use the following command for you system when you are in your project folder. 

### Windows
```
.venv\Scripts\activate
```
### Linux/MacOS
```
source .venv/bin/activate
```

## Need extra packages?
To add a package use `uv add package_name` where `package_name` is replaced with the python package you want to add to your project.

## Useful links:

* [**Pennylane Documentation**](https://pennylane.ai/devices)
* [**Pennylane Devices**](https://docs.pennylane.ai/en/stable/)
* [**Pennylane Examples**](https://pennylane.ai/search/?contentType=DEMO&categories=how-to&sort=publication_date)
* [**Pennylane Noisy Circuits**](https://pennylane.ai/qml/demos/tutorial_noisy_circuits)
* [**Python Documentation**](https://docs.python.org/3.12/)
* [**UV Documentation**](https://docs.astral.sh/uv/getting-started/features/#scripts)
* [**Matplotlib Documentation**](https://matplotlib.org/stable/index.html)
* [**Numpy Documentation**](https://numpy.org/devdocs/)