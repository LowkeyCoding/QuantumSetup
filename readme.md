# Step 1: Setup the Backend

If you're using Windows, open Command Prompt (cmd.exe) or PowerShell. If you're using Unix-based systems like Linux or macOS, open Terminal.
Run the following command to install the ibm backend and other required dependencies:

## Windows
```
.venv\Scripts\activate
py -m pip install qiskit-ibm-runtime
```

## Unix

```
source .venv/bin/activate
python3 -m pip install qiskit-ibm-runtime
```

# Step 2: Get API Key from IBM Quantum Dashboard

Go to the IBM Quantum Dashboard website (https://quantum-computing.ibm.com/).
If you don't have an account, sign up for one. Otherwise, log in.
Once logged in, navigate to your dashboard. You'll find your API key there.
Copy your API key. This will be used to authenticate your access to IBM Quantum services.
![alt text](./images/api_key.png "Title")
Paste your API key into the `save_account.py` file then run it. It is important that you never run it on untrusted systems and NEVER publish the `save_account.py` with the api key in it. After running it once on a system the account will automatically be used when using the IBM backend.

With these two steps completed, you'll have the ibm backend installed and configured to use IBM Quantum hardware. You can then start experimenting with quantum circuits and running them on real quantum computers provided by IBM.
