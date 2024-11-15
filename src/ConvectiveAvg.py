import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
import numpy as np 
import pandas as pd 

b.config_labels(fontsize = 35 )


def size_by_grid(
        df, 
        step = 2.5, 
        rounding = 0
        ):
  
    lon_bins = np.arange(
        df['lon'].min(), 
        df['lon'].max() + step, step
        )
    lat_bins = np.arange(
        df['lat'].min(), 
        df['lat'].max() + step, step
        )
    
    df['lon_bin'] = pd.cut( df['lon'], 
        bins=lon_bins, 
        labels=lon_bins[:-1]
        )
    df['lat_bin'] = pd.cut(df['lat'], 
        bins=lat_bins, 
        labels=lat_bins[:-1]
        )
    
    df['lon_bin'] = df['lon_bin'].astype(
        float).round(rounding)
    df['lat_bin'] = df['lat_bin'].astype(
        float).round(rounding)

      
    event_count = df.groupby(
        ['lon_bin', 'lat_bin']).size(
            ).reset_index(name='event_count')
    
    return event_count

def plot_map_contour(ax, df, year = 2019):

    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
    gg.map_attrs(
       ax, year, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )
    
    gg.plot_rectangles_regions(ax, year, color = 'white')
    
    ax.contourf(
        df.columns, 
        df.index, 
        df.values, 
        levels = np.arange(0, 100, 1), 
        cmap = 'jet'
        )
    
    return ax



def set_data(df, step = 2):
    
    df['lon'] = (df['x1'] + df['x0']) / 2
    df['lat'] = (df['y1'] + df['y0']) / 2
    
    ds = size_by_grid(df, step = step).dropna()
    
    ds = pd.pivot_table(
        ds, 
        columns = 'lon_bin', 
        index = 'lat_bin', 
        values = 'event_count'
        )
    
    ds = ds.replace(np.nan, 0)
    
    ds = (ds / np.nanmax(ds.values)) * 100 
    
    return ds 





def plot_seasonal_convective_rate(df):
    
    year = df.index[0].year

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
    
    
    for i, ax in enumerate(ax.flat):
        
        season = months[i]
        ds = set_data(df.loc[df.index.month.isin(season)])
            
        plot_map_contour(ax, ds) 
        
        if i != 2:
            
            ax.set(
                xticklabels = [],
                xlabel = '',
                ylabel = '',
                yticklabels = []
                )
    
        
        ax.set_title(names[i].upper(), fontsize = 30)
        
        
    b.fig_colorbar(
            fig,
            label = 'Occurrence rate of convective nucleos (\%)',
            fontsize = 35,
            vmin = 0, 
            vmax = 100, 
            step = 10,
            orientation = 'horizontal',
            sets = [0.14, 1., 0.75, 0.02] 
            )
    
    fig.suptitle(year, y = 1.1)
    
    return fig


# for year in range(2014, 2018):
#     infile = f'GOES/data/nucleos/{year}'
#     fig = plot_seasonal_convective_rate( b.load(infile))