import numpy as np

def read_xyz_file(filename):
    coordinates = []
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two lines
        for line in lines:
            parts = line.split()
            if len(parts) == 4:
                symbol, x, y, z = parts
                coordinates.append((float(x), float(y), float(z)))
    return np.array(coordinates)

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.rad2deg(np.arccos(np.dot(v1_u, v2_u)))



def main():
    file = '10G_Chain.xyz'

    coordinates = read_xyz_file(file)

    indexes = np.array([
        [18, 20, 37],
        [84, 86, 103],
        [147, 149, 166],
        [210, 212, 229],
        [273, 275, 292],
        [335, 337, 354],
        [399, 401, 418],
        [462, 464, 481],
        [525, 527, 544],
        [588, 590, 607]
    ])

    angles = []
    plane_tilt = []

    for i in range(len(indexes) - 1):
        # calculate vectors
        v1 = coordinates[indexes[i][1]] - coordinates[indexes[i][2]]
        v2 = coordinates[indexes[i + 1][1]] - coordinates[indexes[i + 1][2]]

        v3 = coordinates[indexes[i][1]] - coordinates[indexes[i][0]]
        v4 = coordinates[indexes[i + 1][1]] - coordinates[indexes[i + 1][0]]

        # tilt between planes
        n1 = unit_vector(np.cross(v1, v3))
        n2 = unit_vector(np.cross(v2, v4))

        # transform v2 vector so it lies in the n1 plane
        v2_trans = v2 - np.dot(v2, n1) * n1
        v4_trans = v4 - np.dot(v4, n1) * n1

        # append angle between 
        angles.append(angle_between(v1, v2_trans))
        angles.append(angle_between(v3, v4_trans))

        plane_tilt.append(angle_between(n1, n2))

    print('DNA strand angles')
    print('angle =', np.mean(np.array(angles)))
    print('error =', np.std(np.array(angles)))
    print('')
    print('Base pairs tilt angle')
    print('angle =', np.mean(np.array(plane_tilt)))
    print('error =', np.std(np.array(plane_tilt)))


if __name__ == '__main__':
    main()