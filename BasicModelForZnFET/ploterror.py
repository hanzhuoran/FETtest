import matplotlib.pyplot as plt
import os
import numpy as np
import generateplot as gp
import sys

zerk_order = 100
totalmodes = int((zerk_order+2)*(zerk_order+1)/2)
evenmodes= int(np.floor(zerk_order/2)+1)
# print(evenmodes)
N = []
for i in range(1,len(sys.argv)):
    N.append(int(sys.argv[i]))

gp.generate_plotM(N,zerk_order,evenmodes)
# gp.generate_plotN(N,porder)
