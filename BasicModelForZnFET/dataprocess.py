import glob
import matplotlib.pyplot as plt
import openmc
import os
import numpy as np
import openmc.capi as capi
import scipy.misc as scm
import scipy.special as scp
import generate_xml as genxml
import helperfunction as hf
import csv

####function to process data######
def process_data(ringnum,zerk_order,rad,n):
	N = int(n)
	Nstr = str(N)
	modenum=int(np.floor(zerk_order/2)+1)

	# TKL_TAL
	directory = "./data/TKL/"+ Nstr+"/"
	filename = "statepoint."+str(int(n+100))+".h5"
	sp = openmc.StatePoint(directory+filename)
	tkltal = sp.get_tally(name='tracklength')
	df=tkltal.get_pandas_dataframe()
	# print(df[df['score'] == 'absorption'])
	tkl_abs = df[df['score'] == 'absorption']['mean']
	tkl_abs = tkl_abs.values
	directory = "./data/TKL/"+ Nstr+"/"
	filename3 = "abs_rate_tkl_"+Nstr+".csv"
	np.savetxt(directory+filename3, tkl_abs, delimiter=",")

	#FET
	directory = "./data/FET/"+ Nstr+"/"
	filename = "statepoint."+str(int(n+100))+".h5"
	sp = openmc.StatePoint(directory+filename)
	name = 'fet'+str(zerk_order)
	fettal = sp.get_tally(name=name)
	# df = fet.get_pandas_dataframe()
	fetabs = fettal.get_slice(scores=['absorption'])
	fet_abs_coeff = fetabs.get_pandas_dataframe()['mean']
	pos,nvec = hf.get_position(zerk_order)
	tal_at_pos = hf.get_val_at_pos(pos,fet_abs_coeff)
	a_n= np.multiply(nvec,tal_at_pos)

	fet_abs = np.zeros((modenum,ringnum))
	for i in range(0,modenum):
		# i = int(order/2)
		coeff = a_n[0:i+1]
		for j in range(0,ringnum):
			rin = rad[j] 
			rout = rad[j+1]
			w = hf.equal_vol_rings(rin,rout,1000)
			# print(pos[0:i+1])
			y = hf.fet_func(w,coeff,pos[0:i+1])
			fet_abs[i,j] = 2*np.pi*np.trapz(np.multiply(y,w),w)

	# ###Note that `numerical integration` here is very time consuming.
	# fet_abs=[]
	# for order in range(0,int(zerk_order+2),2):
	# 	pos,nvec = hf.get_position(order)
	# 	# print(pos)
	# 	tal_at_pos = hf.get_val_at_pos(pos,fet_abs_coeff)
	# 	fetintvalue = np.zeros(ringnum)
	# 	for i in range(0,len(rad)-1):
	# 		fetintvalue[i] = hf.num_int_a_ring(rad[i],rad[i+1],order,pos,tal_at_pos,nvec)
	# 	fet_abs.append(fetintvalue)

	directory = "./data/FET/"+ Nstr+"/"
	filename3 = "abs_rate_fet_"+Nstr+".csv"
	np.savetxt(directory+filename3, fet_abs, delimiter=",")

	# ### Load Reference
	directory = "./reference/100000"
	filename1 = "abs_rate_tkl_100000.csv"

	with open(directory+"/"+filename1) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		ref = []
		for row in readCSV:
			ref.append(row)
	ref = np.mat(ref)
	ref = ref.astype(np.float)
	ref = np.squeeze(np.asarray(ref))
	ref = np.ndarray.tolist(ref)
	# print(ref)
	# realref = hf.shrink(ref,ringnum)
	# print(ref)
	
	#error analysis
	err1 = np.zeros(int(np.floor(zerk_order/2)+1))
	# print(realref)
	# print(fet_abs[j])
	for j in range(0,len(err1)):
		# print(j)
		err1[j] = hf.rRMSE(fet_abs[j],ref,ringnum)

	err2 = np.zeros(1)

	#print(ref)
	err2[0] = hf.rRMSE(tkl_abs,ref,ringnum)

	err = np.append(err1,err2)
	# print(len(err))
	directory = "./data"
	filename5 = "err_"+Nstr+".csv"
	np.savetxt(directory+"/"+filename5, err, delimiter=",")
