import numpy as np
import matplotlib.pyplot as plt
import os
import csv
def generate_plotM(N,porder):
    errormatrix = np.zeros((porder+2,len(N)))
    errormatrix = np.mat(errormatrix)
    orderarray = np.linspace(0,porder,porder+1)
    for i in range(0,len(N)):
        n = N[i]
        Nstr = str(n)
        directory = "./"+Nstr
        filename1 = "err_"+Nstr+".csv"
        # print(directory+"/"+filename1)
        with open(directory+"/"+filename1) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            val = []
            for row in readCSV:
                # print(row)
                val.append(row)
            val = np.mat(val)
            errormatrix[:,i]=val
    errormatrix[porder+1,len(N)-1] = 1e-6
    # print(errormatrix)
    for i in range(0,len(N)):
        n = N[i]
        Nstr = str(n)
        temp = np.ndarray.tolist(errormatrix[:,i])
        # print(temp)
        plt.plot(orderarray,temp[:-1],'o',label = Nstr)
    plt.legend()
    plt.yscale('log')
    plt.xlabel('orders')
    plt.savefig("err_vs_M.png", dpi = 500)
    plt.show()

def generate_plotN(N,porder):
    errormatrix = np.zeros((porder+2,len(N)))
    errormatrix = np.mat(errormatrix)
    Narray = np.multiply(N,1e5)
    for i in range(0,len(N)):
        n = N[i]
        Nstr = str(n)
        directory = "./"+Nstr
        filename1 = "err_"+Nstr+".csv"
        # print(directory+"/"+filename1)
        with open(directory+"/"+filename1) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            val = []
            for row in readCSV:
                # print(row)
                val.append(row)
            val = np.mat(val)
            errormatrix[:,i]=val
        if n == 1e4:
            errormatrix[porder+1,i] = 1e-5
            print(errormatrix)
    for i in [0,5,10,15,20,25,50,51]:
        if i <= porder:
            name = str(2*i)
        # elif i == porder+1:
        #     name = "collision"
        # elif i == porder+:
        #     name = "analog"
        elif i == porder+1:
            name = "tracklength"
        temp = np.ndarray.tolist(errormatrix[i,:])[0]
        plt.plot(Narray,temp,label = name, marker = 'o')
    # one = np.ones(len(N))
    # one = np.multiply(one,1e-3)
    # plt.plot(N,one,label = "std")
    plt.legend()
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('# of Particles')
    plt.savefig("err_vs_N.png", dpi = 500)
    plt.show()
