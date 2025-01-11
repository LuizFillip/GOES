# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:25:00 2025

@author: Luiz
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Example data

num = 1
lats = np.linspace(30, 90, 100)  # Latitude from 30°N to 90°N
lons = np.linspace(-180, 180, 100)  # Longitude from -180° to 180°
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Cria dados sintéticos (por exemplo, uma função sinusoidal para representar anomalias)
data = 50 * np.sin(2 * np.pi * lon_grid / 180) * np.cos(np.pi * (lat_grid - 60) / 30)

# Flatten the arrays
# lons = lons.flatten()
# lats = lats.flatten()

# Create a polar stereographic projection for the Northern Hemisphere
projection = ccrs.NorthPolarStereo()

# Create a figure and a set of subplots
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': projection})

# Set up the map with coastlines and features
ax.coastlines(resolution='110m', linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
ax.set_extent([-180, 180, 30, 90], crs=ccrs.PlateCarree())  # Limit map extent

# Add gridlines with latitudinal labels
gridlines = ax.gridlines(
    draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--'
)
gridlines.top_labels = False
gridlines.right_labels = False
gridlines.ylocator = plt.FixedLocator([30, 40, 50, 60, 70, 80, 90])  # Latitudinal lines
gridlines.xlabel_style = {'size': 10}
gridlines.ylabel_style = {'size': 10}

# Plot the data as a scatter plot
scatter = ax.contourf(
    lons, lats, data, transform=ccrs.PlateCarree(), cmap='coolwarm'
)

# Add a colorbar
cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.7, pad=0.1)
cbar.set_label('Data Value', size=12)

# Set title
ax.set_title('Scatter Plot over Northern Hemisphere (30°N to 90°N)', fontsize=14)

# Show the plot
plt.show()