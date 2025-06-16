from mpqp import QCircuit, Barrier
from mpqp.gates import H, CRk, SWAP

from math import floor

class QFT(QCircuit):

    #The qubits should be consecutive so targets is of type range
    #If range does not start from 0, we add the first qubits
    def __init__(self, targets: range):
        super().__init__(targets[0] + len(targets))
        self.targets = targets
        self._build()
    
    def _build(self):
        for j in range(len(self.targets)):
            self.add(H(self.targets[j]))
            self.add([CRk(i + 1, self.targets[i], self.targets[j]) for i in range(j + 1, len(self.targets))])
            self.add(Barrier())
        self.add([SWAP(self.targets[i], self.targets[len(self.targets)-1-i]) for i in range(int(floor(len(self.targets) / 2)))])