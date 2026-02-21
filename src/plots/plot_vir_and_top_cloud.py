import matplotlib.pyplot as plt
import GOES as gs
import datetime as dt 
import cartopy.crs as ccrs
from matplotlib.gridspec import GridSpec
import base as b 

b.sci_format(fontsize = 20)


def plot_vir_image(ax0, dn):
    url_img = gs.image_url(dn)
    img =  gs.imshow_url(url_img)
    
    lat_max = 12  
    lon_max = -30
    lat_min = -55
    lon_min = -100
    extent = [lon_min, lon_max, lat_min, lat_max]
    ax0.imshow(
        img, 
        origin="upper",
     transform=ccrs.PlateCarree(),
               extent = extent)
    ax0.axis("off")

def plot_top_cloud_temp(ax1, dn):
    fn = gs.get_path_by_dn(dn)
    lon, lat, temp = gs.read_gzbin(
        fn, 
        lat_max = 13.0, 
        lon_min = -100.0, 
        dy = 0.04
        )
    
    gs.plot_cloud_top_temperature(
        lon, lat, temp, ax1, 
        lat_max = 12, 
        lon_max = -30, 
        lat_min = -55, 
        lon_min = -100
        )


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

dn = dt.datetime(2015, 1, 3)
 
fig = plot_vir_and_top_cloud(dn)