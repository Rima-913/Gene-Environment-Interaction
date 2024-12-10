import random 
import numpy as np
import pandas as pd
import scipy.stats as stats
# relative bias function
def rel_bias(original,new):
    return ((new-original)/original)*100

data=pd.read_csv('data(3).csv')
# print(data)
relative_bias=[]
mean= list(data.mean())
# print(mean)
for i in mean:
    relative_bias.append(rel_bias(0.2,i))

# print(relative_bias)

"""Mean Square Error"""
MSE=[]
for i in range(4):
    mse=0
    for j in range(100):
        mse += (0.2-data.iloc[j,i])**2
        mse/=100
    MSE.append(mse)
# print(MSE)

"""Hypothesis testing"""
# Null Hypothesis 
# 𝐻0 : The mean interaction coefficient is 0 across scenarios.
# Alternative Hypothesis 
# 𝐻𝑎 : The mean interaction coefficient is non_zero across scenarios.

hypothesized_mean =0
alpha=0.05
df=99=100-1

only_genotype_error = data.iloc[:,0]
only_environment_error = data.iloc[:,1]
both_errors = data.iloc[:,2]


t_stat1= ((np.mean(only_genotype_error)- hypothesized_mean)*10)/ np.std(only_genotype_error)
t_stat2= ((np.mean(only_environment_error)- hypothesized_mean)*10)/ np.std(only_environment_error)
t_stat3= ((np.mean(both_errors)- hypothesized_mean)*10)/ np.std(both_errors)

p_val1=2* stats.t.sf(np.abs(t_stat1), df=99)
p_val2=2* stats.t.sf(np.abs(t_stat2), df=99)
p_val3=2* stats.t.sf(np.abs(t_stat3), df=99)

print('T_stat1 : {}, T_stat2 : {},T_stat3 : {}'.format(t_stat1,t_stat2,t_stat3))
print('p_val1: {}, p_val2: {}, p_val3: {}'.format(p_val1,p_val2,p_val3))

