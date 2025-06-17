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