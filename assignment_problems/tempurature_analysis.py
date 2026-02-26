import numpy as np
import time

'''
======================================
Task 1: Create an Array and Basic Math
======================================
'''

temps_celsius = np.array([22,25,28,24,26])
fahrenheit_temps = temps_celsius * 1.8 + 32

print(f"Celsius: {temps_celsius}") # Celsius: [22 25 28 24 26]
print(f"Fahremhiet: {fahrenheit_temps}") # Fahremhiet: [71.6 77.  82.4 75.2 78.8]
print(f"Average Fahrenheit: {fahrenheit_temps.mean()}") # Average Fahrenheit: 77.0

'''
======================================
Task 2: Array Shape and Statistics
======================================
'''

arr = np.array([85, 90, 78, 92, 88, 76, 95, 82, 89, 91, 87, 84])

print(f"Shape: {arr.shape}") # Shape: (12,)
print(f"Total element: {arr.size}") # Total element: 12
print(f"Highest Score: {np.max(arr)}") # Highest Score: 95
print(f"Lowest Score: {np.min(arr)}") # Lowest Score: 76
# print(f"Range: {arr.max() - arr.min()}")
print(f"Range: {np.ptp(arr)}") # Range: 19 (peak-to-peak)

'''
======================================
Task 2: Array Shape and Statistics
======================================
'''

np_arr = np.arange(1,50001)
py_list = list(range(1,50001))

st_np = time.time()
np_sum = np.sum(np_arr)
end_np = time.time()
total_np_time = end_np - st_np

st_py = time.time()
py_sum = sum(py_list)
end_py = time.time()
total_py_time = end_py - st_py


print(f"NumPy Sum: {np_sum}") # NumPy Sum: 1250025000
print(f"Python Sum: {py_sum}") # Python Sum: 1250025000
print(f"NumPy Time: {total_np_time:.4f}") # NumPy Time: 0.0000
print(f"Python Time: {total_py_time:4f}") # Python Time: 0.000152
print(f"Numpy is {total_py_time/total_np_time:.1f} faster") # Numpy is 18.8 faster
'Note: Time Varies for each operation'