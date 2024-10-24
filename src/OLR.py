import pandas as pd 
import base as b 
import numpy as np
import GEO as gg 
import cartopy.crs as ccrs
import matplotlib.pyplot as plt 
import datetime as dt 

infile = 'GOES/data/Select_ep_data_lat_lon_2013.txt'

b.config_labels()


def plot_regions(
        ax, 
        x_stt, y_stt, 
        x_end, y_end, 
        number = None
        ):
    
  
    rect = plt.Rectangle(
    (x_stt, y_stt), 
    x_end - x_stt, 
    y_end - y_stt,
    edgecolor = 'k', 
    facecolor = 'none', 
    linewidth = 3
    )
    
    ax.add_patch(rect)
    
    if number is not None:
        middle_y = (y_end + y_stt) / 2
        middle_x = (x_end + x_stt) / 2
        
        ax.text(
            middle_x, 
            middle_y + 1, number, 
            transform = ax.transData
            )
    return ax 

def tracker_plot(ds):
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 10),
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
    
    for index, row in ds.iterrows():
        
        plot_regions(
            ax,
            row['x0'], 
            row['y0'],
            row['x1'], 
            row['y1'], 
            # i = indexs
            )
        
        ax.scatter(row['mx'], row['my'], s = 100, color = 'red')
    return ax 
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

def tracker_clouds(ds):
    times = pd.to_datetime(np.unique(ds.index))

    ds = ds.loc[ds['area'] > 50]
    i = 0
    ds1 = ds.loc[ds.index == times[i]]
    
    ds2 = ds.loc[ds.index == times[i + 1]]
    
    for i, s1 in enumerate(ds1['mx'].values):
        for j, s2 in  enumerate(ds2['mx'].values):
            if abs(s1 - s2) < 1:
                print(ds1.iloc[i, :], ds2.iloc[j, :],)
    

# df = load_tunde(infile)
# for index, row in df1.iterrows():
    
# df1['mean_90_110'].max()
# df['mean_90_110'].resample('15D').mean().plot()


ds = b.load('test_goes')

dn = dt.datetime(2013, 1, 2)
delta = dt.timedelta(days = 1)
ds = ds.loc[(ds.index > dn) & (ds.index < dn + delta)]

ds['mx'] = (ds['x1'] + ds['x0']) / 2
ds['my'] = (ds['y1'] + ds['y0']) / 2



ax = tracker_plot(ds)

ax.set(title = dn)

# ds