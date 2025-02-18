import numpy as np 
import pandas as pd
import os
import shutil
import subprocess

# 0-12 C
# 13-28 G
# 22 - 10 -> H_g - N_c
# 20 - 8 -> O_g - H_c
# 25 - 12 -> H_g - O_c
FDF_FILE = "GC.fdf"
OUT_FILE = "GC.out"
PATH = os.getcwd()
NPROC = 4

def Load_Coordinates():
    with open(FDF_FILE, "r") as fdf_file:
        lines = fdf_file.readlines()

    inside_block = False
    atomic_coordinates = []
    atomic_species = []
    for line in lines:
        words = line.strip().split()

        if "%block AtomicCoordinatesAndAtomicSpecies" in line:
            inside_block = True
            continue

        if "%endblock AtomicCoordinatesAndAtomicSpecies" in line:
            inside_block = False

        if inside_block:
            x, y, z, species_index, number, species_symbol = words
            atomic_coordinates.append([float(x), float(y), float(z)])
            atomic_species.append([int(species_index), int(number), species_symbol])

    return np.array(atomic_coordinates), atomic_species

def Write_fdf_File(out_name, atomic_coordinates, atomic_species):
    with open(os.path.join(PATH, FDF_FILE), "r") as fdf_file:
        lines = fdf_file.readlines()

    inside_block = False
    done = False
    with open(out_name, "w") as new_fdf_file:
        for line in lines:

            if "%block AtomicCoordinatesAndAtomicSpecies" in line:
                inside_block = True
                new_fdf_file.write(line)
                continue

            if "%endblock AtomicCoordinatesAndAtomicSpecies" in line:
                inside_block = False

            if inside_block and not done:
                done = True
                for coords, species in zip(atomic_coordinates, atomic_species):
                    x, y, z = coords
                    species_index, number, species_symbol = species
                    new_fdf_file.write(f"    {x} {y} {z}  {species_index}  {number}  {species_symbol}\n")
            elif not inside_block:
                new_fdf_file.write(line)

def Meassure_Distance(atomic_coordinates, atom1, atom2):
    return np.linalg.norm(atomic_coordinates[atom2] - atomic_coordinates[atom1])

def Move_Molecule(atomic_coordinates, vector, distance, start, end):
    for i in range(start, end):
        atomic_coordinates[i] += distance*vector

def Calculate_Vector(atomic_coordinates, atom1, atom2):
    v = atomic_coordinates[atom2] - atomic_coordinates[atom1]
    v /= np.linalg.norm(v)
    return v

def main():
    atomic_coordinates, atomic_species = Load_Coordinates()

    v1 = Calculate_Vector(atomic_coordinates, 22, 10)
    v2 = Calculate_Vector(atomic_coordinates, 20, 8)
    v3 = Calculate_Vector(atomic_coordinates, 25, 12)
    v = (v1 + v2 + v3)/3
    v /= np.linalg.norm(v)

    base_distance = Meassure_Distance(atomic_coordinates, 22, 10)
    distance = 2.1002953262910853 - base_distance
    print(distance)
    Move_Molecule(atomic_coordinates, v, distance, 0, 13)
    Write_fdf_File("Energy_Optimized_GC.fdf", atomic_coordinates, atomic_species)


if __name__ == '__main__':
    main()