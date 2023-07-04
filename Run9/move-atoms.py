import numpy as np
import sys
from scipy.spatial.transform import Rotation as R


def move(coordinates, move_d):
	for i in coordinates:
		i-=move_d

def print_c(coordinates):
	print('')
	print('---------------- New Coordinates -------------------------')
	print('')
	fmt = '%1.6f', '%1.6f', '%1.6f', '%d'
	np.savetxt(sys.stdout.buffer, coordinates, fmt=fmt)

def read_data(atoms):
	n_rows = input("number of atoms: ")
	n_columns = 4

	for i in range(int(n_rows)):
		a =[float(x) for x in input().split()[:4]]
		atoms.append(a)



def read_data_file(atoms,file):
	with open(file) as f:
		for line in f:
			lines =[float(x) for x in line.split()[:4]]
			atoms.append(lines)
	f.close()

def rootate(angle, rot_axis, coordinates, Rad=False):

	if Rad:
		rotation_radians = angle
	else:
		rotation_radians = np.radians(angle)

	rotation_axis = np.array(rot_axis)
	rotation_vector = rotation_radians * rotation_axis
	rotation = R.from_rotvec(rotation_vector)

	for i in coordinates:
		vec = np.array([i[0], i[1], i[2]])
		rotated_vec = rotation.apply(vec)
		i[0], i[1], i[2] = rotated_vec

def move_vec(x1,x2,d):
	vec = d*(x2-x1)/np.linalg.norm(x2-x1)
	return vec

def plain(coordinates, y):
	x = coordinates[0]
	if x[2]<0:
		val=1
	else:
		val=-1

	x_angle = val*np.arcsin(x[2]/(np.sqrt(x[1]*x[1]+x[2]*x[2])))
	rootate(x_angle, np.array([1,0,0]), coordinates, True)

	y_angle = val*np.arcsin(x[2]/(np.sqrt(x[0]*x[0]+x[2]*x[2])))
	rootate(y_angle, np.array([0,1,0]), coordinates, True)


def main():
	atoms = []

	Move = True
	Rotate = False
	Vec = False
	Plain = False

	x=[-14.870482 , -5.8861465 , -3.6191788]

	angle = 20 #degrees
	rot_axis = [0,0,1] 


	vec1 = [0,0,2]
	vec2 = [0,0,1]
	d = 4

	move_c = [ -14.870482 , -5.890042 , -3.344028, 0]
	to = [ 0.0 , 0.0, 0.0, 0]

	x1 = np.array(vec1)
	x2 = np.array(vec2)


	#read_data(atoms)
	read_data_file(atoms,'coords.txt')
	coordinates = np.array(atoms)
	aux_move = np.array(move_c)
	aux_to = np.array(to)
	move_d = aux_move - aux_to

	if Vec:
		move(coordinates, move_vec(x1,x2,d))

	if Move:
		move(coordinates, move_d)

	if Rotate:
		rootate(angle, rot_axis, coordinates)

	if Plain:
		plain(coordinates, x)

	print_c(coordinates)

if __name__ == '__main__':
	main()

