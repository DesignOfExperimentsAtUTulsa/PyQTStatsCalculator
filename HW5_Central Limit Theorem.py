
"""
@author: Anvar Akhiiartdinov
HW: Simulation of Central Limit Theorem

"""
import random
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

m = 10000
n = 100 #2,10,100
sum_ar = np.zeros(m)
y = np.zeros((n,m))

for i in range(m):
    sum_ar[i] = 0
    for j in range(n):
        y[j][i] = random.random()
        sum_ar[i] += y[j][i]

plt.hist(sum_ar,bins=20*n,normed=True, label='CLT')

mu = np.mean(sum_ar)
sigma = np.std(sum_ar)
x = np.linspace(mu-3*sigma,mu+3*sigma, 100)
y_norm = mlab.normpdf(x, mu, sigma)
plt.plot(x,y_norm,'k--',label='Normal')
plt.legend(loc=0,shadow=True)



  
    
        



