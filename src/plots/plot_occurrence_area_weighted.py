import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GOES as gs
import matplotlib.colors as colors 
import datetime as dt 
from scipy.ndimage import gaussian_filter
 
def occurrence_area_weighted(df, lon_bins, lat_bins):
 
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["area_km2"] = gs.bbox_area_km2(
        df["lon_min"], df["lon_max"],
        df["lat_min"], df["lat_max"]
    )

    df["lon_bin"] = pd.cut(df["lon"], lon_bins, labels=lon_bins[:-1])
    df["lat_bin"] = pd.cut(df["lat"], lat_bins, labels=lat_bins[:-1])

    weighted = (
        df.groupby(["lon_bin", "lat_bin"])["area_km2"]
          .sum()
          .reset_index()
    )

    grid = pd.pivot_table(
        weighted,
        index="lat_bin",
        columns="lon_bin",
        values="area_km2"
    )

    return grid.fillna(0)

 

def plot_raw_occurrence_area_weighted(nl, step = 2, cmap = 'plasma'):
   
    lon_bins, lat_bins = gs.get_bins(
        
        nl, step = step, 
        )
    
    grid = occurrence_area_weighted(nl, lon_bins, lat_bins)
    smooth = gaussian_filter(grid.values, sigma=1.5)
  
    vmax = np.nanpercentile(grid.values, 99)   
    norm = colors.Normalize(vmin=0, vmax=vmax)
    
 
    fig, ax = gs.map_defout(
        ncols = 2, 
        lat_min = -45,
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
    
 



dn = dt.datetime(2013, 1, 1)

step = 2

fn = gs.get_path_by_dn(dn)

lon, lat, temp = gs.read_gzbin(fn)

nl = gs.find_nucleos(       
    lon,
    lat,
    temp,
    dn=None,
    temp_threshold= -40,
)

# lon_bins, lat_bins = gs.get_bins(nl, step = 2)

# grid = occurrence_area_weighted(nl, lon_bins, lat_bins)
 

# vmax = np.nanpercentile(grid.values, 99)   
# norm = colors.Normalize(vmin = 0, vmax = vmax)


# sigma = 1.5


# smooth = gaussian_filter(grid.values, sigma=sigma)
# fig, ax = gs.map_defout(
#     ncols = 1,  
#     lat_min=-50,
#     lat_max=10,
#     lat_step=10,
#     lon_min=-100,
#     lon_max=-30
#      )

# cmap = 'plasma'
# img1 = ax.pcolormesh(
#     grid.columns,
#     grid.index,
#     smooth,
#     cmap= cmap,   # melhor que jet
#     norm=norm,
#     # shading="auto"
# )

# cax  = ax.inset_axes([1.03, 0, 0.04, 1])
 
# cbar = fig.colorbar(
#     img1,
#     ax=ax,
#     orientation="vertical",
 
#     cax  = cax
# )

fig = plot_raw_occurrence_area_weighted(nl,  cmap = 'plasma')