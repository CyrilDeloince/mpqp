from mpqp import QCircuit, Barrier
from mpqp.gates import H, X
from mpqp.measures import BasisMeasure
from mpqp.execution.algorithms.shor.modularExponentiationGate import CME
from mpqp.execution.algorithms.shor.qft import QFT

from math import floor, log

class ShorCircuit(QCircuit):

    def __init__(self, a: int, N: int):
        #Initialise the number of target qubits
        n = floor(log(N - 1, 2)) + 1

        #Circuit with 2*n controls and n targets
        super().__init__(2 * n + n)
        self._build(n, a, N)
    
    def _build(self, n: int, a: int, N: int):
        #Initialise the state of the targets
        self.add(X(2 * n))

        self.add(Barrier())
        
        for k in range(2 * n):
            self.add(H(k))
            self.add(CME(a, N, k, [k], list(range(2 * n, 3 * n))))
        
        self.add(Barrier())

        #QFT not QFT inverse (see MAGNIEZ Lecture Notes)
        self += QFT(range(2 * n)).inverse()

        self.add(BasisMeasure(list(range(2 * n)), shots=10000))