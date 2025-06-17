import numpy as np

from math import gcd

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

# Euclide algorithm
def euclide(a, b):
  while b != 0:
    tmp = b
    b = a % b
    a = tmp
  return a

# Choose a random integer 'a' which is a factor of 'N'
def getFactor(N: int) -> int:
  a = np.random.randint(2, N)
  while euclide(a, N) != 1:
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

def convergents(a):
    """
    Donne la liste des convergents (p_i, q_i) à partir de la liste
    des quotients partiels a = [a0, a1, …].
    Cette implémentation gère automatiquement len(a)=1.
    """
    # initialisation selon la récurrence standard :
    # p_{-2}=0, p_{-1}=1 ; q_{-2}=1, q_{-1}=0
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0

    convergents = []
    for ai in a:
        p_i = ai * p_prev1 + p_prev2
        q_i = ai * q_prev1 + q_prev2

        convergents.append((p_i, q_i))

        # décale les indices pour l’itération suivante
        p_prev2, p_prev1 = p_prev1, p_i
        q_prev2, q_prev1 = q_prev1, q_i

    return convergents

# Compute the factores of N
def compute_factors(a, convergents, N):
  """
    convergents : liste de tuples (p_k, q_k)
    a, N        : paramètres de l'algo de Shor
    Retour :
      (p1, p2)   si deux facteurs non triviaux de N sont trouvés,
      (None, None) sinon.
    """
  for _, r in convergents:
        # 1) Vérifier la période candidate
        if pow(a, r, N) != 1:
            continue
        # 2) r doit être pair
        if r % 2 == 1:
            continue
        # 3) Calculer a^(r/2) mod N
        x = pow(a, r//2, N)
        # 4) Exclure le cas x ≡ −1 mod N
        if x == N-1:
            continue

        # 5) Extraire les deux gcd
        p1 = math.gcd(x-1, N)
        p2 = math.gcd(x+1, N)

        # 6) S’assurer d’avoir deux facteurs non triviaux
        if 1 < p1 < N and 1 < p2 < N:
            return p1, p2
        # (si un seul est non trivial, c'est déjà surprenant, on continue)
    # Aucun r valide n'a donné les deux facteurs
  return None, None