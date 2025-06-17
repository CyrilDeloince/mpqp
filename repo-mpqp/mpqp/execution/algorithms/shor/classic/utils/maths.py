import numpy as np

# Fast exponantiation modulo m
def fast_expo(a: int, n: int, m: int = None) -> int:
  if n == 0:
    return 1
  b = (a*a)
  if m != None:
    b = b % m
  if n % 2 == 0:
    return fast_expo(b, n // 2, m)
  return a * fast_expo(b, n // 2, m)

# Choose a random integer 'a' which is a factor of 'N'
def getFactor(N: int) -> int:
  a = np.random.randint(2, N)
  while euclide(a, N) == 1:
    a = np.random.randint(2, N)
  return a

# using continued fractions estimate the period r
def continued_fraction(p, q):
    a = []
    while q:
        a.append(p // q)
        p, q = q, p % q
    return a

# verify whether a**r mod N = 1.
def verify_period(a, r, N):
  return (a**r) % N == 1

# Compute the factores of N
def compute_factors(a, r, N):
  if r % 2 == 0 and fast_expo(a, r // 2, N) != -1 % N:
    p = fast_expo(a, r // 2)
    return euclide(p-1, N), euclide(p+1, N)