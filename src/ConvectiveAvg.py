import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
import GOES as gs
import numpy as np 
import math 
import pandas as pd 


def size_by_grid(
        df, lon_step=2.5, lat_step=2.5, 
        rounding = 0):
 
    lon_bins = np.arange(
        df['lon'].min(), 
        df['lon'].max() + lon_step, lon_step
        )
    lat_bins = np.arange(
        df['lat'].min(), 
        df['lat'].max() + lat_step, lat_step
        )
    
    df['lon_bin'] = pd.cut(
        df['lon'], 
        bins=lon_bins, 
        labels=lon_bins[:-1]
        )
    df['lat_bin'] = pd.cut(
        df['lat'], 
        bins=lat_bins, 
        labels=lat_bins[:-1]
        )
    
    df['lon_bin'] = df['lon_bin'].astype(float).round(rounding)
    df['lat_bin'] = df['lat_bin'].astype(float).round(rounding)

      
    event_count = df.groupby(['lon_bin', 'lat_bin']).size().reset_index(name='event_count')
    
    return event_count

def plot(ax, df):

    
    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
    gg.map_attrs(
       ax, 2013, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )
    gg.plot_rectangles_regions(ax, 2013)
    img = ax.contourf(
        df.columns, 
        df.index, 
        df.values, 
        10, 
        cmap = 'jet')
    
    # ticks= np.arange(0, 110, 20)
    
    # b.colorbar(img,  ax,     ticks, 
    #       label = 'TECU ($10^{16}/m^2$)', 
    #       height = "100%", 
    #       width = "10%",
    #       orientation = "vertical", 
    #       anchor = (.25, 0., 1, 1)
    #       )

    # ax.scatter(
    #     df['lon_bin'], 
    #     df['lat_bin'], 
    #     c = df['event_count'], 
    #     cmap = 'jet'
    #     )
    
    return fig

def to_pivot(ds):
    ds = pd.pivot_table(
        ds, columns = 'lon_bin', index = 'lat_bin', 
                    values = 'event_count')
    
    # ds = ds.replace(np.nan, 0)
    
    ds = (ds / np.nanmax(ds.values)) * 100 
    
    return ds
    

fname = 'E:/database/goes/2019/04/S10635346_201904010000.nc'


# figs = gs.test_plot(fname, temp = -60)

dn = gs.fname2date(fname)
infile = 'GOES/data/2019/'
infile = 'GOES/data/2018'

def set_data(df):
    df['lon'] = (df['x1'] + df['x0']) / 2
    df['lat'] = (df['y1'] + df['y0']) / 2
    
    
    df = df.loc[df['area'] > 10, ['area', 'lon', 'lat']]
    
    
    ds = size_by_grid(
        df, lon_step = 1, lat_step = 1).dropna()
    
    return to_pivot(ds)
# fig = plot(ds) 

# ds



df = b.load(infile)

months = [
    [12, 1, 2],
    [3, 4, 5], 
    [6, 7, 8],
    [9, 10, 11]
    ]

names = [
    'dez - fev', 
    'mar - mai', 
    'jun - agu',
    'set - nov'
    ]
fig, ax = plt.subplots(
      dpi = 300, 
      ncols = 2, 
      nrows = 2, 
      figsize = (16, 16),
      subplot_kw = 
      {'projection': ccrs.PlateCarree()}
      )
    


for i, ax in enumerate(ax.flat):
    
    season = months[i]
    ds = set_data(
        df.loc[df.index.month.isin(season)])
        
    plot(ax, ds) 
    
    if i != 2:
        
        ax.set(
            xticklabels = [],
            xlabel = '',
            ylabel = '',
            yticklabels = [])

    
    ax.set(title = names[i].upper())
    
    
b.fig_colorbar(
        fig,
        label = 'Convective Nucleos (\%)',
        fontsize = 35,
        vmin = 0, 
        vmax = 100, 
        step = 20,
        orientation = 'horizontal',
        sets = [0, 1., 0.95, 0.02] 
        )