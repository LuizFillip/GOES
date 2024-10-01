# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:38:34 2024

@author: Luiz
"""

# glon, glat, grid = grid_mean(
#     lon, lat, data, 
#     grid_size = 100
#     )

# ns = ['lon', 'lat', 'temp']

# ds = pd.DataFrame(
#     structured_data(glon, glat, grid), 
#     columns = ns
#     )

# ds['date'] = fname2date(fname)

# # ax = gs.map_attrs(glon, glat, grid)

# vls = ds.loc[ds['temp'] < -50].min()

# clon, clat = gg.plot_square_area(
#         ax, 
#         lat_min = vls['lat'].min(), 
#         lon_min = vls['lon'].min(),
#         lat_max = None, 
#         lon_max = None, 
#         radius = 7
#         )

# import matplotlib.pyplot as plt


# clat = vls['lat']
# clon = vls['lon']

# circle = plt.Circle(
#     (clon, clat), 
#     5, 
#     lw =2,
#     edgecolor = 'red', 
#     color = 'red', 
#     )

# plt.gca().add_patch(circle)

ds 