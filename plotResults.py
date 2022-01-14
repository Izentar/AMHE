import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv (r'out.csv', delimiter=';')
df = pd.DataFrame(data, columns= ['args','input','function','1e-05','1e-05_msreach','1','1_msreach','0.01','0.01_msreach'])
df['sigma'] = [0.05 if ('sigma=[0.05]' in x) else (0.1 if ('sigma=[0.1]' in x) else 0.3 if ('sigma=[0.3]' in x) else 0.9) for x in df['args']]
df['dim'] = [5 if ('dim=[5]' in x) else 10 for x in df['args']]
df['estart'] = ['dull' if ('estart=[\'dull\']' in x) else 'gauss' for x in df['args']]
df['xstart'] = ['gauss' if ('xstart=[\'gauss\']' in x) else ('uniform' if ('xstart=[\'uniform\']' in x) else 'exp') for x in df['args']]

name = 0
for fun in ['elli','rosen','sphere','hyperelli','rastrigin','schwefel','bukin','schaffer']:
	for sigma in [0.05, 0.1, 0.3, 0.9]:
		for dim in [5, 10]:
			for xstart in ['gauss', 'uniform', 'exp']:
				dull = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'dull')]
				gauss = df[(df['sigma'] == sigma) & (df['dim'] == dim) & (df['xstart'] == xstart) & (df['function'] == fun) & (df['estart'] == 'gauss')]
				plt.plot([1, 2, 3], [dull['1'], dull['0.01'], dull['1e-05']], [1, 2, 3], [gauss['1'], gauss['0.01'], gauss['1e-05']])
				plt.xlabel('epsilon')
				plt.ylabel('Liczba iteracji')
				plt.grid(True)
				plt.title('Test title')
				plt.xticks([1, 2, 3],[1, 0.01, 1e-05])
				plt.ylim([0, max(max(dull['1e-05']), max(gauss['1e-05']))])
				plt.legend(['dull', 'gauss'])
                #plt.show()
				plt.savefig(".\\imgs\\" + str(name) + ".png")
				name = name + 1
				plt.clf()
