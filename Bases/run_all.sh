#!/bin/bash
set -xo
I_PATH=$(pwd)
SIESTA=siesta-4.1.5
NPROC=2


for BASE in Adenine Cytosine Guanine Thymine 
do
	cd $I_PATH/${BASE}
	mpirun -np $NPROC $SIESTA < ${BASE}.fdf > ${BASE}.out
done

