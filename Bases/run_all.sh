#!/bin/bash
set -xo
I_PATH=$(pwd)
SIESTA=siesta-4.1.5
NPROC=4


for BASE in Adenine Cytosine Guanine Thymine 
do
	cd $I_PATH/${BASE}/${BASE}_Infinity
	mpirun -np $NPROC $SIESTA < ${BASE}.fdf > ${BASE}.out
	cd $I_PATH/${BASE}/${BASE}_Single_Point
	mpirun -np $NPROC $SIESTA < ${BASE}.fdf > ${BASE}.out
	cd $I_PATH/${BASE}/Relaxation_Process/Try1
	mpirun -np $NPROC $SIESTA < ${BASE}.fdf > ${BASE}.out
	cd $I_PATH/${BASE}/Relaxation_Process/Try2
	mpirun -np $NPROC $SIESTA < ${BASE}.fdf > ${BASE}.out
done


