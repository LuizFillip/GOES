import GOES  as gs
from matplotlib import cm
import cartopy.crs as ccrs
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 
import GEO as gg  
from matplotlib.patches import Ellipse
 


def goes_cmap(path = 'GOES/src/plots/colorbar.cpt'):
    cpt = gs.loadCPT(path)
    return cm.colors.LinearSegmentedColormap('cpt', cpt) 

 
def plot_cloud_top_temperature(
        lon, lat, temp, 
        # ax = None,
        lat_min = -50, 
        lat_max = 10,
        lat_step = 10,
        lon_min = -100,
        lon_max = -30, 
        lon_step = 10, 
        dn = None
        ):
    
    fig, ax = plt.subplots(
        dpi=300,
        figsize=(10, 10),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )
        
    lat_lims = dict(min=lat_min, max=lat_max, stp=lat_step)
    lon_lims = dict(min=lon_min, max=lon_max, stp=lon_step)

   
    img =  ax.pcolormesh(
        lon, lat, temp, 
        vmin = -100, 
        vmax = 100,
        cmap= goes_cmap(), 
        transform=ccrs.PlateCarree()
        )
    
 
    
    gg.map_attrs(
        ax,
        year=None,
        lat_lims=lat_lims,
        lon_lims=lon_lims,
        grid=False,
        degress=None,
    )
     
   
    step = 20
    ticks = np.arange(-100, 100 + step, step)
    height = "100%"
    width = "5%"
    anchor = (.1, 0., 1, 1)
    
    b.colorbar(
           img, 
           ax, 
           ticks, 
           label = 'Temperature (°C)', 
           height = height, 
           width = width,
           orientation = 'vertical', 
           anchor = anchor
           )
    
    if dn is not None:
        ax.set(title = dn.strftime('%Y-%m-%d %H:%M'))
    
    return fig, ax
    
 


def plot_rectangle(
        ax, x0, 
        x1, y0, y1, 
        lw=3, dot_size=50, 
        number = None
        ):
    x0, x1 = sorted([x0, x1])
    y0, y1 = sorted([y0, y1])

    rect = plt.Rectangle(
        (x0, y0),
        x1 - x0,
        y1 - y0,
        edgecolor="k",
        facecolor="none",
        linewidth=lw,
        transform=ccrs.PlateCarree(),
        zorder=5,
    )
    ax.add_patch(rect)

    my = (x0 + x1) / 2
    mx = (y0 + y1) / 2,
    
    if dot_size is not None:
        ax.scatter(
            mx, my,
            s=dot_size,
            color="red",
            transform=ccrs.PlateCarree(),
            zorder=6,
        )
        
    if number is not None:
    
        ax.text(
            mx, my + 1, number, 
            transform=ccrs.PlateCarree()
            )
    
    return None 

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