import numpy as np
import matplotlib.pyplot as plt
import os
import csv

####Geneate plot of RMSE vs Order M for a certain number of particles
def generate_plotM(N,zerk_order,evenmodes):
    errormatrix = np.zeros((evenmodes+1,len(N)))
    errormatrix = np.mat(errormatrix)
    orderarray = np.linspace(0,zerk_order,evenmodes)
    for i in range(0,len(N)):
        n = N[i]
        Nstr = str(n)
        directory = "./data"
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
    # errormatrix[evenmodes+1,len(N)-1] = 1e-6
    # print(errormatrix)
    for i in range(0,len(N)):
        n = N[i]
        Nstr = str(n)
        temp = np.ndarray.tolist(errormatrix[:,i])
        print(len(temp))
        plt.plot(orderarray,temp[:-1],'o',label = Nstr)
    plt.legend()
    plt.yscale('log')
    plt.xlabel('orders')
    plt.ylabel('rRMSE')
    plt.savefig("err_vs_M.png", dpi = 500)
    plt.show()


####Geneate plot of RMSE vs number of particles at a certain order
def generate_plotN(N,evenmodes):
    errormatrix = np.zeros((evenmodes+2,len(N)))
    errormatrix = np.mat(errormatrix)
    for i in range(0,len(N)):
        n = N[i]
        Nstr = str(n)
        directory = "./data"
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
        if n == 1e6:
            errormatrix[evenmodes+1,i] = 1e-5
            print(errormatrix)
    for i in range(0,evenmodes+2):
        if i <= evenmodes:
            name = str(i)
        # elif i == evenmodes+1:
        #     name = "collision"
        # elif i == evenmodes+:
        #     name = "analog"
        elif i == evenmodes+1:
            name = "tracklength"
        temp = np.ndarray.tolist(errormatrix[i,:])[0]
        plt.plot(N,temp,label = name, marker = 'o')
    # one = np.ones(len(N))
    # one = np.multiply(one,1e-3)
    # plt.plot(N,one,label = "std")
    plt.legend()
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('# of Particles')
    plt.ylabel('rRMSE')
    plt.savefig("err_vs_N.png", dpi = 500)
    plt.show()
