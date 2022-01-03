from cma import purecma as pcma
import cma
from colorama import init
from colorama import Fore, Back, Style
init()

numSamples = 25
initSigma = 0.5
initX = 8 * [0.1]
stdDev = 1
#testFun = pcma.ff.elli
#testFun = pcma.ff.sphere
testFun = cma.ff.rosen

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

targetMin = 1
while targetMin > 0.001:
	nonRandomIters = AverageCountCMAESIterations(numSamples, targetMin, initSigma, False, stdDev, initX, testFun)
	randomIters = AverageCountCMAESIterations(numSamples, targetMin, initSigma, True, stdDev, initX, testFun)
	if(nonRandomIters < randomIters):
		print(Fore.RED + str(nonRandomIters) + " < " + str(randomIters) + " [Non-random vs random] [targetMin:" + str(targetMin) + "]" + Style.RESET_ALL)
	else:
		print(Fore.GREEN + str(nonRandomIters) + " > " + str(randomIters) + " [Non-random vs random] [targetMin:" + str(targetMin) + "]" + Style.RESET_ALL)
	targetMin = targetMin / 2
