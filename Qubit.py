from qiskit import QuantumCircuit
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import XGate
from qiskit.providers import DWaveProvider
import math

# Set the bounds
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663

# Define the oracle to check if a given value of m satisfies (a*b) % m == x
def oracle(m, x):
    oracle_qc = QuantumCircuit(1)
    target = QuantumCircuit(1)
    target.x(0)
    oracle_qc.append(target.to_instruction(), [i for i in range(1)])
    for i in range(1):
        oracle_qc.append(XGate().power(int(math.pow(2, i))), [i])
    for i in range(0, 1):
        oracle_qc.cx(i, 0)
    oracle_qc.x(0)
    oracle_qc.append(target.to_instruction().inverse(), [i for i in range(1)])
    return oracle_qc.to_gate()

# Define the problem
def amplification_problem(m):
    return AmplificationProblem(oracle(m, 55066263021366149949932944254155024514247492615142308993872983365411851378577), is_good_state)

# Define the good states
def is_good_state(x):
    a = 115792089237316195423570985008687907852837564279074904382605163141518161494336
    b = 40360748372915677739060455046407153445907911874643188801639465548522
    return ((a * b) % m) == 55066263021366149949932944254155024514247492615142308993872983365411851378577

# Find m using Grover's algorithm
for m in range(N, P+1):
    print("Checking m = " + str(m))
    problem = amplification_problem(m)
    dwave_provider = DWaveProvider(token='DEV-b5d2e8fdc8a07946bf396c0fb686f3873fddfeb9', endpoint='DW_2000Q_6')
    quantum_instance = QuantumInstance(dwave_provider.get_backend('DW_2000Q_6'), shots=1000)
    grover = Grover(quantum_instance=quantum_instance)
    result = grover.amplify(problem, max_iterations=2)
    if result.top_measurement in problem.good_state_numbers:
        print("Found m = " + str(m))
        break
