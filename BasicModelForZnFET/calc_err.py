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

ringnum = 100
zerk_order = 100
rad,radmid = hf.get_radius(ringnum)

#Also, we can also take an array
#num = int(sys.argv[1])
N = []
for i in range(1,len(sys.argv)):
	N.append(int(sys.argv[i]))

for n in N:
	dp.process_data(ringnum,zerk_order,rad,n)
	