from cma import purecma as pcma
import cma
from random import gauss
import argparse
import csv
import pandas as pd
import os, sys
import numpy as np
import numpy.linalg as norm

def CountCMAESIterations(ftarget, maxLoops, initialSigma, m1_initEvolutionPath, initXFun, dim, testFunction):
	xstart = initXFun(dim)
	es1 = pcma.CMAES(xstart=xstart, sigma=initialSigma, ftarget=ftarget, m1_initEvolutionPath = m1_initEvolutionPath)
	iterCount = 0
	isBest = True
	while(not es1.stop()):
		points = es1.ask()
		es1.tell(points, [testFunction(x) for x in points])
		iterCount = iterCount + 1
		if(maxLoops < iterCount):
			isBest = False
			break
	return iterCount, isBest # aRT average running time

def AverageCountCMAESIterations(repeat, minimumTarget, maxLoops, epsilon, initialSigma, m1_initEvolutionPath, initXFun, dim, testFunction):
	iterCount = 0
	notReachedBest = 0
	ftarget = epsilon + minimumTarget
	for _ in range(0, repeat):
		ret = CountCMAESIterations(ftarget=ftarget, maxLoops=maxLoops, initialSigma=initialSigma,
			m1_initEvolutionPath=m1_initEvolutionPath, initXFun=initXFun, dim=dim, testFunction=testFunction)
		if(ret[1]):
			iterCount += ret[0]
		else: # does not reached best extremum
			notReachedBest += 1
			repeat -= 1
	if(repeat != 0):
		iterCount /= repeat # average
	return iterCount, notReachedBest

def RunTest(minimumTarget, testFun, repeat, initFunc, initXFun, initSigma, dim, maxLoops, epsilons: list):
	returnVals = []
	for eps in epsilons:
		ret = AverageCountCMAESIterations(repeat=repeat, epsilon=eps, minimumTarget=minimumTarget, maxLoops=maxLoops,
			initialSigma=initSigma, m1_initEvolutionPath=initFunc, initXFun=initXFun, dim=dim, testFunction=testFun)
		returnVals.append(tuple([ret[0], eps, ret[1]]))
	return returnVals
		

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-eps', type=float, nargs='+', required=False, default=[1, 0.01, 0.00001], help="Number of steps.")
	parser.add_argument('--sigma', type=float, nargs=1, required=True, help="Initial sigma value.")
	parser.add_argument('--dim', type=int, nargs=1, required=True, help="Number of dimensions.")
	parser.add_argument('--maxl', type=int, nargs=1, required=False, default=21000, help="Max number of loops / evolution steps.")

	parser.add_argument('--xstart', type=str, nargs=1, required=True, choices=['gauss'], help="Initial solution vector type.")
	parser.add_argument('--xsgm', type=float, nargs=1, required=False, default=None, help="xstart gauss mean.")
	parser.add_argument('--xsgstd', type=float, nargs=1, required=False, default=None , help="xstart gauss std.")

	parser.add_argument('--estart', type=str, nargs=1, required=True, choices=['dull', 'gauss'], help="Type of initialization of the evolution path p_sigma.")
	parser.add_argument('--esgm', type=float, nargs=1, required=False, default=None, help="estart gauss mean.")
	parser.add_argument('--esgstd', type=float, nargs=1, required=False, default=None, help="estart gauss std.")

	parser.add_argument('--testf', type=str, nargs=1, required=True, choices=['elli', 'rosen', 'test'], help="Type of test function.")
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
		Returns test function and target minimum value (the minimum of the test function that should be reached).
	"""
	if(ftype == 'elli'):
		return pcma.ff.elli, 0.0 
	elif(ftype == 'rosen'):
		return pcma.ff.rosen, 0.0 
	elif(ftype == 'test'):
		return cma.ff.cigar, 0.0 
	elif(ftype == 'test'):
		return cma.ff.cigar, 0.0 # warning, some functions in cma.ff use <list> ** 2 but this is invalid operation. It needs to be changed to for loop.
	else:
		raise Exception(f"Unknown parameter: {ftype}")

	#testFun = pcma.ff.sphere	# Min = 0 at x=(0,...,0)
	#RunTest(0)
	#testFun = cma.ff.rosen		# Min = 0 at x=(1,...,1)
	#RunTest(1)
	#testFun = pcma.ff.elli		# Min = 0 at x=(0,...,0)

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

	def getPos(columns, val):
		pos = 0
		for i, c in enumerate(list(columns)):
			if(c > str(val)):
				pos += 1
			else:
				break
		return pos
	def strMissReached(val):
		return str(val) + '_' + 'msreach'

	for result, step, missreached in returnVals:
		if(str(step) not in list(outdf.columns)):
			posStep = getPos(outdf.columns, step)
			outdf.insert(posStep, column = str(step), value='0')
			outdf.insert(posStep + 1, column = strMissReached(step), value='0')

		row[str(step)] = str(result)
		row[strMissReached(step)] = str(missreached)
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
	results = RunTest(minimumTarget=tmp[1], testFun=tmp[0], repeat=args.r[0], initFunc=getEstartFun(args.estart[0]), maxLoops=args.maxl,
		initXFun=getXstartFun(args.xstart[0], args), dim=args.dim[0], initSigma=args.sigma[0], epsilons=args.eps)
	saveInfo(args, results)
	cma.ff.cigar

