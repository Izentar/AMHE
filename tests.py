from cma import purecma as pcma

def TestCMAES(numberOfIterations, targetMinimumValue, initialSigma, standardDeviation, initialXValues, testFunction):
    results = []
    for it in range(0,numberOfIterations):
        es1 = pcma.CMAES(initialXValues, initialSigma, ftarget=targetMinimumValue, randompsigma = False, randompgaussstddev = standardDeviation).optimize(testFunction, verb_disp=0)
        es2 = pcma.CMAES(initialXValues, initialSigma, ftarget=targetMinimumValue, randompsigma = True, randompgaussstddev = standardDeviation).optimize(testFunction, verb_disp=0)
        results.append(es1.result[1] - es2.result[1])
    return results

def EvalCMAESTest(results, endMsg = ""):
    numOfBetterSolutions = sum([1 if x>0 else 0 for x in results])
    print(f'Got {numOfBetterSolutions:.0f}/{len(results):.0f} solutions better than zero init' + endMsg)
    return numOfBetterSolutions

numIter = 100
targetMin = 0.1
initSigma = 0.5
initX = 8 * [0.1]
stdDev = 10
testFun = pcma.ff.elli
EvalCMAESTest(TestCMAES(numIter, targetMin, initSigma, stdDev, initX, testFun), " for target = 0.1")
EvalCMAESTest(TestCMAES(numIter, 0.05, initSigma, stdDev, initX, testFun), " for target = 0.05")
EvalCMAESTest(TestCMAES(numIter, 0.01, initSigma, stdDev, initX, testFun), " for target = 0.01")
EvalCMAESTest(TestCMAES(numIter, 0.001, initSigma, stdDev, initX, testFun), " for target = 0.001")
EvalCMAESTest(TestCMAES(numIter, 0.0, initSigma, stdDev, initX, testFun), " for target = 0.0")
