import pandas as pd 
import matplotlib.pyplot as plt
import base as b 
import datetime as dt 
import GOES as gs 
 

def plot_steps_grid_occurrence_one_file(dn):
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
    
def colorbar(ax, img):
    cax = ax.inset_axes([1.1, 0, 0.05, 1])
     
    cb = plt.colorbar(
        img,  
        cax = cax, 
        )
    
    cb.set_label("Convection activity (\%)")
    
    return None


df = b.load('GOES/data/nucleos3/201302')

dn = dt.date(2013, 2, 1)
nl = df.loc[df.index.date == dn]

def plot_steps_grid_occurrence_one_day(dn):
    lon_bins, lat_bins = gs.get_bins(nl, step = 2)

    fig, ax  =  gs.map_defout(
        figsize = (12, 8), ncols = 2,
        lon_max = -40, wspace = 0.3)
        
    img = gs.plot_occurrence_rate_grid(
        ax[0], nl, lon_bins, lat_bins)

    colorbar(ax[0], img)

    img = gs.plot_kernel_smooth(
        ax[1], nl, lon_bins, lat_bins, sigma = 1)

    colorbar(ax[1], img)

    fig.suptitle(dn.strftime('%Y-%m-%d'), y = 1)
     
    return 

