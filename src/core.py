import gzip
import numpy as np
import xarray as xr

import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
# import base as b

def read_gzbin(f_name):
 
    with gzip.open(f_name, 'rb') as f:
        
        dados_binarios = np.frombuffer(
            f.read(), 
            dtype = np.int16
            )

        imageSize = [1714, 1870]
        

        data_bin = dados_binarios.reshape(imageSize)
    
        return data_bin / 100 - 273.13



ds = xr.open_dataset('S10635336_202110231400.nc')
data = ds['Band1'].values / 10 - 273.13
data 

fig, ax = plt.subplots(
    dpi = 300,
    figsize = (9, 9),
    subplot_kw = 
        {
        'projection': ccrs.PlateCarree()
        }
    )

gg.map_features(ax)

lat = gg.limits(
    min = -70, 
    max = 40, 
    stp = 10
    )
lon = gg.limits(
    min = -120, 
    max = -20, 
    stp = 10
    )    

gg.map_boundaries(ax, lon, lat)

# plot_sites_and_meridians(ax, year)

gg.mag_equator(
    ax,
    2013,
    degress = None
    )

data[(data < -200) | (data > 0)] = np.nan 

img = ax.contourf(
    ds['lon'], ds['lat'],
         data, cmap = 'rainbow')

plt.colorbar(img)
