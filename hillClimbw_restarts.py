# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 22:49:48 2022

@author: jasmi
"""


#basic hill climbing search provided as base code for the DSA/ISE 5113 course
#author: Charles Nicholson
#date revised: 3/26/2021

#NOTE: YOU MAY CHANGE ALMOST ANYTHING YOU LIKE IN THIS CODE.  
#However, I would like all students to have the same problem instance, therefore please do not change anything relating to:
#   random number generator
#   number of items (should be 150)
#   random problem instance
#   weight limit of the knapsack

#------------------------------------------------------------------------------

#Student name:Jasmin Wilson
#Date: 04.10.2022


#need some python libraries
from random import Random   #need this for the random number generation -- do not change
import numpy as np


#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 51132021
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#number of elements in a solution
n = 150

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    value.append(round(myPRNG.triangular(150,2000,500),1))
    
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(8,300,95),1))
    
#define max weight for the knapsack
maxWeight = 2500

k_restarts = 10    #number of restarts to do

#change anything you like below this line ------------------------------------
#some of the provided functions are intetionally incomplete
#also, you may wish to restructure the approach entirely -- this is NOT the world's best Python code


#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
def evaluate(x):
          
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)
    
    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection
    
    if totalWeight > maxWeight:
        totalValue = np.nan
    
    return [totalValue, totalWeight]   #returns a list of both total value and total weight
          
       
#here is a simple function to create a neighborhood
#1-flip neighborhood of solution x         
def neighborhood(x):
        
    nbrhood = []     
    
    for i in range(0,n):
        nbrhood.append(np.copy(x))
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
      
    return nbrhood
          


#create the initial solution
def initial_solution():
    x = []   #i recommend creating the solution as a list
    weightCount=0   #weight counter
    totalOnes=0     #total one's needed
    #this loop will make sure of weight constraint of intial solution
    while weightCount <= maxWeight:
        weightCount= weightCount+ myPRNG.choice(weights) #adding randomness in choosing different weight than highest
        totalOnes+=1 #keep a count until random weights equals 2500 or less
        
    x= np.zeros(n, dtype=int)   #fill x with 0's
    x[np.random.randint(n, size=totalOnes)] = 1 #adding randomness is placing one's differently
    total_weight = evaluate(x)[1]   #use evaluate function to get the total weight
    
    #makes sure of no infeasability
    if total_weight > maxWeight: #if feasibility found, generate random again until totalWeight < maxWeight
        x= np.zeros(n, dtype=int)   #fill x with 0's
        while weightCount <= maxWeight:
            weightCount= weightCount+ myPRNG.choice(weights)
            totalOnes+=1
            x[np.random.randint(n, size=totalOnes)] = 1 #randomly assing 1's
            total_weight = evaluate(x)[1] #calculate totalWeight again
    
    return x

#------ USING BEST-ACCEPT METHOD


#varaible to record the number of solutions evaluated
solutionsChecked = 0

#store all the past solutions from the restarts 
best_value = []     #stores the best values from all restarts
best_weights = []   #stores the best weights from all restarts
best_x = []         #stores the best solutions from all restarts


for restart in range(k_restarts): 

    x_curr = initial_solution()  #x_curr will hold the current solution 
    x_best = x_curr[:]           #x_best will hold the best solution 
    f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton 
    f_best = f_curr[:]
    
    
    
    #begin local search overall logic ----------------
    done = 0
        
    while done == 0:
                
        Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
        
        for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:   
                x_best = s[:]                 #find the best member and keep track of that solution
                f_best = evaluate(s)[:]       #and store its evaluation  
        
        if f_best == f_curr:               #if there were no improving solutions in the neighborhood
            done = 1
        else:
            
            x_curr = x_best[:]         #else: move to the neighbor solution and continue
            f_curr = f_best[:]         #evalute the current solution
            
            print ("\nTotal number of solutions checked: ", solutionsChecked)
            print ("Best value found so far: ", f_best)

    best_value.append(f_best[0])
    best_weights.append(f_best[1])
    best_x.append(x_best)
    
print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)
