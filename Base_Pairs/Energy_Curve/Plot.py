import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate, optimize

# Read the CSV file into a pandas DataFrame
#data = pd.read_csv('GC_Results.csv')
data = pd.read_csv('AT_Results.csv')

# Extract the Distance and Total Energy columns
distance = data['Distance'].to_numpy() - data['Distance'].to_numpy()[0] + 0.5

# GC
total_energy = data['Total Energy'].to_numpy()  + 2396.283550 + 1750.398574

# AT
#total_energy = data['Total Energy'].to_numpy()  + 1959.692534 + 2039.322296


# Create an interpolator for the Total Energy data
interpolator = interpolate.interp1d(distance, total_energy, kind='cubic')

# Perform optimization to find the minimum
minimum_result = optimize.minimize_scalar(interpolator, bounds=(distance.min(), distance.max()), method='bounded')
minimum_distance = minimum_result.x
minimum_total_energy = minimum_result.fun

# Plot Distance vs Total Energy
plt.plot(distance, total_energy, 'o')
plt.xlabel('Distance')
plt.ylabel('Total Energy')
plt.title('Distance vs Total Energy')
#plt.ylim(-2, 2)

# Add horizontal and vertical lines for the minimum value
plt.axhline(minimum_total_energy, color='r', linestyle='--')
plt.axvline(minimum_distance, color='r', linestyle='--')

# Add labels for the minimum value
plt.text(minimum_distance, minimum_total_energy, f'({minimum_distance:.2f}, {minimum_total_energy:.2f})',
         verticalalignment='top', horizontalalignment='left', color='black')


plt.show()