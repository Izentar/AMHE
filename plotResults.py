import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from statistics import mean

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str, nargs=1, required=True, help="Input file")
	parser.add_argument('-o', type=str, nargs=1, required=False, help="Output processed csv file")
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

	resultsList = []

	name = 0
	for fun in ['elli','rosen','sphere','hyperelli','rastrigin','schwefel','bukin','schaffer']:
		for xstart in ['gauss', 'uniform', 'exp']:
			for dim in [5, 10]:
				for sigma in [0.05, 0.1, 0.3, 0.9]:
					dull = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'dull')]
					gauss = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'gauss')]
					uni = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'uniform')]
					exp = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'exp')]
					for eps in epsilon:
						resultsList.append([fun, xstart, dim, sigma, 'dull', eps, c(dull[str(eps)].values)])
					for eps in epsilon:
						resultsList.append([fun, xstart, dim, sigma, 'gauss', eps, c(gauss[str(eps)].values)])
					for eps in epsilon:
						resultsList.append([fun, xstart, dim, sigma, 'uniform', eps, c(uni[str(eps)].values)])
					for eps in epsilon:
						resultsList.append([fun, xstart, dim, sigma, 'exp', eps, c(exp[str(eps)].values)])
					x = range(1,len(epsilon)+1)
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
	results = pd.DataFrame(resultsList, columns = ['function', 'xstart', 'dim', 'sigma', 'estart', 'eps', 'val'])
	eps_count = len(epsilon)
	gauss_vals = [[] for i in range(len(epsilon))]
	uni_vals = [[] for i in range(len(epsilon))]
	exp_vals = [[] for i in range(len(epsilon))]
	currentFun = c(results.iloc[[0]]['function'].values)
	name = 0
	for i in range(0,(len(results)-4*eps_count), 1):
		dull_val = c(results.iloc[[i]]['val'].values)
		gauss_vals[i%eps_count].append(dull_val - c(results.iloc[[i+1*eps_count]]['val'].values))
		uni_vals[i%eps_count].append(dull_val - c(results.iloc[[i+2*eps_count]]['val'].values))
		exp_vals[i%eps_count].append(dull_val - c(results.iloc[[i+3*eps_count]]['val'].values))
		tempFun = c(results.iloc[[i]]['function'].values)
		if(currentFun is not tempFun):
			currentFun = tempFun
			x = range(1,len(epsilon)+1)
			gaussMeans = [mean(gauss_vals[i%eps_count]) for i in range(eps_count)]
			uniMeans = [mean(uni_vals[i%eps_count]) for i in range(eps_count)]
			expMeans = [mean(exp_vals[i%eps_count]) for i in range(eps_count)]
			plt.plot(x, gaussMeans, x, uniMeans, x, expMeans)
			plt.savefig(".\\imgs2\\" + str(name) + ".png")
			name = name + 1
			plt.clf()
			for i in range(eps_count):
				gauss_vals[i].clear()
				uni_vals[i].clear()
				exp_vals[i].clear()
	return(results)

if __name__ == '__main__':
	parser = createParser()
	args = parser.parse_args()
	results = plotGraphs(epsilon=args.eps, inputFile=args.i[0])
	if(args.o[0] != ''):
		results.to_csv(args.o[0], sep=';')
