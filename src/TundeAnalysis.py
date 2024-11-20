import pandas as pd 
import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
from scipy.ndimage import gaussian_filter
import numpy as np 
import core as c



    


def load_nucleos(year = 2019, sample = '15D'):
    infile = f'GOES/data/nucleos/{year}'
    
    df = b.load(infile)
    
    df['lon'] = (df['x1'] + df['x0']) / 2
    df['lat'] = (df['y1'] + df['y0']) / 2
    
    #
    cond = [  
        (df['lat'] > -20) & 
        (df['lat'] < 10) ]
    df = df.resample(sample).size()
    
    
    df = (df / df.values.max()) *100
    return df 

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




def size_by_grid(
        df, 
        step = 1, 
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
    
    df['lon_bin'] = pd.cut(
        df['lon'], 
        bins = lon_bins, 
        labels = lon_bins[:-1]
        )
    df['lat_bin'] = pd.cut(
        df['lat'], 
        bins = lat_bins, 
        labels = lat_bins[:-1]
        )
    
    df['lon_bin'] = df['lon_bin'].astype(
        float).round(rounding)
    df['lat_bin'] = df['lat_bin'].astype(
        float).round(rounding)

      
    event_count = df.groupby(
        ['lon_bin', 'lat_bin']
        ).mean().reset_index()
    
    return event_count




def plot_map(ax, ds, year = 2013):

    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
    gg.map_attrs(
       ax, 
       year, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )
    
    # gg.plot_rectangles_regions(ax, year, color = 'k')

    img = ax.contourf(
        ds.columns, 
        ds.index, 
        ds.values, 
        levels = np.arange(3, 20, 1),
        cmap = 'jet'
        )
    
    return img 
    

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
    # print(np.nanmax(ds.values))
    return ds 

def plot_seasonal_Ep():

    fig, ax = plt.subplots( 
        sharex = True,
        sharey = True,
        figsize = (14, 8), 
        dpi = 300
        )
        
    years = [2013, 2019]
    maks = ['s', 'o']
    labl = ['Maximum', 'Minimum']
    
    for i, year in enumerate(years):
        
        df = c.potential_energy(year)
        
        ds = df['mean_90_110'].resample('1M').mean()
        
        ds.index = ds.index.month
        
        ax.plot(ds, lw = 2, 
                label = f'Solar {labl[i]} - {year}',
                markersize = 20, 
                marker = maks[i], 
             
                )
    
    ax.legend(loc = 'upper right')
    ax.set(
           ylabel = 'Ep (J/Kg)', 
           xticks = np.arange(1, 13, 1),
           xlabel = 'Months')
    
    plt.show()
    return fig

def plot_seasonal_occurrence(
        ax, 
        row = 1, 
        year = 2013,
        step = 2
        ):
    
    ds = c.potential_energy(year)
    
    ds = ds.rename(columns = {'Lat': 'lat', 
                              'Lon': 'lon'})

    
    seasons = {
        'Nov - Jan': [11, 12, 1], 
        'Feb - Apr': [2, 3, 4], 
        'Jun - Sep': [5, 6, 7],
        'Agu - Oct': [8, 9, 10]
        }


    for i, (key, value) in enumerate(seasons.items()):
       
        df = ds.loc[ds.index.month.isin(value)]
        
              
        plot_map(ax[row, i], set_data(df, step = step)) 
        
        # if row == 0:
            
        l = b.chars()[i]
        
        ax[row, i].set_title(
            f'({l}) {key} ({year})', 
            fontsize = 20
            )
            
        
        if i == 0 and row == 1:
            pass
        else:
            ax[row, i].set(
                xticklabels = [],
                xlabel = '',
                ylabel = '',
                yticklabels = []
                )
            
    return ax 
        ''
        
        
        
        
b.config_labels(fontsize = 25)
    

fig, axs = plt.subplots(
      dpi = 300, 
      ncols = 4, 
      nrows = 2, 
      figsize = (15, 8),
      subplot_kw = 
      {'projection': ccrs.PlateCarree()}
      )

plt.subplots_adjust(wspace = 0.1, hspace = 0.1)
    
plot_seasonal_occurrence(axs, row = 0, year = 2013, step = 3)
plot_seasonal_occurrence(axs, row = 1, year = 2019, step = 3)

b.fig_colorbar(
        fig,
        label = 'Ep (J/Kg)',
        fontsize = 35,
        vmin = 3, 
        vmax = 18, 
        step = 2,
        orientation = "vertical", 
        anchor = (.94, 0.13, 0.03, 0.73)
        )

# fig.suptitle(year, y = 1.1)
 
