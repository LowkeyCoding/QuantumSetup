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

## Useful links:
- https://docs.pennylane.ai/en/stable/
- https://pennylane.ai/search/?contentType=DEMO&categories=how-to&sort=publication_date
- https://pennylane.ai/devices
- https://matplotlib.org/stable/users/index
- https://matplotlib.org/stable/index.html