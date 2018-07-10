import matplotlib.pyplot as plt
import os
import openmc
import numpy as np
import helperfunction as hf
import csv

# ### Load Reference
directory = "./data/FET/10000/"
sp = openmc.StatePoint(directory+'statepoint.10100.h5')
porder = 50
name = 'fet'+str(porder)
fet = sp.get_tally(name=name)
df = fet.get_pandas_dataframe()
# print(df[df['score'] == 'absorption'])
fet_mean_coeff = df[df['score'] == 'absorption']['mean']
fet_std_coeff = df[df['score'] == 'absorption']['std. dev.']
fet_var_coeff = np.square(fet_std_coeff)
fet_var_coeff_even = fet_var_coeff[::2]
fet_mean_coeff_even = fet_mean_coeff[::2] 
# print(fet_mean_coeff)
# print(fet_std_coeff)
# print(fet_var_coeff)
# normarray = np.arange(porder+1)
normarrayeven = np.linspace(0,porder,num = (porder/2)+1)
print(normarrayeven)
k_n = (2*normarrayeven + 1)/2
up = np.multiply(fet_var_coeff_even,k_n)
upnew = fet_var_coeff_even
down = np.square(fet_mean_coeff_even)
Rvalue = np.divide(up,down)
Rvalue_new = np.divide(upnew,down)
ones = np.ones(len(normarrayeven))
plt.plot(normarrayeven,ones,label = "R^2=1")
plt.plot(normarrayeven,Rvalue,'o',label = "R w/ k")
plt.plot(normarrayeven,Rvalue_new,'o',label = "R w/o k")
plt.yscale('log')
plt.savefig("R_even",dpi=500)
plt.show()


