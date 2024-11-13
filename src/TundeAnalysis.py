import pandas as pd 
import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 

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


def plot_map():
    fig, ax = plt.subplots(
          dpi = 300, 
    
          figsize = (10,10),
          subplot_kw = 
          {'projection': ccrs.PlateCarree()}
          )
        
    
    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
    gg.map_attrs(
       ax, 2013, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )
    
    
    ax.scatter(
        df['Lon'],
        df['Lat'], 
        c = df['mean_90_110']
        )

infile = 'GOES/data/Select_ep_data_lat_lon_2013.txt'

ds = load_tunde(infile)

ds = ds.loc[(ds['Lat'] > -20) & 
            (ds['Lat'] < 10)]

sample = '5D'
ds = ds['mean_90_110'].resample(sample).mean()


infile = 'GOES/data/2013'

df = b.load(infile)

df['lon'] = (df['x1'] + df['x0']) / 2
df['lat'] = (df['y1'] + df['y0']) / 2

df = df.loc[
    (df['lat'] > -20) & 
    (df['lat'] < 10) ].resample(sample).size()


df['percent'] = (df / df.values.max()) *100


def plot_seasonal(df, ds):

    fig, ax = plt.subplots(
          dpi = 300, 
          figsize = (16, 8)
          )
        
    ax.scatter(df.index, 
               df['percent'], c = 'b' )
    df = df.rolling(10).mean()
    ax.plot(
        df.index, 
        df, 
            lw = 3, color = 'blue')
    ax.set(ylabel = 'Convective activity (\%)')
    
    b.change_axes_color(
            ax, 
            color = 'blue',
            axis = "y", 
            position = "left"
            )
    
    ax1 = ax.twinx()
    ax.scatter(ds.index, ds.values, c = 'red')
    ax1.plot(ds.index, b.smooth2(ds, 10), lw = 3, color = 'red')
    
    ax1.set(ylabel = 'GW potential energy (J/Kg)')
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    
    b.format_month_axes(ax)


plot_seasonal(df, ds)

ds