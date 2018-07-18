	
def fet_func(w,coeff,pos):
	order = len(pos)-1
	for i in range(0,len(w)+1):
		full_zn_vals = capi.calc_zn(order,w[i]/R,0)
		rn_at_pos = hf.get_val_at_pos(pos,full_zn_vals)
		y[i] = np.sum(np.multiply(coeff,rn_at_pos))

	
	
	return y