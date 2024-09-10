# Step 1: Setup the backend

If you're using Windows, open Command Prompt (cmd.exe) or PowerShell. If you're using Unix-based systems like Linux or macOS, open Terminal.
Run the following command to install Qiskit and other required dependencies:

## Windows
```
.venv\Scripts\activate
pip install qiskit-braket-provider boto3 amazon-braket-sdk
```

## Unix/Mac

```
source .venv/bin/activate
pip install qiskit-braket-provider boto3 amazon-braket-sdk
```

Unix users may need to install `PyQt5` if they dont use Jupyter to show plots
```
pip install PyQt5
```

# Step 2: Creating Access key
First, click on your username (1), then click on Security credentials (2). 
![Locate Credentials section](./images/amazon%20menu.PNG)

Next, click on `Create new access key` (3) and follow the instructions. You'll need both the access key and the Secret access key for the next step.

![Create new key](./images/add_new_bracket.png)

# step 3: Login with Python
Setup the environment file `.env` by adding the lines 
```bash
aws_access = Your Access key
aws_secret = Your Secret access key
aws_region = Your Region
```
Then the minial login script below should provide an aws session used to access amazon bracket backends. 
```python
from braket.aws.aws_session import AwsSession 
import boto3
import os 
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

boto_session = boto3.Session(
    aws_access_key_id=os.environ['aws_access'],
    aws_secret_access_key=os.environ['aws_secret'],
    region_name=os.environ['aws_region'],
)
session = AwsSession(boto_session)
``` 

# Step 4: Listing accesible backends.
To list the currently available backends add the snippet below to the login example.
```python 
print("This workspace's targets:")
for backend in provider.backends(aws_session = session):
    print("- " + backend.name)
```
This should produce a list like the one below.
```
This workspace's targets:
- Aria 1
- Aria 2
- Aspen-M-3
- Forte 1
- Harmony
- Lucy
- SV1
- TN1
- dm1
```

# Step 5: Running a quantum circuit.
To run a quantum circuit a specific backend has to be chosen from the list of currently available ones. This is done by getting the backend from the provider `provider.get_backend("SV1", aws_session = session)` as seen in the example below. It is important to always test programs on the simulator first and, in general, limit the usage of real hardware as the cost adds up extremely quickly.
```python
from braket.aws.aws_session import AwsSession 
import boto3
import os 
from dotenv import load_dotenv

from qiskit import *
import numpy as np
from qiskit_braket_provider import BraketProvider
from qiskit.visualization import plot_histogram
from matplotlib import pyplot

# Load environment variables 
load_dotenv()

boto_session = boto3.Session(
    aws_access_key_id=os.environ['aws_access'],
    aws_secret_access_key=os.environ['aws_secret'],
    region_name=os.environ['aws_region'],
)
session = AwsSession(boto_session)

provider = BraketProvider()

backend = provider.get_backend("SV1", aws_session = session)

circ = QuantumCircuit(3)

circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)

circ.measure_all()
circ.draw('mpl')

# Transpile circuit to work with the current backend.
qc_compiled = transpile(circ, backend)
# Run the job
job_sim = backend.run(qc_compiled, shots=1024)
# Get the result
result_sim = job_sim.result()
counts = result_sim.get_counts()
# Plot the result
plot_histogram(counts)
pyplot.show()
```
