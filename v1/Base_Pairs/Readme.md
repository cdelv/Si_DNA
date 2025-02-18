# Bases

In this directory, the optimization of nitrogenated base pairs and the energy curve to asses their bonding energy. 

## Content

### Base Pair:

* Relaxation Process: Directory containing the relaxation simulations required to go from the individual bases to a stable base pair.

* Energy_Curve: Contains a Python script that allows you to adjust the distance between base pairs resulting from the Relaxation process and run a single point calculation for each distance. It includes all the individual simulations and a results.csv file that summarizes all the outputs. There are also scripts to plot the results and create a .fdf file with the optimal distance.

* Energy_Optimized: A relaxation simulation using the optimal .fdf file from Energy_Curve. 

* *.xyz: The optimized geometry from the simulation in Energy_Optimized.