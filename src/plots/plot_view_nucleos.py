import GOES  as gs 
import cartopy.crs as ccrs
import datetime as dt 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.patches import Ellipse
 

def ensure_lat_ascending(lon, lat, temp):
    """Garante lat crescente e temp alinhado (temp: [lat, lon])."""
    lon = np.asarray(lon, float)
    lat = np.asarray(lat, float)
    temp = np.asarray(temp)

    if lat[0] > lat[-1]:
        lat = lat[::-1]
        temp = temp[::-1, :]
    return lon, lat, temp
 


def add_ellipse_from_bbox(
    ax,
    lon_min, lon_max,
    lat_min, lat_max,
    *,
    shrink=1.0,
    edgecolor="k",
    linewidth=2.5,
    facecolor="none",
    zorder=6,
):
    # garante ordem
    x0, x1 = sorted([lon_min, lon_max])
    y0, y1 = sorted([lat_min, lat_max])

    xc = 0.5 * (x0 + x1)
    yc = 0.5 * (y0 + y1)

    width = (x1 - x0) * shrink
    height = (y1 - y0) * shrink

    e = Ellipse(
        (xc, yc),
        width=width,
        height=height,
        angle=0.0,  # pode rotacionar depois se quiser
        edgecolor=edgecolor,
        facecolor=facecolor,
        linewidth=linewidth,
        transform=ccrs.PlateCarree(),
        zorder=zorder,
    )
    ax.add_patch(e)

    # marcador no centro (opcional)
    ax.scatter(
        xc, yc, s=20, 
        color="red", 
        transform=ccrs.PlateCarree(), 
        zorder=zorder + 1
        )

    return e


def plot_view_nucleos(
        lon, lat, temp, 
        threshold=-40,
        draw_regions=True, 
        dot_size = None
        ):
    lon, lat, temp = ensure_lat_ascending(lon, lat, temp)
 

    nl = gs.find_nucleos(       
        lon,
        lat,
        temp,
        dn=None,
        temp_threshold=threshold,
    )
    
   
    fig, ax  =  gs.plot_cloud_top_temperature(lon, lat, temp)
    if dot_size is not None:
        for _, row in nl.iterrows():
            x0, x1 = row["lon_min"], row["lon_max"]
            y0, y1 = row["lat_min"], row["lat_max"]
            add_ellipse_from_bbox(
                ax,
                x0, x1,
                y0, y1
                )
            # gs.plot_rectangle(
            #         ax, x0, 
            #         x1, y0, y1, 
            #         lw=3, 
            #         dot_size=None, 
            #         number = None
            #         )
  
    return fig, ax, nl


# --------- example usage ---------
def example_usage():
    dn = dt.datetime(2015, 1, 1)
    files = gs.walk_goes(dn, B="D")
    fn = files[3]
    print(fn)
    fn = 'GOES/data/S10635346_201801010100.nc'
    # lon, lat, temp = gs.read_gzbin(fn)
    lon, lat, temp = gs.read_dataset(fn)
    
    threshold = -40
    
    fig, ax, nl = plot_view_nucleos(
        lon, lat, temp, 
        threshold=threshold, 
        draw_regions=False, 
        dot_size = None
        )
    
    
    plt.show()
    
    # nl = gs.find_nucleos(       
    #     lon,
    #     lat,
    #     temp,
    #     dn= gs.fn2dn(fn),
    #     temp_threshold=threshold,
    # )
    
    # nl
    
