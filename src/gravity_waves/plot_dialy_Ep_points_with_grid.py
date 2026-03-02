import GOES as gs
import matplotlib.pyplot as plt 
import datetime as dt 
import pandas as pd
import numpy as np 
from scipy.ndimage import gaussian_filter

def average_grid(df, values = 'mean_90_110', step = 2):
    lon_min = df['lon'].min()
    lon_max = df['lon'].max()
    lat_min = df['lat'].min()
    lat_max = df['lat'].max()
    
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    df["lon_bin"] = pd.cut(
        df["lon"], lon_bins, 
        labels = lon_bins[:-1]
        )
    
    df["lat_bin"] = pd.cut(
        df["lat"], lat_bins, 
        labels=lat_bins[:-1]
        )
    
    counts = (
        df.groupby(["lon_bin", "lat_bin"])
          .mean() 
          .reset_index()
    )
     
    return pd.pivot_table(
        counts,
        index = "lat_bin",
        columns = "lon_bin",
        values = values 
    )


def smooth_grid(grid, sigma = 1.5):
    grid = grid.replace(np.nan, 0)
    
    return gaussian_filter(grid.values, sigma = sigma)

def colorbar(ax):
    cax = ax.inset_axes([1.1, 0, 0.05, 1])
     
    cb = plt.colorbar(
        img,  
        cax = cax, 
        )
    
    cb.set_label("Ep (J/kg)")

df = gs.potential_energy(year = 2013)

dn = dt.date(2013, 2, 1)
df = df.loc[df.index.date == dn]

step = 4

fig, ax = gs.map_defout(ncols = 3, wspace = 0.4)


values = 'mean_90_110'

grid = average_grid(df, values, step )

img = ax[0].scatter(
    df['lon'], 
    df['lat'], 
    c = df[values],
    s = 100, 
    cmap = 'jet'
    )

colorbar(ax[0])


ax[1].pcolormesh(
    grid.columns, 
    grid.index,
    grid.values, 
    cmap = 'jet'
    )

colorbar(ax[1])
sigma = 1.5
smooth = smooth_grid(grid, sigma = 1)

img = ax[2].pcolormesh(
    grid.columns, 
    grid.index,
    smooth, 
    cmap = 'jet'
    )

colorbar(ax[2])

ax[0].set( title = 'Raw data (SABER)')

ax[1].set( title = f'Occurrence grid ({step}x{step})')

ax[2].set( 
    title = f'Gaussian filter ($\sigma$ = {sigma})',
    
    )

fig.suptitle(dn.strftime('%Y-%m-%d'), y = 0.73)