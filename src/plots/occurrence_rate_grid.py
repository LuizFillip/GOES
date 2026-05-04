import pandas as pd 
from scipy.ndimage import gaussian_filter
import base as b 
import numpy as np 
import matplotlib.pyplot as plt
import GEO as gg 
import cartopy.crs as ccrs
import datetime as dt 

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
    
    if isinstance(grid, pd.DataFrame):
        grid  = grid.values
    else:
        grid = grid.copy()
        
    smooth = gaussian_filter(grid, sigma=sigma)
  
    
    smooth = smooth / smooth.max() * np.nanmax(grid)
    
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
        n_total,
        cmap = 'jet', 
        vmax = 30, 
        sigma = None 
        ):
    
   

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
    ) 
     
    return img 
    
 

df = b.load('GOES/data/nucleos_40/2013')

def set_bins(nl, step = 4):
    
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    return lon_bins, lat_bins 
 

def plot_grid_and_interp_maps():
    fig, ax = plt.subplots(
         dpi=300,
         figsize=(10, 10),
         ncols = 2,
         subplot_kw={"projection": ccrs.PlateCarree()},
     )
    
    dn = dt.date(2013, 12, 24)
    
    lat_lims = dict(min=-60, max=10, stp=10)
    lon_lims = dict(min=-90, max=-30, stp=10)
    
    
    nl = df.loc[df.index.date == dn]
    # print(
    total_month = df.loc[df.index.month == dn.month]
    n_total = len(total_month.index.unique())
    # n_total = len(nl.index.unique())
    
    lon_bins, lat_bins  = set_bins(nl)
    
    sigma = [None, 2]
    titles = ['Grid 4 x 4', 'Gaussian interpolation']
    for i, a in enumerate(ax.flat):
        gg.map_attrs(
            a,
            year=None,
            lat_lims=lat_lims,
            lon_lims=lon_lims,
            grid=False,
            degress=None,
        )
        
        img = plot_occurrence_rate_grid(
                ax[i],
                nl,
                lon_bins,
                lat_bins, 
                n_total, 
                cmap = 'turbo', 
                vmax = 30, 
                sigma = sigma[i]
                )
        
        ax[i].set(title = titles[i])
        # plt.colorbar(img)
        
    
    ax[1].set(yticklabels = [], ylabel = '')
    
    b.colorbar(
            img, 
            ax[1], 
            # ticks, 
            label = 'Occurrence rate (\%)', 
            height = "100%", 
            width = "5%",
            orientation = "vertical", 
            anchor = (.2, 0., 1, 1)
            )
    
    fig.suptitle(dn.strftime('%Y-%m-%d'), y = 0.8)
 

