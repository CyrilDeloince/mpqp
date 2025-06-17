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

def convergents(a):
    """Retourne la liste des (p_k, q_k) pour la CF donnée par a = [a0,a1,...]."""
    P = [a[0], a[0]*a[1] + 1]
    Q = [1, a[1]]
    conv = [(P[0],Q[0]), (P[1],Q[1])]
    for i in range(2, len(a)):
        Pk = a[i]*P[i-1] + P[i-2]
        Qk = a[i]*Q[i-1] + Q[i-2]
        P.append(Pk)
        Q.append(Qk)
        conv.append((Pk, Qk))
    return conv

# Compute the factores of N
def compute_factors(a, convergents, N):
  """
    convergents : liste de tuples (p_k, q_k)
    a, N        : comme dans l'algo de Shor
    """
  for _, r in convergents:
        # 1) test de la période
        if pow(a, r, N) != 1:
            continue
        # 2) r doit être pair
        if r % 2 == 1:
            continue
        # 3) calcul de a^(r/2) mod N
        x = pow(a, r//2, N)
        # 4) éviter le -1 trivial
        if x == N-1:
            continue
        # 5) extraire un facteur
        p1 = math.gcd(x-1, N)
        if 1 < p1 < N:
            return p1
        p2 = math.gcd(x+1, N)
        if 1 < p2 < N:
            return p2
    # si on n’a rien trouvé, essayer un autre 'a' ou relancer la mesure
  return None