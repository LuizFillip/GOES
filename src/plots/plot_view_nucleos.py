import GOES  as gs 
import cartopy.crs as ccrs
import datetime as dt 
import matplotlib.pyplot as plt 
import numpy as np 
 

def ensure_lat_ascending(lon, lat, temp):
    """Garante lat crescente e temp alinhado (temp: [lat, lon])."""
    lon = np.asarray(lon, float)
    lat = np.asarray(lat, float)
    temp = np.asarray(temp)

    if lat[0] > lat[-1]:
        lat = lat[::-1]
        temp = temp[::-1, :]
    return lon, lat, temp
 
from matplotlib.patches import Ellipse
 

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
    
    ax.set(title = gs.fn2dn(fn).strftime('%Y-%m-%d %H:%M'))
    plt.show()
    
    # nl = gs.find_nucleos(       
    #     lon,
    #     lat,
    #     temp,
    #     dn= gs.fn2dn(fn),
    #     temp_threshold=threshold,
    # )
    
    # nl
    
fn = "D:\\database\\goes\\2012\\01\\S10216956_201201010600.gz"
fn = "D:\\database\\goes\\2012\\S10236965_201202020000.gz"
# lon, lat, temp = gs.read_gzbin(fn)
# lon, lat, temp = gs.read_dataset(fn)
# import gzip
# with gzip.open(fn, 'rb') as f:
    
#     dados_binarios = np.frombuffer(
#         f.read(), 
#         dtype = np.int16
#         ).astype(np.float32)

# image_size = [1714, 1870] 
# data_bin = dados_binarios.reshape(image_size)  
 
# dx = 0.04,
# dy = 0.04,
 
# lon_min = -100.0
# lat_max =  12.0 
    
# ny, nx = tuple(image_size)

 
# lon = lon_min + np.arange(nx) * dx
# lat = lat_max - np.arange(ny) * dy   
 
# temp = data_bin / 100 - 273.13


# fig, ax = gs.plot_cloud_top_temperature(lon, lat, temp)
