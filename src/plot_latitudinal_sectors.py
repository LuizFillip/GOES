import GOES  as gs
from matplotlib import cm
import cartopy.crs as ccrs
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 
import GEO as gg 
import matplotlib.patches as mpatches
import datetime as dt 

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
            temp = -30
            )
    
    ax.set(title = ds.dn)
    
def limits(
        df, 
           x0 = -80, x1 = -40, 
           y0 = -10, y1 = 0):
    
    return  df.loc[
        ((df['Lon'] > x0) & (df['Lon'] < x1)) &
        ((df['Lat'] > y0) & (df['Lat'] < y1))
        ]

def plot_sectors( 
        ax, 
        lat_min = -50, 
        lat_max = 20,
        lon_min = -80, 
        lon_max = -30, 
        height = 20
        ):

    latitudes = range(lat_min, lat_max + 1, height)
    
    
    for i, lat in enumerate(latitudes):
        rect = mpatches.Rectangle(
            xy=(lon_min, lat),  
            width = lon_max - lon_min, 
            height = height,  
            edgecolor = 'blue',
            facecolor = 'none',
            linewidth = 4
        )
        ax.add_patch(rect)
        
        middle = (lat + 5) - 1
        
        ax.text(-35, middle, i + 1, 
                transform = ax.transData, 
                fontsize = 40, 
                color = 'blue'
                )
    return None 
     
def plot_top_cloud_map(
    
        ):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 12), 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    lat_lims = dict(min = -60, max = 30, stp = 10)
    lon_lims = dict(min = -90, max = -20, stp = 10) 
    
    gg.map_attrs(
       ax, 2013, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )
    
    plot_contours(ax, fig)
    
 
    
    return fig 



dn = dt.datetime(2019, 4, 1, 0, 0)



def plot_nucleos_from_data(ax, dn):
    
    infile = f'GOES/data/nucleos/{dn.year}'
    
    df = b.load(infile)
    
    df['Lon'] = (df['x1'] + df['x0']) / 2
    df['Lat'] = (df['y1'] + df['y0']) / 2
    
    ds = df.loc[df.index == dn]
    
    ax.set(title = ds.index[0])
    
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
    
fig = plot_top_cloud_map()
