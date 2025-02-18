#!/bin/bash

I_path=$(pwd)

for dir in Adenine_VDW_OP Cytosine_VDW_OP Guanine_VDW_OP Thymine_VDW_OP; do
  echo "Processing directory: $dir"

  # Change to the directory
  cd $I_path/$dir

  # Find the .fdf file and run the siesta command
  fdf_file=$(ls *.fdf)
  out_file="${fdf_file%.fdf}.out"

  mpirun -np 32 siesta-5 < $fdf_file > $out_file

  echo "Done"

  cd $I_path
done