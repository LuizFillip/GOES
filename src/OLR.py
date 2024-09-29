import xarray as xr 
import base as b 
import GEO as gg 
import pandas as pd 
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np 


def OLR_Map(df, dn ):
    fig, ax = plt.subplots(
         figsize = (10, 10), 
         dpi = 300, 
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    gg.map_attrs(
        ax, dn.year, 
        grid = False,
        degress = None
        )
    
    lon = df['lon'].values
    lat = df['lat'].values
    values = df['olr'].values
    
    img = ax.contourf(
        lon,
        lat, 
        values, 
        30, 
        cmap = 'jet'
        )
    
    ticks = np.arange(values.min(), values.max(), 50)
    b.colorbar(
            img, 
            ax, 
            ticks, 
            label = 'OLR (Watts/$m^2$)', 
            height = "100%", 
            width = "10%",
            orientation = "vertical", 
            anchor = (.25, 0., 1, 1)
            )
    
    ax.set(title = dn.strftime('%Y-%m-%d'))
    gg.plot_rectangles_regions(ax, dn.year)

b.config_labels()
import PlasmaBubbles as pb 

infile = 'GOES/data/olr.cbo-2.5deg.day.mean.nc'
ds = xr.open_dataset(infile)
ds['lon'] = ds['lon'] - 180
ds['time'] = pd.to_datetime(ds['time'])



def select_data_by_time(ds, dn):
    
    df = ds.sel(time = dn)
    
    df = df.to_dataframe()
    
    df['lon'] = df.index.get_level_values(1)
    df['lat'] = df.index.get_level_values(0)
    
    df.index = df['time']
    
    del df['time']
    
    return df

def get_averages_by_sector(df, dn):
    
    out = {}
    for sector in np.arange(-80, -40, 10):
        
        data_filtered = pb.filter_region(df, dn.year, sector)
        out[sector] = data_filtered['olr'].mean()
    
    return pd.DataFrame(out, index = [dn])

from tqdm import tqdm 

def run_in_avg(ds):
    dates = pd.date_range('2013-01-01', '2023-12-31')
    
    out = []
    
    for dn in tqdm(dates, 'OLR-avg'):
        df = select_data_by_time(ds, dn)
        
        out.append(get_averages_by_sector(df, dn))
        
        
    return pd.concat(out)

df = run_in_avg(ds)
ds.to_csv('GOES/data/OLR_avg')

