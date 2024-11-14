import pandas as pd 
import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
from scipy.ndimage import gaussian_filter
import numpy as np 

def load_tunde(infile):
    df = pd.read_csv(infile, delim_whitespace=True)
    
    df.index = pd.to_datetime(
        df['Date'] + ' ' + 
        df[['Hour', 'Minute', 'Second']
           ].astype(str).agg(':'.join, axis=1))
    
    df = df.drop(
        columns = [
        'Year', 'DOY', 'Date', 
        'Hour', 'Minute', 'Second']
        )
    
    return df



    


def load_nucleos():
    infile = 'GOES/data/2013'
    
    df = b.load(infile)
    
    df['lon'] = (df['x1'] + df['x0']) / 2
    df['lat'] = (df['y1'] + df['y0']) / 2
    
    #
    cond = [   (df['lat'] > -20) & 
        (df['lat'] < 10) ]
    df = df.resample(sample).size()
    
    
    df = (df / df.values.max()) *100


def plot_seasonal(df, ds):

    fig, ax = plt.subplots(
          dpi = 300, 
          figsize = (16, 8)
          )
        
    sdf = gaussian_filter(df, sigma=1)

    ax.plot(
        df.index,
        sdf, 
            lw = 3, color = 'blue')
    ax.set(ylabel = 'Convective activity (\%)')
    
    b.change_axes_color(
            ax, 
            color = 'blue',
            axis = "y", 
            position = "left"
            )
    
    ax1 = ax.twinx()
    # ax1.scatter(ds.index, ds.values, c = 'red')
    
    # ds = ds.rolling(10).mean()
    sds = gaussian_filter(ds, sigma=1)
    ax1.plot(ds.index, sds,  lw = 3, color = 'red')
    
    ax1.set(ylabel = 'GW potential energy (J/Kg)')
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    
    b.format_month_axes(ax)


# plot_seasonal(df, ds)


def size_by_grid(
        df, step = 1, 
        rounding = 0):
 
    lon_bins = np.arange(
        df['lon'].min(), 
        df['lon'].max() + step, step
        )
    lat_bins = np.arange(
        df['lat'].min(), 
        df['lat'].max() + step, step
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
    
    df['lon_bin'] = df['lon_bin'].astype(
        float).round(rounding)
    df['lat_bin'] = df['lat_bin'].astype(
        float).round(rounding)

      
    event_count = df.groupby(
        ['lon_bin', 'lat_bin']
        ).mean().reset_index()
    
    return event_count




def plot_map(ax, ds):
    # fig, ax = plt.subplots(
    #       dpi = 300, 
    #       figsize = (10,10),
    #       subplot_kw = 
    #       {'projection': ccrs.PlateCarree()}
    #       )
        
    
    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
    gg.map_attrs(
       ax, 2013, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )


    img = ax.contourf(
        ds.columns, 
        ds.index, 
        ds.values, 
        levels = np.arange(3, 18, 1),
        cmap = 'jet'
        )
    
    # ticks= np.arange(3, 18, 2)
    
    # b.colorbar(
    #     img,  
    #     ax,   
    #     ticks, 
    #     label = 'Ep (J/Kg)', 
    #     height = "100%", 
    #     width = "10%",
    #     orientation = "vertical", 
    #     anchor = (.25, 0., 1, 1)
    #     )
    
    

def set_data(ds, step = 1):
    
    df = size_by_grid(
            ds, step = step, 
            rounding = 0
            )

    ds = pd.pivot_table(
        df, 
        columns = 'lon_bin', 
        index = 'lat_bin', 
        values = 'mean_90_110'
        )
    
    # ds = ds.replace(np.nan, 0)
    
    return ds 

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

plt.subplots_adjust(wspace = 0., hspace = 0.15)

year = 2013
infile = 'GOES/data/Select_ep_data_lat_lon_2013.txt'

ds = load_tunde(infile)


ds = ds.rename(columns = {'Lat': 'lat', 'Lon': 'lon'})

b.config_labels()

step = 2


for i, ax in enumerate(ax.flat):
    
    season = months[i]
    
    df = ds.loc[ds.index.month.isin(season)]
          
    plot_map(ax, set_data(df, step = step)) 
    
    if i != 2:
        
        ax.set(
            xticklabels = [],
            xlabel = '',
            ylabel = '',
            yticklabels = []
            )

    
    ax.set(title = names[i].upper())
    
    
b.fig_colorbar(
        fig,
        label = 'Ep (J/Kg)',
        fontsize = 35,
        vmin = 3, 
        vmax = 18, 
        step = 2,
        orientation = 'horizontal',
        sets = [0.13, 1., 0.75, 0.02] 
        )

fig.suptitle(year)