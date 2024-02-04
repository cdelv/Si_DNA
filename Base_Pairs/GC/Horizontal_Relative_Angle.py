import numpy as np

def load_coordinates(coord_file, atom1, atom2):
	with open(coord_file, 'r') as file:
		lines = file.readlines()

		atom_1_coords = np.array(list(map(float, lines[atom1 + 2].split()[1:4])))
		atom_2_coords = np.array(list(map(float, lines[atom2 + 2].split()[1:4])))

	return atom_2_coords - atom_1_coords


def main(coord_file, atom1, atom2):
	horizontal = load_coordinates(coord_file, 22, 10)
	vec = load_coordinates(coord_file, atom1, atom2)
	angle = np.arccos(np.dot(vec,horizontal)/(np.linalg.norm(vec)*np.linalg.norm(horizontal)))
	print("Angle =", np.rad2deg(angle))
	print("Distance =", np.linalg.norm(vec))



if __name__ == '__main__':
	main("GC.xyz", 12,25)