import matplotlib.pyplot as plt
import GOES as gs
import datetime as dt 
import cartopy.crs as ccrs
from matplotlib.gridspec import GridSpec
import base as b 
 
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



def plot_vir_and_top_cloud(dn):
    
    fig = plt.figure(
        dpi = 300,
        figsize = (14,  14), 
        )
       
    gs2 = GridSpec(1, 2)
    
    gs2.update(wspace = 0.2)
    
    ax0 = plt.subplot(
        gs2[0], projection = ccrs.PlateCarree(
            ))
    
    ax1 = plt.subplot(
        gs2[1], projection = ccrs.PlateCarree())
    
    plot_vir_image(ax0, dn)
  
    gs.plot_view_nucleos(dn, ax=ax1, threshold=-40)
    
    fmt = '%Y-%m-%d %H:%M UT'
    
    fig.suptitle(
        dn.strftime(fmt), y = 0.73)
    
    axs = [ax0, ax1]
    b.plot_letters(
            axs, 
            x = 0.02, 
            y = 0.8, 
            offset = 0, 
            fontsize = 30,
            num2white = 0
            )
    return fig

def main():
     
    dn = dt.datetime(2013, 1, 1)
    
    fig = plot_vir_and_top_cloud(dn)
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Convective_analysis\\'
     
    figname = 'vir_and_top_cloud'
    fig.savefig(path_to_save + figname, dpi = 400)

    
# main()
