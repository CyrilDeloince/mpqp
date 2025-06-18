from mpqp import QCircuit, Barrier
from mpqp.gates import H, X
from mpqp.measures import BasisMeasure
from mpqp.execution.algorithms.shor.quantum.modularExponentiationGate import CME
from mpqp.execution.algorithms.shor.quantum.qft import QFT

from mpqp.core.languages import Language
from typing import TYPE_CHECKING

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
        self += QFT(range(2 * n))

        self.add(BasisMeasure(list(range(2 * n)), shots=1))
    
    def __str__(self) -> str:
        # n = self.nb_qubits // 3
        # print(2**n)
        # qiskit_circ = QCircuit(2 * n + n)
        # qiskit_circ.add(X(2 * n))
        # qiskit_circ.add(Barrier())

        qiskit_circ = self.to_other_language(Language.QISKIT, printing=True)
        if TYPE_CHECKING:
            from qiskit import QuantumCircuit

            assert isinstance(qiskit_circ, QuantumCircuit)
        output = str(qiskit_circ.draw(output="text", fold=0))
        if len(self.noises) != 0:
            noises = "\n    ".join(str(noise) for noise in self.noises)
            output += f"\nNoiseModel:\n    {noises}"
        return output