import random 
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
# function fro simulating genotypes
def simulate_genotypes(num_individuals, freq_ref):
    genotypes=[]
    for i in range(num_individuals):
        p_AA = freq_ref ** 2
        p_Aa = 2 * freq_ref * (1 - freq_ref)
        p_aa = (1 - freq_ref) ** 2
            
            # Use random.choices() with weighted probabilities
        
        gen = random.choices([0, 1, 2], weights=[p_AA, p_Aa, p_aa])[0]
        genotypes.append(gen)
    return genotypes

# relative bias function
def rel_bias(original,new):
    return ((new-original)/original)*100

error_rate = 0.1  # 5% error rate
num_errors = 10

n_samples=100
interacton_coeff=[]
for i in range(n_samples):
    coef=[]
    #genotype simulation and creating a dataframe
    genotype_data = simulate_genotypes(100,freq_ref=0.6)
    data1=pd.DataFrame({'genotype':genotype_data})
    #exposure simulation 
    data1['Exposure'] = np.random.binomial(1,0.6,100)
    #phenotype simulation 
    beta_gen = 0.3
    beta_exp = 0.5
    interaction_effect = 0.2
    data1['Phenotype'] = (beta_gen * data1['genotype'] +
                          beta_exp* data1['Exposure'] +
                          interaction_effect * data1['genotype'] * data1['Exposure'] +
                          np.random.normal(0, 1, 100))
    
    # adding error to genotype 
    rows_for_gen = np.random.choice(data1.index, num_errors, replace=False)
    data1['genotype_with_error']=data1['genotype']
    for row in rows_for_gen:
        original_genotype = data1.loc[row, 'genotype']
    
        possible_values = [0, 1, 2]
        possible_values.remove(original_genotype)
    
        new_genotype = np.random.choice(possible_values)
        data1.loc[row, 'genotype_with_error'] = new_genotype

    # adding error to exposure 
    rows = np.random.choice(data1.index, 20, replace=False)
    data1['Exposure_with_error']=data1['Exposure']
    for row in rows:
        data1.loc[row,'Exposure_with_error']= 1-data1.loc[row,'Exposure']
    
    #calculating the interaction terms
    data1['interaction_without_error']=data1['genotype'] * data1['Exposure']
    data1['interaction_with_gen_error']=data1['genotype_with_error']*data1['Exposure']
    data1['interaction_with_exp_error']=data1['Exposure_with_error']*data1['genotype']
    data1['interaction_with_both_error']=data1['genotype_with_error']*data1['Exposure_with_error']
    
    x_1=data1[['genotype_with_error','Exposure','interaction_with_gen_error']]
    x_2=data1[['genotype','Exposure_with_error','interaction_with_exp_error']]
    x_3=data1[['genotype_with_error','Exposure_with_error','interaction_with_both_error']]
    x_4=data1[['genotype','Exposure','interaction_without_error']]
    y=data1['Phenotype']
    model1=LinearRegression().fit(x_1,y)
    model2=LinearRegression().fit(x_2,y)
    model3=LinearRegression().fit(x_3,y)
    model4=LinearRegression().fit(x_4,y)
    
    coef.append(model1.coef_[2])
    coef.append(model2.coef_[2])
    coef.append(model3.coef_[2])
    coef.append(model4.coef_[2])
    
    interacton_coeff.append(coef)
# print(interacton_coeff)

#making a data frame of these interaction coeff
df=pd.DataFrame(interacton_coeff)
df.columns=['genotype error','exposure error','both error','without error']
print(df)

df.to_csv('data(4).csv',index=False)
