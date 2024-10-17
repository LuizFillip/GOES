import xarray as xr 
import base as b 
import GEO as gg 
import pandas as pd 
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np 
from tqdm import tqdm 

lat_lims = dict(min = -40, max = 20, stp = 10)
lon_lims = dict(min = -90, max = -30, stp = 10) 

# lat_lims = dict(min = -90, max = 90, stp = 15)
# lon_lims = dict(min = -180, max = 180, stp = 30) 



def OLR_Map(df, dn, ax = None):
    
    if ax is None:
        fig, ax = plt.subplots(
             figsize = (16, 12), 
             dpi = 300, 
             subplot_kw = 
             {'projection': ccrs.PlateCarree()}
             )
    
    gg.map_attrs(
        ax, dn.year, 
        lat_lims  = lat_lims, 
        lon_lims = lon_lims,
        grid = False,
        degress = None
        )
    
    lon = df['lon'].values
    lat = df['lat'].values
    values = df['olr'].values
    
    levels = np.arange(70, 400, 5)
    
    img = ax.contourf(
        lon,
        lat, 
        values, 
        levels = levels, 
        cmap = 'jet'
        )
    
    ticks = np.arange(70, 400, 100)
    
    b.colorbar(
            img, 
            ax, 
            ticks, 
            label = 'OLR (Watts/$m^2$)', 
            height = "100%", 
            width = "3%",
            orientation = "vertical", 
            anchor = (.1, 0., 1, 1)
            )
    
    ax.set(title = dn.strftime('%Y-%m-%d'))
    gg.plot_rectangles_regions(ax, dn.year)
    
    if ax is None:
        return fig
    else:
        return ax

b.config_labels()




def dataset_to_dataframe(df):
    
    df = df.to_dataframe()
    
    df['lon'] = df.index.get_level_values(1)
    df['lat'] = df.index.get_level_values(0)
    
    df.index = df['time']
    
    del df['time']
    
    return df



def sel_sector(df, sector , year,  step = 0.5):

    corners = gg.set_coords(year)
    
    xlim, ylim = corners[sector]
    
    return df.sel(
        lon = slice(xlim[0] - step, xlim[1] + step), 
        lat = slice(ylim[0] - step, ylim[1] + step)
        )


def sel_sector2(df, sector , year,  step = 0.5):

    corners = gg.set_coords(year)
    
    xlim, ylim = corners[sector]
    
    return df.sel(
        lon = slice(xlim[0] - step, xlim[1] + step), 
        lat = slice(ylim[1] - step, ylim[0] + step)
        )


def interpol_data(ds):


    
    new_lon = np.linspace(ds.lon[0], ds.lon[-1], 360)
    
    new_lat = np.linspace(ds.lat[0], ds.lat[-1], 180)
    
    ds = ds.interp(lat = new_lat, lon = new_lon)

def get_avg(ds):
    out = {}
    dn = pd.to_datetime(ds['time'].values)
    
    for sector in np.arange(-80, -40, 10):
        df = sel_sector2(ds, sector, dn.year)
        
        out[sector] = df['olr'].mean().values
        
    return pd.DataFrame(out, index = [dn])
    
# 

def runnig_by_days(ds, year):
    
    out = []
    print('starting', year)
    for day in tqdm(range(365)):
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1) + delta
            
        out.append(get_avg(ds.sel(time = dn)))
         
    return pd.concat(out)


