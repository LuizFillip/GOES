# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, find_objects

# Example array (replace this with your actual array)
data = np.zeros((10, 10)) * np.nan


data[3:6, 2:6] = 4

data[7:9, 7:9] = 15

data[:2, :2] = 10


# Step 1: Create a binary mask of non-NaN values
non_nan_mask = ~np.isnan(data)

# Step 2: Label connected non-NaN regions
labeled_array, num_features = label(non_nan_mask)

# Step 3: Get bounding boxes for each labeled region
slices = find_objects(labeled_array)

plt.imshow(
    data, 
    aspect = 'auto', 
    interpolation='none')

step = 0.5
for i, region in enumerate(slices):
   
    y_start, x_start = region[0].start - step, region[1].start - step
    y_end, x_end = region[0].stop - step, region[1].stop - step
    
    
    rect = plt.Rectangle(
        (x_start, y_start), 
        x_end - x_start, y_end - y_start,
        edgecolor = 'red', 
        facecolor = 'none', 
        linewidth = 2 
        )
    
    plt.gca().add_patch(rect)


plt.show()


num_features