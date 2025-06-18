from mpqp.execution import Result

# Retreive the state with the higher probability
def getBestGuess(res: Result) -> int:
  bestGuess = 0
  proba = 0
  for i in range(len(res.samples)):
    if (res.samples[i].probability > proba):
      bestGuess = res.samples[i].index
      proba = res.samples[i].probability
  return bestGuess