import matplotlib.pyplot as plt
import os
import numpy as np
import generateplot as gp
import sys

porder = 50
#N = [100,1000,10000,100000,1000000]
N = [100]
# for i in range(1,len(sys.argv)):
#     N.append(int(sys.argv[i]))

gp.generate_plotM(N,porder)
#gp.generate_plotN(N,porder)
