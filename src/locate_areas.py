# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:16:14 2023

@author: Luiz
"""

def find_regions_below_threshold_2d(arr, threshold):
    regions = []  # List to store the regions

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] < threshold:
                start_i, start_j = i, j  # Start of a new region
                end_i, end_j = i, j

                # Expand the region horizontally
                while end_j + 1 < len(arr[i]) and arr[i][end_j + 1] < threshold:
                    end_j += 1

                # Check vertically within the same row
                for row in range(i + 1, len(arr)):
                    valid = True
                    for col in range(start_j, end_j + 1):
                        if arr[row][col] >= threshold:
                            valid = False
                            break
                    if valid:
                        end_i = row
                    else:
                        break

                # Store the region
                regions.append(((start_i, start_j), (end_i, end_j)))

    return regions

# Example usage with a 2D array:
my_2d_array = [
    [2, 3, 1, 0, 4],
    [2, 1, 5, 6, 2],
    [0, 3, 4, 5, 2]
]

threshold_value = 3

result = find_regions_below_threshold_2d(my_2d_array, threshold_value)
print(result)
