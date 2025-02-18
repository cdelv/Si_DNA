# Bases

In this directory, the optimization of single nitrogenated bases. 

## Content

* run_all.sh: Is a bash script that will run the simulations in all subdirectories.

* Base: This directory contains the relaxation process of each molecule, a single point calculation of the relaxed molecule, and a single point calculation where the coordinates of each molecule are multiplied by a large number to assess stability. 

* .XYZ files inside each directory contains the final relaxed coordinates of each molecule.

* Coordinate_Multiplayer.py: recives an input file with the SIESTA coordinates and multiplies them by a constant factor. It outputs an other file. 


### Comments

When running the infinity directories, it may not converge on the first try. But when you repeat the simulation, it should. 