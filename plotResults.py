import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str, nargs=1, required=True, help="Input file")
	parser.add_argument('-eps', type=float, nargs='+', required=False, default=[1, 0.01, 0.00001], help="Number of steps used in experiment")
	return parser

def checkEpsInLine(epsilon, line):
	if(line):
		for eps in epsilon:
			if (('sigma=[' + str(eps) + ']') in line):
				return eps
	return None

def c(array):
	try:
		return(array[0])
	except IndexError as e:
		return(0)

def plotGraphs(epsilon, inputFile):
	data = pd.read_csv (inputFile, delimiter=';')
	columnHeaders = ['args','input','function']
	for eps in epsilon:
		columnHeaders.append(str(eps))
		columnHeaders.append((str(eps) + "_msreach"))
	df = pd.DataFrame(data, columns = columnHeaders)
	df['sigma'] = [0.05 if ('sigma=[0.05]' in x) else (0.1 if ('sigma=[0.1]' in x) else 0.3 if ('sigma=[0.3]' in x) else 0.9) for x in df['args']]
	df['dim'] = [5 if ('dim=[5]' in x) else 10 for x in df['args']]
	df['estart'] = ['dull' if ('estart=[\'dull\']' in x) else ('gauss' if ('estart=[\'gauss\']' in x) else ('uniform' if ('estart=[\'uniform\']' in x) else 'exp')) for x in df['args']]
	df['xstart'] = ['gauss' if ('xstart=[\'gauss\']' in x) else ('uniform' if ('xstart=[\'uniform\']' in x) else 'exp') for x in df['args']]

	name = 0
	for fun in ['elli','rosen','sphere','hyperelli','rastrigin','schwefel','bukin','schaffer']:
		for xstart in ['gauss', 'uniform', 'exp']:
			for dim in [5, 10]:
				for sigma in [0.05, 0.1, 0.3, 0.9]:
					dull = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'dull')]
					gauss = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'gauss')]
					uni = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'uniform')]
					exp = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'exp')]
					x = range(1,len(epsilon)+1)
					#if(len(gauss) > 0):
					plt.plot(x, [c(dull[str(eps)].values) for eps in epsilon], x, [c(gauss[str(eps)].values) for eps in epsilon], x, [c(uni[str(eps)].values) for eps in epsilon], x, [c(exp[str(eps)].values) for eps in epsilon])
					plt.xlabel('epsilon')
					plt.ylabel('Liczba iteracji')
					plt.grid(True)
					plt.title(str(fun) + ", sigma=" + str(sigma) + ", dim=" + str(dim) + ", xstart=" + str(xstart))
					plt.xticks(x,epsilon)
					plt.autoscale(enable=True, axis='y')
					plt.legend(['dull', 'gauss', 'uniform', 'exp'])
					plt.savefig(".\\imgs\\" + str(name) + ".png")
					plt.clf()
					name = name + 1

if __name__ == '__main__':
	parser = createParser()
	args = parser.parse_args()
	plotGraphs(epsilon=args.eps, inputFile=args.i[0])
