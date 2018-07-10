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

plnnum = 100
porder = 50
pln,plnmid = hf.get_planes(plnnum)

N = [1000]

for n in N:
	dp.process_data(plnnum,porder,pln,n)
