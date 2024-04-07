# Step 1: Setup Environment

If you're using Windows, open Command Prompt (cmd.exe) or PowerShell. If you're using Unix-based systems like Linux or macOS, open Terminal.
Run the following command to install Qiskit and other required dependencies:

## Windows
```
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

## Unix

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```