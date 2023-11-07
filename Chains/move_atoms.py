import numpy as np
from scipy.spatial.transform import Rotation

def read_xyz_file(filename):
    coordinates = []
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two lines
        for line in lines:
            parts = line.split()
            if len(parts) == 4:
                symbol, x, y, z = parts
                coordinates.append((symbol, float(x), float(y), float(z)))
    return coordinates

def write_xyz_file(filename, coordinates):
    with open(filename, 'w') as file:
        file.write(f"{len(coordinates)}\n")
        file.write("Properties=species:S:1:pos:R:3 XYZ=T pbc=\"F F F\"\n")
        for symbol, x, y, z in coordinates:
            file.write(f"{symbol:>2} {x:.8f} {y:.8f} {z:.8f}\n")

def add_point(coordinates, point):
    new_coordinates = [(symbol, x + point[0], y + point[1], z + point[2]) for symbol, x, y, z in coordinates]
    return new_coordinates

def subtract_point(coordinates, point):
    new_coordinates = [(symbol, x - point[0], y - point[1], z - point[2]) for symbol, x, y, z in coordinates]
    return new_coordinates

def rotate_coordinates(coordinates, axis, angle_degrees):
    r = Rotation.from_euler(axis, angle_degrees, degrees=True)
    new_coordinates = []
    
    for symbol, x, y, z in coordinates:
        vector = np.array([x, y, z])
        rotated_vector = r.apply(vector)
        new_coordinates.append((symbol, rotated_vector[0], rotated_vector[1], rotated_vector[2]))
    return new_coordinates

def merge_xyz_files(input_filename1, input_filename2, output_filename):
    # Read coordinates from the first file
    coordinates1 = read_xyz_file(input_filename1)
    
    # Read coordinates from the second file
    coordinates2 = read_xyz_file(input_filename2)
    
    # Merge the coordinates from both files
    merged_coordinates = coordinates1 + coordinates2
    
    # Write the merged coordinates to the output file
    write_xyz_file(output_filename, merged_coordinates)

if __name__ == '__main__':
    input_filename = '5G_Chain.xyz'
    output_filename = '5G_Chain2.xyz'

    new_coordinates = read_xyz_file(input_filename) # 40.7564
    case = 1

    if case == 1:
        new_coordinates = rotate_coordinates(new_coordinates, 'z', 39.54265413838987*5)

        molec_n = 58
        point = (new_coordinates[molec_n][1], new_coordinates[molec_n][2], new_coordinates[molec_n][3])
        new_coordinates = subtract_point(new_coordinates, point)

        point = (-2.3212, -1.8897, 21.4295)
        new_coordinates = add_point(new_coordinates, point)

        write_xyz_file(output_filename, new_coordinates)
        merge_xyz_files(input_filename, output_filename, '5G_Chain3.xyz')

    elif case == 2:
        new_coordinates = rotate_coordinates(new_coordinates, 'z', 180.0)

        molec_n = 319
        point = (new_coordinates[molec_n][1], new_coordinates[molec_n][2], new_coordinates[molec_n][3])
        new_coordinates = subtract_point(new_coordinates, point)

        point = (0.0, 0.0, 44.7564)
        new_coordinates = add_point(new_coordinates, point)

        molec_n = 310
        point = (new_coordinates[molec_n][1], new_coordinates[molec_n][2], 0)
        a = (4.3688, 19.5970, 0)

        angle_a = np.degrees(np.arctan2(a[1], a[0]))
        angle_b = np.degrees(np.arctan2(point[1], point[0]))
        new_coordinates = rotate_coordinates(new_coordinates, 'z', angle_a)
        new_coordinates = rotate_coordinates(new_coordinates, 'z', -angle_b)

        print(np.degrees(np.arctan2(a[1], a[0])))
        point = (new_coordinates[molec_n][1], new_coordinates[molec_n][2], 0)
        print(np.degrees(np.arctan2(point[1], point[0])))

        write_xyz_file(output_filename, new_coordinates)
        merge_xyz_files(input_filename, output_filename, '5G_Chain3.xyz')