from cma import purecma as pcma

print("Standard init (ps = [0])")
es = pcma.CMAES(8 * [0.1], 0.5, randompsigma = False).optimize(pcma.ff.elli)
print('termination by', es.stop())
print('best f-value =', es.result[1])
print('best solution =', es.result[0])


print("Random init (ps = [Norm(0,1)])")
es = pcma.CMAES(8 * [0.1], 0.5, randompsigma = True).optimize(pcma.ff.elli)
print('termination by', es.stop())
print('best f-value =', es.result[1])
print('best solution =', es.result[0])
