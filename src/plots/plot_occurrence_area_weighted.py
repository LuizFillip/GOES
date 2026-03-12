import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GOES as gs
import matplotlib.colors as colors 
import datetime as dt 
from scipy.ndimage import gaussian_filter
 



def plot_raw_occurrence_area_weighted(
        nl, step = 2, cmap = 'jet'):
    
    dn = nl.index[0]
    
    lon_bins, lat_bins = gs.get_bins(
        
        nl, step = step, 
        )
    
    grid = gs.occurrence_area_weighted(nl, lon_bins, lat_bins)
    smooth = gaussian_filter(grid.values, sigma=1.5)
  
    vmax = np.nanpercentile(grid.values, 99)   
    norm = colors.Normalize(vmin=0, vmax=vmax)
    
 
    fig, ax = gs.map_defout(
        ncols = 2, 
        lat_min = -50,
        lat_max = 10,
        lat_step = 10,
        lon_min = -100,
        lon_max = -30, 
        lon_step = 10,
        )

    # Painel 1
    img1 = ax[0].pcolormesh(
        grid.columns,
        grid.index,
        grid.values,
        cmap = cmap,   # melhor que jet
        norm = norm,
        shading = "auto"
    )
    
    ax[0].set_title("Raw occurrence")
    
    # Painel 2
    img2 = ax[1].pcolormesh(
        grid.columns,
        grid.index,
        smooth,
        cmap= cmap,
        norm=norm,
        shading="auto"
    )
    
    ax[1].set_title("Smoothed occurrence")
    
    cax = ax[1].inset_axes([1.03, 0, 0.04, 1])
     
    cbar = fig.colorbar(
        img1,
        ax=ax,
        orientation="vertical",
        cax  = cax
    )
    
    cbar.set_label("Area-weighted occurrence (km²)")
    
    fig.suptitle(dn.strftime('%Y-%m-%d %H:%M'), y = 0.8)
    
    # plt.tight_layout()
    plt.show()
    
    return fig 
    
 
import base as b 


df = b.load("GOES/data/nucleos_40/2013")   


df 