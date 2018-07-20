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
def process_data(plnnum,porder,pln,n):
	N = int(n)
	Nstr = str(N)
	zmin = -100
	zmax = 100
	norm = (zmax-zmin)/2
	directory = "./data/TKL/"+ Nstr+"/"
	filename = "statepoint."+str(int(n+100))+".h5"
	sp = openmc.StatePoint(directory+filename)

	#TKL
	tal3 = sp.get_tally(name='tracklength')
	df=tal3.get_pandas_dataframe()
	# print(df)
	tkl_abs = df[df['score'] == 'absorption']['mean']
	tkl_abs = tkl_abs.values

	directory = "./data/TKL/"+ Nstr+"/"
	filename3 = "abs_rate_tkl_"+Nstr+".csv"
	np.savetxt(directory+filename3, tkl_abs, delimiter=",")

	realref = hf.loadreference(plnnum)
	#FET
	directory = "./data/FET/"+ Nstr+"/"
	filename = "statepoint."+str(int(n+100))+".h5"
	sp = openmc.StatePoint(directory+filename)

	name = 'fet'+str(porder)
	fet = sp.get_tally(name=name)
	df = fet.get_pandas_dataframe()
	# print(df)
	fet_abs_coeff = df[df['score'] == 'absorption']['mean']
	normarray = np.arange(porder+1)
	a_n = (2*normarray + 1)/2 * fet_abs_coeff

	fet_abs = np.zeros((porder+1,plnnum))
	fetval = np.zeros((porder+1,plnnum))
	dz = (zmax-zmin)/plnnum

	t = 1000
	#for i in range(0,porder+1):
	for i in [2,50]:
		wtot = []
		diffsqrtot = []
		coeff = a_n[0:i+1]
		print("for order:",i)
		fet_abs_func = np.polynomial.Legendre(coeff/norm, domain=(zmin,zmax))
		for j in range(0,plnnum):
			# //plnnum
			zlow = dz*j+zmin
			zhigh = dz*(j+1)+zmin
			w = np.linspace(zlow, zhigh, t)
			ref = realref[j]
			intg = np.trapz(fet_abs_func(w),w)
			fetval[i,j] = intg
			diff = fet_abs_func(w)-ref
			diffsqr = np.square(diff)
			# print(np.ndarray.tolist(w))
			wtot += np.ndarray.tolist(w)
			# print(wtot)
			#print(len(wtot))
			diffsqrtot += np.ndarray.tolist(diffsqr)
			#print(len(diffsqrtot))
			fet_abs[i,j] = np.trapz(diffsqr,w)
			# print(fet_abs[i,j])
		# print(len(wtot))
		# print(len(diffsqrtot))
		plt.figure(1)
		plt.title(str(i))
		plt.plot(wtot,diffsqrtot,label = str(i))
		plt.savefig("diffsqr"+str(i)+".png",dpi = 500)
		plt.show()


	plotref = np.append(realref,realref[-1])
	plt.figure(2)
	plt.plot(pln,plotref,drawstyle='steps-post',label ='ref',alpha=0.5)
	plt.plot(pln[:-1],fetval[porder],label = 'fet50')
	# # plt.plot(pln[:-1],fetval[40,:],label = 'fet40')
	# # plt.plot(pln[:-1],fetval[30,:],label = 'fet30')
	# # plt.plot(pln[:-1],fetval[20,:],label = 'fet20')
	# plt.plot(pln[:-1],fetval[10,:],label = 'fet10')
	# print(fetval[1])
	plt.plot(pln[:-1],fetval[2],label = 'fet2')
	plt.plot(pln[:-1],fetval[1],label = 'fet1')
	plt.legend()
	plt.savefig("comp.png",dpi = 500)
	plt.show()

	directory = "./data/FET/"+ Nstr+"/"
	filename3 = "abs_rate_fet_"+Nstr+".csv"
	np.savetxt(directory+filename3, fet_abs, delimiter=",")


	#error analysis
	err1 = np.zeros(porder+1)
	for i in range(0,len(err1)):
		err1[i] = np.sum(fet_abs[i])
		#err1[i] = hf.rRMSE(fetval[i],realref,plnnum)


########### how to deal with each slab

	err2 = np.zeros(1)

	# print(tkl_abs)

	err2[0] = hf.rRMSE(tkl_abs,realref,plnnum)

	err = np.append(err1,err2)
	# print(len(err))
	directory = "./data"
	filename5 = "err_"+Nstr+".csv"
	np.savetxt(directory+"/"+filename5, err, delimiter=",")
