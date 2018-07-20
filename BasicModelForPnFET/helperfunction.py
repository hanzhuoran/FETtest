import openmc
import numpy as np
import openmc.capi as capi
import os
import csv

def get_position(order):
# get the position of even orders in ANSI rule
# order: maximum order of polys
# position: the position of even orders
# normvec: vectors for normalizatoin as it changes with orders.
	R = 0.392
	position = []
	normvec = []
	max_even_order = np.floor(order/2)*2
	max_even_order = int(max_even_order)

	for i in range(0,max_even_order+2,2):
	    pos = i*(i+2)/2
	    pos = int(pos)
	    position.append(pos)
	    normval = (i+1)/(np.pi*R**2)
	    normvec.append(normval)
	return position, normvec

def get_radius(ringnum):
# get the radius bins and the middle position in each bin
# ringnum: number of rings
# rad: vectors of radial postions
# radmid: middle position in each bins
    Rout = 0.392
    darea = np.pi*Rout**2/ringnum
    area = 0
    rad = [0]
    for i in range(0,ringnum):
        area += darea
        r = np.sqrt(area/np.pi)
        rad.append(r)
    radmid=np.multiply(0.5,np.add(rad[0:ringnum],rad[1:ringnum+1]))
    return rad,radmid

def get_planes(plnnum):
# get the radius bins and the middle position in each bin
# ringnum: number of rings
# rad: vectors of radial postions
# radmid: middle position in each bins
    zmin = -100
    zmax = 100
    dz = (zmax-zmin)/plnnum
    pln = [zmin]
    for i in range(0,plnnum):
        p = zmin+(i+1)*dz
        pln.append(p)
    plnmid=np.multiply(0.5,np.add(pln[0:plnnum],pln[1:plnnum+1]))
    return pln,plnmid


def get_tal_at_pos(position,fetabs_rate):
# get the tally results given the position of even orders
# position: Zernike even order positions
# fetabs_rate: FET results
# tal_at_pos: desired tally results
    tal_at_pos = np.zeros(len(position))
    for i in range(0,len(position)):
        tal_at_pos[i] =  fetabs_rate[position[i]]
    return tal_at_pos

def get_fet_est(radmid,position,order,tal_at_pos,normvec):
# get the FET estimations at the middle of each rings
# radmid: middle positions
# order: order of zernikes
# position: even order positions
# tal_at_pos: tallies at even orders
# normvec: normalization vectors
# fet_est_norm: normalized results to get the shape
    zn_mode = np.zeros((len(radmid),len(position)))
    R = 0.392
    for j in range(0,len(radmid)):
        full_zn_vals = capi.calc_zn(order,radmid[j]/R,0)
        for k in range(0,len(position)):
            zn_mode[j,k] = full_zn_vals[position[k]]
    tal_at_pos_mat = np.mat(tal_at_pos)
    normvec_mat = np.mat(normvec)
    tal_at_pos_mat = np.multiply(tal_at_pos_mat,normvec_mat)
    estimate = zn_mode*np.transpose(tal_at_pos_mat)
    fet_est = np.squeeze(np.asarray(estimate))
    fet_est_norm = fet_est/np.linalg.norm(fet_est)
    return fet_est_norm

def num_int_a_ring(r1,r2,order,position,tal_at_pos,normvec):
# numerical integrate the results in a ring
# r1: inner radius
# r2: outer radius
# order: order of zernikes
# position: even order positions
# tal_at_pos: tallies at even orders
# normvec: normalization vectors
# integral: numerical integrals
	R = 0.392
	N = 1000
	rlist = np.linspace(r1,r2,N+1)
	dr = (r2-r1)/N
	zn_mode = np.zeros((len(rlist),len(position)))
	for j in range(0,len(rlist)):
		full_zn_vals = capi.calc_zn(order,rlist[j]/R,0)
		for k in range(0,len(position)):
			zn_mode[j,k] = full_zn_vals[position[k]]
	tal_at_pos_mat = np.mat(tal_at_pos)
	normvec_mat = np.mat(normvec)
	tal_at_pos_mat = np.multiply(tal_at_pos_mat,normvec_mat)
	estimate = zn_mode*np.transpose(tal_at_pos_mat)
	estimate= np.squeeze(np.asarray(estimate))
	integral = 2*np.pi*np.trapz(np.multiply(estimate,rlist),rlist)

	return integral


def rRMSE(P,T,ringnum):
# Caculate relative RMSE
# P: testing results
# T: reference
# ringnum: number of rings
# err: Errors
	# print(P)
	# print(T)
	err = 0
	for j in range(0,ringnum):
		err += (P[j]/T[j]-1)**2
	err = np.sqrt(err/ringnum)
	return err

def RMSE(P,T,ringnum):
# Caculate RMSE
# P: testing results
# T: reference
# ringnum: number of rings
# err: Errors
	err = 0
	for j in range(0,ringnum):
		err += (P[j]-T[j])**2
	err = np.sqrt(err/ringnum)
	return err

def tRMSE(P,T,ringnum):
# Caculate RMSE
# P: testing results
# T: reference
# ringnum: number of rings
# err: Errors
	err = 0
	for j in range(0,ringnum):
		err += (P[j]-T[j])**2
	err = np.sqrt(err)/100
	return err

def shrink(ref,plnnum):
	refpln = len(ref)
	ratio = int(refpln/plnnum)
	print("ratio: ",ratio)
	output = np.zeros(plnnum)
	for i in range(0,plnnum):
		temp = ref[i*ratio:(i+1)*ratio]
		output[i] = np.sum(temp)
	return output

def loadreference(plnnum):
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
	realref = shrink(ref,plnnum)
	
	return realref