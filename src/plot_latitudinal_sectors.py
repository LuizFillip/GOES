import GOES  as gs
from matplotlib import cm
import cartopy.crs as ccrs
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 
import GEO as gg 
import matplotlib.patches as mpatches

def plot_contours(ax, fig):
    fname = 'E:\\database\\goes\\2019\\04\\S10635346_201904010030.nc'

    ds = gs.CloudyTemperature(fname)
    dat, lon, lat = ds.data, ds.lon, ds.lat
    
    ptc = gs.plotTopCloud(dat, lon, lat, fig)
    
    img = ptc.contour(ax)
    
    ptc.colorbar(img, ax)
    
    gs.tracker_nucleos(
            ax, 
            ds, 
            color = 'k',
            temp = -60
            )
    
def limits(
        df, 
           x0 = -80, x1 = -40, 
           y0 = -10, y1 = 0):
    
    return  df.loc[
        ((df['Lon'] > x0) & (df['Lon'] < x1)) &
        ((df['Lat'] > y0) & (df['Lat'] < y1))
        ]


def plot_top_cloud_map(ds):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 12), 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    lat_lims = dict(min = -60, max = 30, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
    gg.map_attrs(
       ax, 2013, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )
    
    
        
    ax.set(title = ds.index[0])
    # plot_contours(ax, fig)
    
    lon_min, lon_max = -80, -40
    
    ds = limits(ds, 
              x0 = lon_min, 
              x1 = lon_max, 
              y0 = -20, y1 = -10)
    
    # count = 0
    for index, row in ds.iterrows():
        
        gs.plot_regions(
            ax,
            row['x0'], 
            row['y0'],
            row['x1'], 
            row['y1'], 
            color = 'k'
            )
        
        mx = (row['x1'] + row['x0']) / 2
        my = (row['y1'] + row['y0']) / 2
        ax.scatter(mx, my, s = 100, color = 'red')
    
    
    
    latitudes = range(-50, 21, 10)
    
   
    for lat in latitudes:
        rect = mpatches.Rectangle(
            xy=(lon_min, lat),  
            width=lon_max - lon_min, 
            height=10,  
            edgecolor='blue',
            facecolor='none',
            linewidth = 4
        )
        ax.add_patch(rect)

import datetime as dt 

dn = dt.datetime(2019, 4, 1, 0, 0)

infile ='GOES/data/nucleos/2019'
df = b.load(infile)
df['Lon'] = (df['x1'] + df['x0']) / 2
df['Lat'] = (df['y1'] + df['y0']) / 2
ds = df.loc[df.index == dn]

    
    
plot_top_cloud_map(ds)
