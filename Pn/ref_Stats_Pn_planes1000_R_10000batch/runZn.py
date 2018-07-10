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
import dataprocess as dp
import generateplot as gp
import sys

plnnum = 1000
porder = 100
# totalmodes = int((porder+2)*(porder+1)/2)
# evenmodes= int(np.floor(porder/2)+1)
# rad,radmid = hf.get_radius(ringnum)

#low = float(sys.argv[1])
#up = float(sys.argv[2])
#num = int(sys.argv[3])
num = int(sys.argv[1])

#N = np.geomspace(low,up,num)
N = [num]
print(N)
fuelcelllist,total_fuel_cell=genxml.generate_mat_and_geom(plnnum)

#tracklength#
for n in N:
	genxml.generate_tallies(fuelcelllist,total_fuel_cell,porder,1)
	genxml.generate_settings(n)
	# Run OpenMC!
	#openmc.run(threads = 4)
	openmc.run(mpi_args=['mpiexec', '-n', '4'])
	#create directory
	Nstr = str(n)
	directory = "./data/TKL/"+ Nstr
	if not os.path.exists(directory):
	    os.makedirs(directory)

	filename1 = directory+'/statepoint.10100.h5'
	os.rename('statepoint.10100.h5',filename1)
	filename2 = directory+'/summary.h5'
	os.rename('summary.h5',filename2)

#FET
#for n in N:
#	genxml.generate_tallies(fuelcelllist,total_fuel_cell,porder,2)
#	genxml.generate_settings(n)
	# Run OpenMC!
	#openmc.run(threads = 4)
#	openmc.run(mpi_args=['mpiexec', '-n', '4'])
	#create directory
#	Nstr = str(n)
#	directory = "./data/FET/"+ Nstr
#	if not os.path.exists(directory):
#	    os.makedirs(directory)

#	filename1 = directory+'/statepoint.10100.h5'
#	os.rename('statepoint.10100.h5',filename1)
#	filename2 = directory+'/summary.h5'
#	os.rename('summary.h5',filename2)
