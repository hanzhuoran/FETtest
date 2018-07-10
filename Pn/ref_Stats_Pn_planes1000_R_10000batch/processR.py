import matplotlib.pyplot as plt
import os
import openmc
import numpy as np
import helperfunction as hf
import csv

# ### Load Reference
directory = "./data/FET/1000000/"
sp = openmc.StatePoint(directory+'statepoint.1000.h5')
porder = 15
name = 'fet'+str(porder)
fet = sp.get_tally(name=name)
df = fet.get_pandas_dataframe()
print(df[df['score'] == 'absorption'])
fet_mean_coeff = df[df['score'] == 'absorption']['mean']
fet_std_coeff = df[df['score'] == 'absorption']['std. dev.']
fet_var_coeff = np.square(fet_std_coeff)
# print(fet_mean_coeff)
# print(fet_std_coeff)
# print(fet_var_coeff)
normarray = np.arange(porder+1)
k_n = (2*normarray + 1)/2
up = np.multiply(fet_var_coeff,k_n)
down = np.square(fet_mean_coeff)
Rvalue = np.divide(up,down)
# print(up)
# print(down)
# print(Rvalue)
plt.plot(normarray[1:16],Rvalue[1:16],'ro')
plt.yscale('log')
#plt.xscale('log')
plt.savefig("R",dpi=500)
plt.show()

