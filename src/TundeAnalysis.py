import pandas as pd 
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
import numpy as np 
import core as c
import GOES as gs
import cartopy.crs as ccrs

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
    lon_lims = dict(min = -80, max = -40, stp = 10) 
    
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
        # levels = np.arange(3, 20, 5),
        cmap = 'jet'
        )
    
    return img 
    

def set_data(ds, step = 3, values = 'mean_60_90'):
    
    df = size_by_grid(
            ds, 
            step = step, 
            rounding = 0
            )

    ds = pd.pivot_table(
        df, 
        columns = 'lon_bin', 
        index = 'lat_bin', 
        values = values
        )

    return ds 



def plot_seasonal_occurrence(
        ax, 
        ds,
        year = 2013,
        step = 2
        ):
    
   
    seasons = {

        'Jan - Feb': [1, 2], 
        'Mar - Apr': [3, 4], 
        'May - Jun': [5, 6], 
        'Jul - Aug': [7, 8], 
        'Sep - Oct': [9, 10], 
        'Nov - Dec': [11, 12]
    }
    
    axes = ax.flat

    for i, (key, value) in enumerate(seasons.items()):
       
        df = ds.loc[ds.index.month.isin(value)]
        
        plot_map(axes[i], set_data(df, step = step)) 
                    
        l = b.chars()[i]
        
        axes[i].set_title(
            f'({l}) {key} ({year})', 
            fontsize = 20
            )
            
        
        if i == 3:
            pass
        else:
            axes[i].set(
                xticklabels = [],
                xlabel = '',
                ylabel = '',
                yticklabels = []
                )
            
    return ax 

       
        
b.config_labels(fontsize = 25)
    
fig, axs = plt.subplots(
      dpi = 300, 
      ncols = 3, 
      nrows = 2, 
      figsize = (13, 14),
      subplot_kw = 
      {'projection': ccrs.PlateCarree()}
      )

plt.subplots_adjust(wspace = 0.1, hspace = 0.05)

ds = b.load('GOES/data/ep_all')

ds = gs.limits(
    ds,  
    x0 = -90, x1 = -30, 
    y0 = -40, y1 = 20
    )

plot_seasonal_occurrence(axs, ds, year = 2013, step = 4)

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

year = 2015
df = gs.potential_energy(year = year)

# df