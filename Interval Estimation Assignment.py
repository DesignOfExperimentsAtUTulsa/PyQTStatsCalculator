# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 09:31:13 2017

@author: redwi
"""

from scipy import stats
import numpy as np
import statistics
import random
import matplotlib.pyplot as plt
input_data = [0.763, 0.720, 0.751, 0.743]

#initial Stats Values
count_value = len(input_data)
DOF = count_value - 1
mean_value = np.mean(input_data)            
stdDev_value = statistics.stdev(input_data)
stdError_value = stats.sem(input_data)
var_value = statistics.variance(input_data)

# Only 1 or 2 will allow the program to go further
#Single or Double tail
tailsSting = input("Is this single (1) or two Tailed (2) \n ---->")
tails = int(tailsSting)
#tails = 2

while tails > 2:
    tailsSting = input("Is this single (1) or two Tailed (2) \n ---->")
    tails = int(tailsSting)
#Second Set of statistics T values
SigString = input("Input the Significance Percentage \n----->")
Sig = int(SigString)
alpha = 1-Sig/100
print("Please wait while the program runs")
tDist = stats.t.ppf(1-alpha/tails, count_value)
low_mean = mean_value - stdError_value*tDist
high_mean =  mean_value + stdError_value*tDist

chiSqrd = stats.chi2.ppf(alpha, count_value -1)
max_var = (count_value-1) * var_value/chiSqrd
max_std = (np.sqrt(max_var))


#Monty Carlo method
pdf = []
a = 10000
for i in range (a):

    pdf.append(mean_value + stats.t.ppf(random.random(), count_value)*stdError_value
       + stats.t.ppf(random.random(), count_value -1) * 
       np.sqrt(((count_value-1)*var_value)/stats.chi2.ppf(random.random(), count_value-1)))
    i = i+1
pdf.sort()

x = []
for n in range(a):
    x.append(n/a)
lower_limit_float = (alpha/2)*a
upper_limit_float = (1-alpha/2)*a   

#change float to int for number retrieval in pdf list
lower_limit = int(lower_limit_float)
upper_limit = int(upper_limit_float)


#plotting

#print(pdf[upper_limit])    
plt.scatter(pdf, x, s=12)
plt.ylabel('CDF')
plt.xlabel('Variable')

norm_low = stats.norm.ppf(alpha/2, mean_value, stdDev_value)
norm_high = stats.norm.ppf(1-alpha/2, mean_value, stdDev_value)


#Differences in the norm and bootstrap bounds
upper_diff = abs(norm_high - pdf[upper_limit])
lower_diff = abs(norm_low - pdf[lower_limit])
#Check Values against Excel sheet


print("\nSummary Statistics")
#print ("Count = ", count_value)
print ("Mean = ", '{:f}'.format(mean_value))
print ("Std Dev =",'{:f}'.format(stdDev_value))
print ("std_error = ", '{:f}'.format(stdError_value))
print ("variance = ", '{:f}'.format(var_value))

print("\nSignificance")
print ("alpha = ",'{:f}'.format(alpha) )

print("\nConfidence Interval for the Mean")
#Two tailed: alpha/2 Single 
print("T Distribution = ", '{:f}'.format(tDist))
print ("Low mean = ", '{:f}'.format(low_mean))
print ("High mean = ", '{:f}'.format(high_mean))

print("\nUpper bound on the variance")
print("chi2 = ", '{:f}'.format(chiSqrd) )
print("Max Variance = ", '{:f}'.format(max_var))
print("Max Standard Deviation = ",'{:f}'.format(max_std))

print("\nMonty Carlo Results")
print("Monty Carlo Lower Limit = ", '{:f}'.format(pdf[lower_limit]))
print("Monty Carlo Upper Limit = ", '{:f}'.format(pdf[upper_limit]))

print("\nSignificance Bounds on Most Likely Normal Distribution")
print("norm lower bound = ", '{:f}'.format(norm_low))
print("norm upper bound = ", '{:f}'.format(norm_high))
print("\nDifference in bounds")
print("The upper difference in limits = ", '{:f}'.format(upper_diff))
print("The lower difference in limits = ", '{:f}'.format(lower_diff))