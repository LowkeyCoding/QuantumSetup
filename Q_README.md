# Setup

## Environment 
To setup the development environment run the following command:
### windows
```
.venv\Scripts\activate
```
If you encounter an error like `scripts cannot be loaded because running scripts is disabled on this system` you need to adjust your PowerShell execution policy. This can be done by running the following command in an elevated PowerShell window (run as administrator):

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
This command allows the execution of locally stored scripts and remote scripts signed by trusted publishers.
### unix

```
source .venv/bin/activate
```
## Use uv
### Run
To run files use:
```
uv run file.py
```
replacing `file` with the python script you want to run.
### Install packages
To install package in environment run:
```
uv pip install package_name
```
replacing `package_name` with the package you want to run.

## Helpful resources
* [**Python Documentation**](https://docs.python.org/3.12/)
* [**UV Documentation**](https://docs.astral.sh/uv/getting-started/features/#scripts)
* [**Qiskit Documentation**](https://docs.quantum.ibm.com/)
* [**Matplotlib Documentation**](https://matplotlib.org/stable/index.html)
* [**Numpy Documentation**](https://numpy.org/devdocs/)
