#Developed by Anvar Akhiiartdinov

import numpy as np
import random

no_switch_wins = 0
switch_wins = 0

#number of runs
n = 100000

for i in range(n):
    
    a = random.randint(0,1)
    if a == 1:
        b = 0
        c = 0
    else:
        b = random.randint(0,1)
        if b == 1:
            c = 0
        else:
            c = 1
    
    options = [a,b,c]            
    array = np.array(options)
    #print(array)
    
    #my random choice of a door
    pick_ind = random.choice([0,1,2])
    #print("picked door= ", pick_ind)
    
    #identify non-zero element
    nzero_ind = np.nonzero(array)[0]
    #print("door with car= ", nzero_ind)
    
    #array of indeces with zero values
    zero_ind = np.nonzero(array==0)[0]
    #print("doors with goats= ", zero_ind)
    
    #host opens that door
    if pick_ind == zero_ind[0]:
            host_ind = zero_ind[1]
    elif pick_ind == zero_ind[1]:
            host_ind = zero_ind[0]
    else:
        host_ind = random.choice(zero_ind)
    #print("Host opens door= ", host_ind)
    
    left_zero_ind = np.setdiff1d(zero_ind,host_ind)
    #print("Left zero index= ", left_zero_ind)
    
    #Count number of wins
    if pick_ind == nzero_ind:
        no_switch_wins += 1
    if pick_ind == left_zero_ind:
        switch_wins +=1
        
print("No switch wins= ",no_switch_wins)
print("Switch wins= ", switch_wins)
print(2/3," = ",switch_wins/n," Great! Statistics work!")    
