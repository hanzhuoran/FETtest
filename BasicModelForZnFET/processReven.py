import matplotlib.pyplot as plt
import os
import openmc
import numpy as np
import helperfunction as hf
import csv
import sys

num = int(sys.argv[1])
N = [num]
zerk_order = 100
evenmodes = int(zerk_order/2+1)
orderarray = np.linspace(0,zerk_order,evenmodes)
pos,k_n = hf.get_position(zerk_order)
for n in N:
	# ### Load Reference
	directory = "./data/FET/"+str(n)+"/"
	filename = "statepoint."+str(int(n+100))+".h5"
	sp = openmc.StatePoint(directory+filename)
	name = 'fet'+str(zerk_order)
	fettal = sp.get_tally(name=name)

	fetabs = fettal.get_slice(scores=['absorption'])
	fetabs_mean = fetabs.get_pandas_dataframe()['mean']
	fetabs_std = fetabs.get_pandas_dataframe()['std. dev.']

	fet_mean_coeff = hf.get_val_at_pos(pos,fetabs_mean)
	fet_std_coeff = hf.get_val_at_pos(pos,fetabs_std )
	fet_var_coeff = np.square(fet_std_coeff)

	# normarrayeven = np.linspace(0,zerk_order,num = (zerk_order/2)+1)
	# print(normarrayeven)
	# k_n = (2*normarrayeven + 1)/2

	up = np.multiply(fet_var_coeff,k_n)
	upnew = fet_var_coeff
	down = np.square(fet_mean_coeff)
	Rvalue = np.divide(up,down)
	Rvalue_new = np.divide(upnew,down)
	
	ones = np.ones(len(orderarray))
	plt.plot(orderarray,ones,label = "R^2=1")
	plt.plot(orderarray,Rvalue,'o',label = "R w/ k")
	plt.plot(orderarray,Rvalue_new,'o',label = "R w/o k")
	plt.yscale('log')
	plt.xlabel('orders')
	plt.ylabel('R value')
	plt.legend()
	plt.savefig("R_even",dpi=500)
	plt.show()


