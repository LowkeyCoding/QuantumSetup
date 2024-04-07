from qiskit_ibm_runtime import QiskitRuntimeService
# Do not under any circustances put the key on a public repository!
# Do not run this with your key on a untrusted machine as any user will be able to use your account henceforth!
QiskitRuntimeService.save_account(channel="ibm_quantum", token="IBM_QUANTUM_API_KEY_HERE")