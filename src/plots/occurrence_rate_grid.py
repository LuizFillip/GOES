import pandas as pd 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from scipy.ndimage import gaussian_filter
import GEO as gg
import datetime as dt 
import GOES as gs 
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

    counts = (
        df.groupby(["lon_bin", "lat_bin"])
          .size()
          .to_frame("hits")
          .reset_index()
    )
    counts["occurrence_%"] = (
        counts["hits"] / n_total
        ) * 100
    values = "occurrence_%"
        
    grid = pd.pivot_table(
        counts,
        index = "lat_bin",
        columns = "lon_bin",
        values = values 
    )

    return grid.fillna(0)

def occurrence_kernel_smooth(
        nl_season, 
        lon_bins, 
        lat_bins, 
        sigma = 1.5
        ):
    
    n_total = len(nl_season.index.unique())
    
    grid = occurrence_rate_grid(
        nl_season,
        lon_bins,
        lat_bins,
        n_total  
    )

    smooth = gaussian_filter(grid.values, sigma = sigma)

    return pd.DataFrame(
        smooth,
        index = grid.index,
        columns = grid.columns
    )

def get_bins(nl, step = 2):
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    return lon_bins, lat_bins 



def map_defout(
        figsize = (16, 12),
        ncols = 2, 
        grid = False, 
        lon_min = -80, 
        lon_max = -30, 
        lat_min = -60,
        lat_max = 10,
        wspace = 0.2
        ):
    
    fig, axs = plt.subplots(
        dpi = 300, 
        ncols = ncols,
        sharex = True, 
        figsize = figsize,
        subplot_kw = {"projection": ccrs.PlateCarree()},
    )
    
    
    lats = dict(min = lat_min, max = lat_max, stp = 10)
    lons = dict(min = lon_min, max= lon_max, stp = 15)
    
    xlocs = np.arange(lons['min'], lons['max'], 4)
    ylocs = np.arange(lats['min'], lats['max'], 4)
   
    if ncols > 1:
        plt.subplots_adjust(wspace = wspace)
        for i, ax in enumerate(axs):
            gg.map_attrs(
                ax, None, 
                lat_lims = lats, 
                lon_lims = lons, 
                grid = False, 
                degress = None
                )
            if grid:
                ax.gridlines(
                    xlocs = xlocs,
                    ylocs = ylocs,
                    linewidth=1,
                    color='k',
                    linestyle='--'
                )
            
            if i !=0:
                ax.set( 
                  
                    yticklabels = [], 
                    ylabel = ''
                    )
    else:
        gg.map_attrs(
            axs, None, 
            lat_lims = lats, 
            lon_lims = lons, 
            grid = False, 
            degress = None
            )
     
    
    return fig, axs
    

def plot_elipses_from_catalog(ax, nl):
    for _, row in nl.iterrows():
        x0, x1 = row["lon_min"], row["lon_max"]
        y0, y1 = row["lat_min"], row["lat_max"]
        
        gs.add_ellipse_from_bbox(
            ax,
            x0, x1,
            y0, y1
            )
        
        my = (x0 + x1) / 2
        mx = (y0 + y1) / 2
        
        ax.scatter(mx, my, color = 'red')
        


def plot_occurrence_rate_grid(
        ax,
        nl,
        lon_bins,
        lat_bins, 
        cmap = 'jet', 
        vmax = 30 
        ):
    
    n_total = len(nl.index.unique())

    grid = occurrence_rate_grid(
        nl,
        lon_bins,
        lat_bins,
        n_total= n_total
    )
    
    img = ax.pcolormesh(
        grid.columns,
        grid.index,
        grid.values,
        cmap= cmap, 
        vmin = 0, 
        vmax = vmax
    ) 
    return img 
    

def plot_kernel_smooth(
        ax, nl, 
        lon_bins, 
        lat_bins, 
        sigma = 1.5
        ):
    
    grid = occurrence_kernel_smooth(
            nl, 
            lon_bins, 
            lat_bins, 
            sigma = sigma
            )
      
    img = ax.pcolormesh(
        grid.columns,
        grid.index,
        grid.values,
        cmap="jet", 
    )
        
    ax.set(title = f'Gaussian filter ($\sigma$ = {sigma})')
    
    return img




