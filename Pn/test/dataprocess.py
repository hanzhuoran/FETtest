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

def process_data(plnnum,porder,pln,n):
	N = int(n)
	Nstr = str(N)
	zmin = -100
	zmax = 100
	norm = (zmax-zmin)/2
	directory = "./data/TKL/"+ Nstr+"/"
	sp = openmc.StatePoint(directory+'statepoint.10100.h5')

	tal3 = sp.get_tally(name='tracklength')
	df=tal3.get_pandas_dataframe()
	tkl_abs = df[df['score'] == 'absorption']['mean']
	tkl_abs = tkl_abs.values

	directory = "./data/FET/"+ Nstr+"/"
	sp = openmc.StatePoint(directory+'statepoint.10100.h5')

	name = 'fet'+str(porder)
	fet = sp.get_tally(name=name)
	df = fet.get_pandas_dataframe()
	fet_abs_coeff = df[df['score'] == 'absorption']['mean']
	normarray = np.arange(porder+1)
	a_n = (2*normarray + 1)/2 * fet_abs_coeff

	fet_abs_func = np.polynomial.Legendre(a_n/norm, domain=(zmin,zmax))

	fet_abs = np.zeros((porder+1,plnnum))
	dz = (zmax-zmin)/plnnum
	for i in range(0,porder+1):
		for j in range(0,plnnum):
			zlow = dz*j+zmin
			zhigh = dz*(j+1)+zmin
			w = np.linspace(zlow, zhigh, 10000)
			coeff = a_n[0:i+1]
			fet_abs_func = np.polynomial.Legendre(coeff/norm, domain=(zmin,zmax))
			fet_abs[i,j] = np.trapz(fet_abs_func(w), w)

	directory = "./data/TKL/"+ Nstr+"/"
	filename3 = "abs_rate_tkl_"+Nstr+".csv"
	np.savetxt(directory+filename3, tkl_abs, delimiter=",")

	directory = "./data/FET/"+ Nstr+"/"
	filename3 = "abs_rate_fet_"+Nstr+".csv"
	np.savetxt(directory+filename3, fet_abs, delimiter=",")

	# ### Load Reference
	directory = "./data/TKL/10000"
	filename1 = "abs_rate_tkl_10000.csv"

	with open(directory+"/"+filename1) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		ref = []
		for row in readCSV:
			ref.append(row)
	ref = np.mat(ref)
	ref = ref.astype(np.float)
	ref = np.squeeze(np.asarray(ref))
	ref = np.ndarray.tolist(ref)
	realref = hf.shrink(ref,plnnum)
	# print(ref)
	
	#error analysis
	err1 = np.zeros(porder+1)
	# print('here')
	for j in range(0,len(err1)):
		err1[j] = hf.rRMSE(fet_abs[j],realref,plnnum)

	err2 = np.zeros(1)
	# err2[0] = hf.rRMSE(abs_rate_col,ref,ringnum)
	# err2[1] = hf.rRMSE(abs_rate_ana,ref,ringnum)
	# tkl_abs = tkl_abs.values
	#print(tkl_abs)

	#print(ref)
	err2[0] = hf.rRMSE(tkl_abs,realref,plnnum)

	err = np.append(err1,err2)
	# print(len(err))
	directory = "./data"
	filename5 = "err_"+Nstr+".csv"
	np.savetxt(directory+"/"+filename5, err, delimiter=",")
