import pandas as pd 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import datetime as dt 
import GOES as gs 
 

def plot_steps_for_grid_occurrence(dn):
    fn = gs.get_path_by_dn(dn)
    
    lon, lat, temp = gs.read_gzbin(fn)
    
    nl = gs.find_nucleos(       
        lon,
        lat,
        temp,
        dn=None,
        temp_threshold= -40,
    )
    
    lon_bins, lat_bins = gs.get_bins(nl, step = 2)
    
    fig, ax  =  gs.map_defout(ncols = 3)
    
    img = ax[0].pcolormesh(
        lon, lat, temp,
        vmin = -100, 
        vmax = 100,
        cmap= gs.goes_cmap(), 
    )
    
    ax[0].set(title = 'Top cloud temperature')
        
    gs.plot_occurrence_rate_grid(
            ax,
            nl,
            lon_bins,
            lat_bins, 
            )
    
    gs.plot_kernel_smooth(ax, nl, lon_bins, lat_bins)
    
    fig.suptitle(dn.strftime('%Y-%m-%d %H:%M'), y = 0.7)