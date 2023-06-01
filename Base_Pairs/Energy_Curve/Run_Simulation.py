import os
import re
import csv
import glob
import shutil
import subprocess
import numpy as np

# Index as in SIESTA fdf, ie., starts at 1
GC_params = ["GC.fdf", 16, 1, 27, "Energy_GC_", "GC"]
AT_params = ["AT.fdf", 15, 11, 27, "Energy_AT_", "AT"]

def main():
    # User defined Parameters
    PARAMS = AT_params
    Nproc = 6

    # Reference atoms
    File = PARAMS[0]
    num_atoms_molecule_1 = PARAMS[1]
    atom1_index = PARAMS[2]
    atom2_index = PARAMS[3]

    # Calculate displacement vector
    coordinates, _ = load_atomic_coordinates(File)
    offset_vector = np.array(calculate_vector(coordinates, atom1_index, atom2_index))
    distance = np.linalg.norm(offset_vector)
    offset_vector /= distance # make it unitary

    # Simulation range parameters
    num_steps = 40
    start_scaling_factor = -distance + 0.5  # Initial scaling factor: 0.5 ang distance
    end_scaling_factor = -distance + 6.0    # Final scaling factor:   6.0 ang distance

    # Get current directory
    current_directory = os.path.abspath(os.path.dirname(__file__))

    # Distances between the 2 molecules
    scaling_factors = np.linspace(start_scaling_factor, end_scaling_factor, num_steps)

    # Run the simulation for each distance
    step = 0
    for scaling_factor in scaling_factors: #scaling_factors:
        os.chdir(current_directory) # Make sure we are in the correct directory

        # Get atomic coordinates from fdf file
        atomic_coordinates, species_indices = load_atomic_coordinates(File)

        # Get the coordinates of each molecule
        molecule1_coordinates = atomic_coordinates[:num_atoms_molecule_1]
        molecule2_coordinates = atomic_coordinates[num_atoms_molecule_1:]

        # Add the offset to molecule 2
        for i in range(len(molecule2_coordinates)):
            molecule2_coordinates[i] = [molecule2_coordinates[i][j] + scaling_factor*offset_vector[j] for j in range(3)]

        # Create the new directory for the SIESTA simulation
        step += 1 
        New_dir = PARAMS[4]+str(step)
        create_directory(New_dir)
        create_fdf_file(File, os.path.join(New_dir, File), molecule1_coordinates, molecule2_coordinates, species_indices)
        
        # Copy the pseudopotentials to the new file
        pseudos_dir = os.path.join(current_directory, "..", "..", "Pseudos")
        matching_files = glob.glob(os.path.join(pseudos_dir, "*.psf"))
        for file in matching_files:
            shutil.copy(file, os.path.join(New_dir, os.path.basename(file)))

        # Run the simulation
        os.chdir(New_dir)
        subprocess.run('mpirun -np ' + str(Nproc) + ' siesta-4.1.5 < ' + File + ' > File.out', shell=True)

    # Extract total energy from each simulation directory
    os.chdir(current_directory)  # Make sure we are in the correct directory
    directories = glob.glob(PARAMS[4]+"*")

    # Get the total energies
    energies = []
    for directory in directories:
        total_energy = extract_total_energy(directory)
        energies.append(total_energy)

    # Write distances and energies to a CSV file
    csv_file = PARAMS[5]+"_Results.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Distance', 'Total Energy'])
        writer.writerows(zip(scaling_factors, energies))


def calculate_vector(coordinates, atom1_index, atom2_index):
    atom1_coords = coordinates[atom1_index - 1]
    atom2_coords = coordinates[atom2_index - 1]

    vector = [atom2_coords[i] - atom1_coords[i] for i in range(3)]
    return vector

def extract_total_energy(directory, file="File.out"):
    output_file = os.path.join(directory, file)
    total_energy = None

    with open(output_file, 'r') as f:
        for line in f:
            match = re.search(r'Total =\s+(-?\d+\.\d+)', line)
            if match:
                total_energy = float(match.group(1))
                break

    return total_energy

def create_directory(directory_path):
    if os.path.exists(directory_path):
        # Directory already exists, delete its contents
        shutil.rmtree(directory_path)

    # Create the directory
    os.makedirs(directory_path)

def create_fdf_file(original_file, new_file, molecule1_coordinates, molecule2_coordinates, species_indices):
    with open(original_file, 'r') as f:
        file_contents = f.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(file_contents):
        if line.strip() == '%block AtomicCoordinatesAndAtomicSpecies':
            start_index = i
        elif line.strip() == '%endblock AtomicCoordinatesAndAtomicSpecies':
            end_index = i
            break

    if start_index is None or end_index is None:
        print('AtomicCoordinatesAndAtomicSpecies block not found in the original file.')
        return

    coordinates_block = file_contents[start_index + 1: end_index]
    molecule1_block = [f'{coord[0]:<15.9f}{coord[1]:<15.9f}{coord[2]:<15.9f}{species_indices[i]:>4}\n' for i, coord in enumerate(molecule1_coordinates)]
    molecule2_block = [f'{coord[0]:<15.9f}{coord[1]:<15.9f}{coord[2]:<15.9f}{species_indices[i + len(molecule1_coordinates)]:>4}\n' for i, coord in enumerate(molecule2_coordinates)]
    new_contents = file_contents[:start_index + 1] + molecule1_block + molecule2_block + file_contents[end_index:]

    with open(new_file, 'w') as f:
        f.writelines(new_contents)

def load_atomic_coordinates(file_path):
    atomic_coordinates = []
    species_indices = []

    with open(file_path, 'r') as f:
        # Search for the start of the block
        for line in f:
            if line.strip() == '%block AtomicCoordinatesAndAtomicSpecies':
                break
        else:
            # Block not found
            return None

        # Read atomic coordinates until the end of the block
        for line in f:
            line = line.strip()
            if line == '%endblock AtomicCoordinatesAndAtomicSpecies':
                break

            # Split the line into coordinate values and species index
            values = line.split()
            coordinates = [float(value) for value in values[:3]]
            species_index = int(values[3])
            atomic_coordinates.append(coordinates)
            species_indices.append(species_index)

    return atomic_coordinates, species_indices


if __name__ == '__main__':
    main()
