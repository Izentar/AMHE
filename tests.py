from cma import purecma as pcma
import cma
from random import gauss
import argparse
import csv
import pandas as pd
import os, sys

def CountCMAESIterations(targetMinimumValue, initialSigma, m1_initEvolutionPath, initXFun, dim, testFunction):
	xstart = initXFun(dim)
	es1 = pcma.CMAES(xstart=xstart, sigma=initialSigma, ftarget=targetMinimumValue, m1_initEvolutionPath = m1_initEvolutionPath)
	iterCount = 0
	while(not es1.stop()):
		solutions = es1.ask()
		es1.tell(solutions, [testFunction(x) for x in solutions])
		iterCount = iterCount + 1
	return iterCount # aRT average running time

def AverageCountCMAESIterations(repeat, targetMinimumValue, initialSigma, m1_initEvolutionPath, initXFun, dim, testFunction):
	iterCount = 0
	for _ in range(0, repeat):
		iterCount += CountCMAESIterations(targetMinimumValue=targetMinimumValue, initialSigma=initialSigma, 
			m1_initEvolutionPath=m1_initEvolutionPath, initXFun=initXFun, dim=dim, testFunction=testFunction)
	iterCount /= repeat # average
	return iterCount

def RunTest(targetMin, testFun, repeat, initFunc, initXFun, initSigma, dim, steps: list = None):
	# Nie można dać steps = [], bo to robi globalną zmienną
	if(steps is None):
		steps = [1.0, 0.5, 0.25, 0.1, 0.01, 0.001, 0.0001, 0.00001]
	returnVals = []
	for st in steps:
		nonRandomIters = AverageCountCMAESIterations(repeat=repeat, targetMinimumValue=targetMin + st, initialSigma=initSigma, m1_initEvolutionPath=initFunc, initXFun=initXFun, dim=dim, testFunction=testFun)
		returnVals.append(tuple([nonRandomIters, st]))
	return returnVals
		

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', type=float, nargs='+', required=False, default=[1.0, 0.5, 0.25, 0.1, 0.01, 0.001, 0.0001, 0.00001], help="Number of steps.")
	parser.add_argument('--sigma', type=float, nargs=1, required=True, help="Initial sigma value.")
	parser.add_argument('--dim', type=int, nargs=1, required=True, help="Number of dimensions.")

	parser.add_argument('--xstart', type=str, nargs=1, required=True, choices=['gauss'], help="Initial solution vector type.")
	parser.add_argument('--xsgm', type=float, nargs=1, required=False, default=None, help="xstart gauss mean.")
	parser.add_argument('--xsgstd', type=float, nargs=1, required=False, default=None , help="xstart gauss std.")

	parser.add_argument('--estart', type=str, nargs=1, required=True, choices=['dull', 'gauss'], help="Type of initialization of the evolution path p_sigma.")
	parser.add_argument('--esgm', type=float, nargs=1, required=False, default=None, help="estart gauss mean.")
	parser.add_argument('--esgstd', type=float, nargs=1, required=False, default=None, help="estart gauss std.")

	parser.add_argument('--testf', type=str, nargs=1, required=True, choices=['elli', 'rosen', 'sphere', 'hyperelli', 'rastrigin', 'schwefel', 'bukin', 'schaffer'], help="Type of test function.")
	parser.add_argument('-r', type=int, nargs=1, required=True, help="Number of repetition of the experiment.")
	parser.add_argument('-o', type=str, nargs=1, required=True, help="Output file")

	
	return parser

def getXstartFun(ftype: str, args):
	if(ftype == 'gauss'):
		if(args.xsgm is None or args.xsgstd is None):
			raise Exception("Argument 'xsgm' or 'xsgstd' not set.")
		return lambda N: [gauss(args.xsgm[0], args.xsgstd[0]) for _ in range(N)]
	else:
		raise Exception(f"Unknown parameter: {ftype}")

def getEstartFun(ftype: str):
	if(ftype == 'dull'):
		return None
	elif(ftype == 'gauss'):
		return lambda N : [gauss(0,1) for _ in range(0,N)]
	else:
		raise Exception(f"Unknown parameter: {ftype}")

def getTestFunction(ftype: str):
	"""
		Returns test function and target minimum value (the value of global minimum).
	"""
	if(ftype == 'elli'):
		return cma.ff.elli, 0.0    # Default is  elli(self, x, rot=0, xoffset=0, cond=1e6, actuator_noise=0.0, both=False)
	if(ftype == 'rosen'):
		return cma.ff.rosen, 0.0
	if(ftype == 'sphere'):
		return pcma.ff.sphere, 0.0
	if(ftype == 'hyperelli'):
		return cma.ff.hyperelli, 0.0
	if(ftype == 'rastrigin'):
		return cma.ff.rastrigin, 0.0
	if(ftype == 'schwefel'):
		return cma.ff.schwefelmult, 0.0
	# Below functions in default variants are meant for 2-dimensional problems,
	# these versions however are simplistically generalized to d-dim
	if(ftype == 'bukin'):
		return pcma.ff.bukin, 0.0
	if(ftype == 'schaffer'):
		return pcma.ff.schaffer, 0.0
	else:
		raise Exception(f"Unknown parameter: {ftype}")

def saveInfo(args, returnVals, verbose = True):
	if(not os.path.isfile(args.o[0])):
		df = pd.DataFrame(columns=['args', 'input', 'function'])
		df.to_csv(args.o[0], index=False, header=True, sep=';', index_label=False)

	outdf = pd.read_csv(args.o[0], sep=';', header=0, index_col=False)
	arguments = str(args)
	arg = str()
	for i in list(sys.argv):
		arg += str(i) + ' '
	row = {
		'function': args.testf[0],
		'input': arg,
		'args': str(args)
	}

	for result, step in returnVals:
		if(str(step) not in list(outdf.columns)):
			pos = 0
			for i, c in enumerate(list(outdf.columns)):
				if(c > str(step)):
					pos += 1
				else:
					break
			outdf.insert(pos, column = str(step), value='0')
		row[str(step)] = str(result)
	newrow = pd.DataFrame(row, index=[-1])

	outdf = outdf.append(newrow, ignore_index=True)
	outdf.reindex(fill_value = '0')
	outdf.to_csv(args.o[0], index=False, header=True, sep=';', index_label=False)
	if(verbose):
		print(str(args))
		print(arg)
		print(str(outdf))

if __name__ == '__main__':
	parser = createParser()
	args = parser.parse_args()

	tmp = getTestFunction(args.testf[0])
	results = RunTest(targetMin=tmp[1], testFun=tmp[0], repeat=args.r[0], initFunc=getEstartFun(args.estart[0]), 
		initXFun=getXstartFun(args.xstart[0], args), dim=args.dim[0], initSigma=args.sigma[0])
	saveInfo(args, results)

