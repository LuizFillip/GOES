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

year = 2019

infile = f'GOES/data/olr-daily_v01r02_{year}0101_{year}1231.nc'
infile = 'GOES/data/olr.cbo-2.5deg.day.mean.nc'
ds = xr.open_dataset(infile)

ds['time'] = pd.to_datetime(ds['time'])

dn = dt.datetime(year, 6, 1)

df = ds.sel(time = dn)
    
OLR_Map(df, dn)

# df