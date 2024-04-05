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

def main():
    file = '10G_Chain.xyz'

    coordinates = read_xyz_file(file)

    indexes_h = [
        [13, 16, 20, 23, 26, 34, 37, 28],
        [583, 586, 590, 593, 596, 604, 607, 598]
    ] 
    h = []

    indexes_l = [
        [55, 120, 183, 246, 309, 372, 435, 498, 561, 626],
        [60, 125, 188, 251, 314, 377, 440, 503, 566, 631]
    ]
    l = []

    for i in range(len(indexes_h[0])):
        h.append(np.linalg.norm(coordinates[indexes_h[0][i]] - coordinates[indexes_h[1][i]]))

    for i in range(len(indexes_l[0])):
        l.append(np.linalg.norm(coordinates[indexes_l[0][i]] - coordinates[indexes_l[1][i]]))

    h = np.array(h)
    l = np.array(l)

    print('DNA strand dimensions')
    print('height =', np.mean(h))
    print('error =', np.std(h))
    print('')
    print('length =', np.mean(l))
    print('error =', np.std(l))


if __name__ == '__main__':
    main()