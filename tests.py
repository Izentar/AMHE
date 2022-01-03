from cma import purecma as pcma
import cma
from colorama import init
from colorama import Fore, Back, Style
from random import gauss
init()

def CountCMAESIterations(targetMinimumValue, initialSigma, randompsigma, standardDeviation, initialXValues, testFunction):
	es1 = pcma.CMAES(initialXValues, initialSigma, ftarget=targetMinimumValue, randompsigma = randompsigma, randompgaussstddev = standardDeviation)
	iterCount = 0
	while(not es1.stop()):
		solutions = es1.ask()
		es1.tell(solutions, [testFunction(x) for x in solutions])
		iterCount = iterCount + 1
	return iterCount

def AverageCountCMAESIterations(samplesCount, targetMinimumValue, initialSigma, randompsigma, standardDeviation, initialXValues, testFunction):
	iterCount = 0
	for i in range(0, samplesCount):
		iterCount = iterCount + CountCMAESIterations(targetMinimumValue, initialSigma, randompsigma, standardDeviation, initialXValues, testFunction)
	iterCount = iterCount / samplesCount
	return iterCount

def RunTest(targetMin, steps = []):
	if(len(steps) <= 0):
		steps = [1.0, 0.5, 0.25, 0.1, 0.01, 0.001, 0.0001, 0.00001]
	while len(steps) > 0:
		nonRandomIters = AverageCountCMAESIterations(numSamples, targetMin + steps[0], initSigma, False, stdDev, initX, testFun)
		randomIters = AverageCountCMAESIterations(numSamples, targetMin + steps[0], initSigma, True, stdDev, initX, testFun)
		if(nonRandomIters < randomIters):
			print(Fore.RED + str(nonRandomIters) + " < " + str(randomIters) + " [Non-random vs random] [targetMin:" + str(targetMin + steps[0]) + "]" + Style.RESET_ALL)
		else:
			print(Fore.GREEN + str(nonRandomIters) + " > " + str(randomIters) + " [Non-random vs random] [targetMin:" + str(targetMin + steps[0]) + "]" + Style.RESET_ALL)
		steps.pop(0)


initSigma = 0.3
initX = [gauss(0,1) for _ in range(0,8)]
stdDev = 1

numSamples = 100

#testFun = pcma.ff.sphere	# Min = 0 at x=(0,...,0)
#RunTest(0)
#testFun = cma.ff.rosen		# Min = 0 at x=(1,...,1)
#RunTest(1)
testFun = pcma.ff.elli		# Min = 0 at x=(0,...,0)
RunTest(0)
