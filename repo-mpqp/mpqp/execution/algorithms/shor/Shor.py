from classic.utils import maths

def shor_algorithm(N: int) -> tuple[int, int]:
    """
    Shor's algorithm to find the prime factors of N.
    
    Args:
        N (int): The integer to factor.
        
    Returns:
        tuple[int, int]: The two prime factors of N.
    """
    
    # If N is even, then 2 is a factor
    if N % 2 == 0:
        return 2, N // 2
    
    # Check if N has small prime divisors (like 3, 5, 7). If yes, the problem is solved.
    for small_prime in [3, 5, 7]:
        if N % small_prime == 0:
            return small_prime, N // small_prime
        
    while True:
        # Step 1: Choose a random integer 'a' which is a factor of 'N'
        a = maths.getFactor(N)
        
        # Step 2: Find the period 'r' using continued fractions
        r = maths.continued_fraction(a, N)
        convergents = maths.convergents(r)
        
        # Step 3: Compute the factors of N
        factors = maths.compute_factors(a, convergents, N)
        if factors == None:
            continue
        else:
            return factors
        
print(shor_algorithm(15))