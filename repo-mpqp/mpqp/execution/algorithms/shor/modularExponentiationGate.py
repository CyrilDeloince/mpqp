from typing import Union
from mpqp.gates import CustomGate, UnitaryMatrix
from mpqp.core.instruction.gates.custom_controlled_gate import CustomControlledGate
from mpqp.tools import fast_expo

import numpy as np

from math import floor, log

class ME(CustomGate):

    def __init__(self, a: int, N: int, k: int, targets: list[int]):
        #Initialise n
        n = floor(log(N - 1, 2)) + 1
        assert len(targets) == n

        #Initialise b = a^(2^k) mod N
        b = fast_expo(a, 2**k, N)

        #Initialise the matrix with zeros and dimension 2^n * 2^n
        d = fast_expo(2, n)
        U = np.zeros((d, d))

        #By definition, U[j> = [b * j mod N> for j in {0, ..., N - 1}
        for j in range(N):
            U[(b * j) % N][j] = 1

        #Then the operator is completed to be applied on all integers from 0 to 2 ** n
        #Nothing is done for j in {N, ..., 2**n}
        for j in range(N, 2**n):
            U[j][j] = 1

        #U is necessarily unitary as b is inversible in Zn
        super().__init__(UnitaryMatrix(U), targets, 'a^(2^' + str(k) + ') mod N')

class CME(CustomControlledGate):
   
   def __init__(self, a: int, N: int, k: int, controls: list[int], targets: list[int]):
      super().__init__(controls, ME(a, N, k, targets))