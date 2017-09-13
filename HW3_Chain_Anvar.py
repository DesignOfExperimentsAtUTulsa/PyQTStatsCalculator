#developed by Anvar Akhiiartdinov

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

link = np.arange(1,31)
p_fr_num = 0.05
print(link[1])

p_ind = (1-p_fr_num)**link
plt.plot(link,p_ind, label="Ind", color='gray',linestyle=':')

dep_func = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
dep_func_str = str(dep_func)

lines = ["-k","--k","-.k",":k"]
linecycler = cycle(lines)

p_dep = np.zeros((len(dep_func),len(link)))
for i in range(len(dep_func)):
    for j in range(len(link)):
        p_dep[i,j] = dep_func[i]**(link[j]-1) * (1-p_fr_num)
    plt.plot(link,p_dep[i,:], next(linecycler), label="dep degree {:1.1f}".format(dep_func[i]))
            
plt.xlabel("Number of Links")
plt.ylabel("Probability of Failure")
plt.grid()
plt.legend(loc=0,shadow=False)
plt.show()
        




    
        

