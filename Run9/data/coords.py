import numpy as np 


data = np.loadtxt('coords.txt',
	dtype={'names': ('X', 'Y', 'Z', 'S'),'formats': ('f', 'f', 'f','f')})

print(len(data['X']))
print(min(data['X']))
print(min(data['Y']))
print(min(data['Z']))