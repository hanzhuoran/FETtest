#!/bin/bash
batchnum=100
python simulation.py $batchnum
python calc_err.py $batchnum
python ploterror.py $batchnum
python processReven.py $batchnum
