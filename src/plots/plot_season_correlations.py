import pandas as pd 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 
import GEO as gg
import datetime as dt 
import GOES as gs 
import base as b 
import numpy as np 

b.sci_format(fontsize = 20)



def month_by_month_seasonality(df, year):

    fig, ax = plt.subplots(
        figsize = (14, 6), 
        dpi = 300, 
        ncols = 6, 
        nrows = 2, 
        subplot_kw = {"projection": ccrs.PlateCarree()}
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    lats = dict(min = -60, max = 10, stp = 10)
    lons = dict(min = -90, max = -30, stp = 20)
    
    for i, ax in enumerate(ax.flat):
        nl = df.loc[df.index.month == i + 1]
        
        blon, blat = gs.get_bins(nl, step = 2)
        
        gs.plot_occurrence_rate_grid(ax, nl, blon, blat)
        
        dn = nl.index[0]
        ax.set( title = dn.strftime('%B'))
        
        gg.map_attrs(
            ax, None, 
            lat_lims = lats, 
            lon_lims = lons, 
            grid = False, 
            degress = None
            )
        
        x0 = -70  
        x1 = -50  
        y0 = -10  
        y1 = 0
        gs.plot_rectangle(
                ax, x0, x1, y0, y1, 
                lw = 3, dot_size=50, 
                number = None, 
                color = 'w'
                )
        
        if i != 6:
            ax.set(
                xticklabels = [],
                yticklabels = [],
                xlabel = '', 
                ylabel = ''
                )
            
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 30, 
            cmap = "jet",
            fontsize = 25,
            step = 5,
            label = f'Convection activity - {year} (\%)', 
            anchor = [0.3, 1.1, 0.4, 0.02], 
            orientation = 'horizontal',
            levels = 50
            )
    
    # fig.suptitle(2013, y = 1.1)

def plot_in(ds, df):

    fig, ax = plt.subplots(
        figsize = (12, 10), 
        sharex = True,
        nrows = 2,
        dpi = 300)
    
    ax[0].scatter(ds.index, ds[vls], s = 10, alpha = 0.4, )
    
    ds = ds.rolling('20d').mean()
    ax[0].plot(ds[vls], lw = 2, color = 'red')
    
    
    ax[0].set(ylabel = 'Ep (J/kg)')
    
    ax[1].scatter(df.index, df, s = 10, alpha = 0.4, )
  
    
    df = df.rolling('20D').mean()
    
    ax[1].plot(df, lw = 2, color = 'red')
    
    ax[1].set(ylabel = 'Number of convections')
    
    b.format_month_axes( ax[-1], month_locator = 1)


def nucleos(df):
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    ds = gs.filter_space(
            df, 
            lon_min = -70, 
            lon_max = -50, 
            lat_min = -10, 
            lat_max = 0
            )
    
    
    df = ds.groupby(ds.index.date).size() 
    
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[~df.index.duplicated()]
    return df 

# year = 2013
# df = b.load(f'GOES/data/nucleos/{year}')

# df = nucleos(df)
 
def waves(vls):

    ds = gs.potential_energy(year = 2013)
  
    ds = gs.filter_space(
            ds, 
            lon_min = -70, 
            lon_max = -50, 
            lat_min = -10, 
            lat_max = 0
            )
    
    # ds = ds.loc[ds[vls] < 20] 
    
    return ds[vls].resample('1D').mean()

