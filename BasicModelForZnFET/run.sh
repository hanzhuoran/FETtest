#!/bin/bash
batchnum1=10
batchnum2=100
num=2
python simulation.py $batchnum1 $batchnum2 $num
python calc_err.py $batchnum1 $batchnum2 
python ploterror.py $batchnum1 $batchnum2 
python processReven.py $batchnum1 $batchnum2
