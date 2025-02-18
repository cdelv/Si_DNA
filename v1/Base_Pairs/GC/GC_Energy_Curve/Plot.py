import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate, optimize

df = pd.read_csv('GC_Results.csv')
df = df[df['energy'] != 0]
distance = df['distance'].to_numpy()
energy = df['energy'].to_numpy() + 4146.079181


interpolator = interpolate.interp1d(distance, energy, kind='cubic', fill_value='extrapolate')
def find_min(x):
    return interpolator(x)

result = optimize.minimize_scalar(find_min, bounds=(distance.min(), distance.max()))
min_distance = result.x
min_energy = result.fun

sigma = min_distance/(2**(1/6))
epsilon = -min_energy
print(sigma)

def Lennard_Jones(x):
	return 4*epsilon*((sigma/x)**12 - (sigma/x)**6)

plt.figure(figsize=(8, 6))
plt.plot(distance, energy, marker='o', linestyle='-', label='Data')
plt.plot(min_distance, min_energy, 'ro', label='Minimum')
#plt.plot(distance, Lennard_Jones(distance), 'r--', label='Lennard-Jones Fit')
plt.title('Distance vs Energy')
plt.xlabel('Distance')
plt.ylabel('Energy')
plt.ylim(ymin=-3, ymax=4)
plt.grid(True)
plt.legend()
plt.show()

print(f"Location of the minimum: {min_distance}")
print(f"Depth of the minimum: {min_energy}")