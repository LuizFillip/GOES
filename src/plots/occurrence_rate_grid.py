import pandas as pd 
from scipy.ndimage import gaussian_filter
# import GOES as gs 
import base as b 
import numpy as np 

b.sci_format(fontsize = 20)
 

def occurrence_rate_grid(
        nl_season, 
        lon_bins, 
        lat_bins, 
        n_total
        ):

    df = nl_season.copy()

    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["lon_bin"] = pd.cut(
        df["lon"], lon_bins, 
        labels=lon_bins[:-1]
        )
    
    df["lat_bin"] = pd.cut(
        df["lat"], lat_bins, 
        labels=lat_bins[:-1]
        )

    ds = (
        df.groupby(["lon_bin", "lat_bin"])
          .size()
          .to_frame("hits")
          .reset_index()
    )
    ds["occurrence_%"] = (ds["hits"] / n_total ) * 100
    values = "occurrence_%"
        
    grid = pd.pivot_table(
        ds,
        index = "lat_bin",
        columns = "lon_bin",
        values = values 
    ).fillna(0)

    return grid

def smooth_grid(grid, sigma = 1):
 
    smooth = gaussian_filter(grid.values, sigma=sigma)
  
    
    smooth = smooth / smooth.max() * grid.max()
    
    return smooth 


def get_bins(nl, step = 2):
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    return lon_bins, lat_bins 


def plot_occurrence_rate_grid(
        ax,
        nl,
        lon_bins,
        lat_bins, 
        cmap = 'jet', 
        vmax = 30, 
        sigma = None 
        ):
    
    n_total = len(nl.index.unique())

    grid = occurrence_rate_grid(
        nl,
        lon_bins,
        lat_bins,
        n_total= n_total
    )
    
    if sigma is not None:
        values = smooth_grid(grid, sigma = sigma)
    else:
        values = grid.values
        
    img = ax.pcolormesh(
        grid.columns,
        grid.index,
        values,
        cmap= cmap, 
        vmin = 0, 
        # vmax = vmax
    ) 
    return img 
    
 

 