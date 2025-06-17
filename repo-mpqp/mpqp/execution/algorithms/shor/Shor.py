from mpqp.execution.algorithms.shor.classic.utils import maths, preprocessing
from mpqp.execution.algorithms.shor.quantum.shorCircuit import ShorCircuit
from mpqp.execution import run, IBMDevice

from math import floor, log

def shor_algorithm(N: int) -> tuple[int, int]:
    """
    Shor's algorithm to find the prime factors of N.
    
    Args:
        N (int): The integer to factor.
        
    Returns:
        tuple[int, int]: The two prime factors of N.
    """
    
    # Check if N has small prime divisors (like 3, 5, 7). If yes, the problem is solved.
    # for small_prime in [2, 3, 5, 7]:
    #     if N % small_prime == 0:
    #         return small_prime, N // small_prime
        
    while True:
        # Step 1: Choose a random integer 'a' which is a factor of 'N'
        a = maths.getFactor(N)

        print("a = " + str(a) + ", N = " + str(N))
        
        c = preprocessing.getBestGuess(run(ShorCircuit(a, N), IBMDevice.AER_SIMULATOR))
        print("c = ", c)
        n = floor(log(N - 1, 2)) + 1
        q = 2 * n

        # Step 2: Find the period 'r' using continued fractions
        r = maths.continued_fraction(c, q)
        print("r = ", r)
        convergents = maths.convergents(r)
        print("convergents = ", convergents)
        
        # Step 3: Compute the factors of N
        factors = maths.compute_factors(a, convergents, N)
        if factors == (None, None):
            continue
        else:
            return factors