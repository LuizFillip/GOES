import GOES  as gs
from matplotlib import cm
import cartopy.crs as ccrs
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 
import GEO as gg 


def test_plot(fname, temp = -30):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 10), 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    ds = gs.CloudyTemperature(fname)
    
    dat, lon, lat = ds.data, ds.lon, ds.lat
  
    ptc = gs.plotTopCloud(dat, lon, lat, fig)
    img = ptc.contour(ax)
    ptc.add_map(ax)
    ptc.colorbar(img, ax)
        
    ax.set(title = ds.dn)
    
    nl =  gs.find_nucleos(
              dat, 
              lon, 
              lat[::-1],
              ds.dn,
              temp_threshold = temp,
             
              )
    count = 0
    for index, row in nl.iterrows():
        count += 1
        ptc.plot_regions(
            ax,
            row['x0'], 
            row['y0'],
            row['x1'], 
            row['y1'], 
            # number = count
            # i = indexs
            )
        
    return fig 

import datetime as dt 

dn = dt.datetime(2018,1,7,19,45)
folder = dn.strftime('%Y\\%m\\S10635346_%Y%m%d%H%M.nc')
fname = f'E:\\database\\goes\\{folder}'

# fig = test_plot(fname, temp = -30)

fname 