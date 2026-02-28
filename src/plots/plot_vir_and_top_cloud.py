import matplotlib.pyplot as plt
import GOES as gs
import datetime as dt 
import cartopy.crs as ccrs
from matplotlib.gridspec import GridSpec
import base as b 
import GEO as gg
import numpy as np 
  
b.sci_format(fontsize = 20)


def plot_vir_image(ax, dn):
    url_img = gs.image_url(dn)
    img =  gs.imshow_url(url_img)
    
    lat_max = 12  
    lon_max = -30
    lat_min = -55
    lon_min = -100
    extent = [lon_min, lon_max, lat_min, lat_max]
    ax.imshow(
        img, 
        origin = "upper",
        transform = ccrs.PlateCarree(),
        extent = extent
        )
    ax.axis("off")
    
    return img 

def plot_top_cloud_temp(
        ax, dn,
                        
            lat_min = -50, 
            lat_max = 10,
            lat_step = 10,
            lon_min = -100,
            lon_max = -30, 
            lon_step = 10):
    fn = gs.get_path_by_dn(dn)
    lon, lat, temp = gs.read_gzbin(
        fn, 
        lat_max = 13.0, 
        lon_min = -100.0, 
        dy = 0.04
        )
   
  
    lat_lims = dict(min=lat_min, max=lat_max, stp=lat_step)
    lon_lims = dict(min=lon_min, max=lon_max, stp=lon_step)

   
    img =  ax.pcolormesh(
        lon, lat, temp, 
        vmin = -100, 
        vmax = 100,
        cmap= gs.goes_cmap(), 
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
    
    
    return  lon, lat, temp


def plot_vir_and_top_cloud(dn):
    
    fig = plt.figure(
        dpi = 300,
        figsize = (14,  14), 
        )
       
    gs2 = GridSpec(1, 2)
    
    gs2.update(wspace = 0.2)
    
    ax0 = plt.subplot(gs2[0], projection = ccrs.PlateCarree())
    
    ax1 = plt.subplot(gs2[1], projection = ccrs.PlateCarree())
    
    plot_vir_image(ax0, dn)
    plot_top_cloud_temp(ax1, dn)

    fig.suptitle(dn.strftime('%Y-%m-%d %H:%M UT'), y = 0.73)
    
    return fig

dn = dt.datetime(2013, 2, 1)
 
fig = plot_vir_and_top_cloud(dn)