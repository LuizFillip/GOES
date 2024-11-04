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
        number = None, 
        color = 'k'
        ):
    
  
    rect = plt.Rectangle(
    (x_stt, y_stt), 
    x_end - x_stt, 
    y_end - y_stt,
    edgecolor = color, 
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

def tracker_plot(ax, ds, color = 'k'):
   
    
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
            color = color
            )
        
        mx = (row['x1'] + row['x0']) / 2
        my = (row['y1'] + row['y0']) / 2
        ax.scatter(mx, my, s = 100, color = 'red')
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



def coord_diff_on_data(df, threshold = 2):

    df['dx0'] =  df['x0'].diff().abs()
    df['dy0'] =  df['y0'].diff().abs()
    df['dx1'] =  df['x1'].diff().abs()
    df['dy1'] =  df['y1'].diff().abs()
    
    df = df.replace(np.nan, 0)
    
    cols = ['dx0', 'dy0', 'dx1', 'dy1']
    mask = (df[cols] < 1).sum(axis=1) >= 4
    
    df_filt = df[mask].copy()
    
    rt = df_filt.index.to_series(
            ).diff().fillna(
        pd.Timedelta(seconds = 0)
        )
    
    df_filt['dtime'] =  (
        rt.dt.components['hours'] +      
        rt.dt.components['minutes'] / 60       
        )     
                   
    df_filt['group'] = (
        df_filt['dtime'] >= threshold
        ).cumsum()
    
    return df_filt.iloc[:, 4:]

def sequential_blocks(df):
    
    df_filtered = coord_diff_on_data(df)
    intervalo_max = pd.Timedelta(hours=0.5)
    
    bloco_atual = []
    blocos_sequenciais = []
    
    for i, (time, row) in enumerate(df_filtered.iterrows()):
        if i == 0 or row['time_diff'] <= intervalo_max:
            bloco_atual.append(row)
        else:
            # Se não for sequencial, salva o bloco atual e começa um novo
            if bloco_atual:
                blocos_sequenciais.append(pd.DataFrame(bloco_atual))
            bloco_atual = [row]
     

    if bloco_atual:
        blocos_sequenciais.append(pd.DataFrame(bloco_atual))
    
    for bloco in blocos_sequenciais:
        bloco.drop(columns=['time_diff'], inplace = True)
        
    return blocos_sequenciais
    

# fig, ax = plt.subplots(
#      dpi = 300, 
#      figsize = (10, 10),
#      subplot_kw = 
#      {'projection': ccrs.PlateCarree()}
#      )

def filter_region(df, sector, year = 2013):
    '''filter region'''
    corners = gg.set_coords(year)

    xlim, ylim = corners[sector]
    
    return df.loc[
        (df['x0'] > xlim[0]) & 
        (df['x1'] < xlim[1]) & 
        (df['y0'] > ylim[0]) & 
        (df['y1'] < ylim[1])
        ]


def built_area_locator_time(df, sector):
    
    start_time = df.index.min()
    end_time = df.index.max()
    area_sum = df['area'].mean()
    time_sum = df['dtime'].sum()
    
    result = {
        'time': time_sum, 
        'area': area_sum, 
        'start': start_time, 
        'end': end_time, 
        'sector': sector
        }
    
    dn = [start_time.date()]
    
    return pd.DataFrame(result, index = dn)




def group_of_convective_storms(ds):
    
    out = []
    for sector in np.arange(-80, -40, 10):
    
        df1 = coord_diff_on_data(
            filter_region(ds, sector).copy()
            )
               
        valid_intervals = df1[df1['dtime'] < 2].groupby('group')
    
        for group_id, group_df in valid_intervals:
            
            out.append(
                built_area_locator_time(
                    group_df, sector
                    )
                )
            
    return pd.concat(out)

from tqdm import tqdm 

ds = b.load('test_goes')

ds = ds.loc[~(ds['area'] > 1000)]
delta = dt.timedelta(days = 1)


times = pd.date_range('2013-01-01', '2017-12-31')

out = []
for dn in tqdm(times):
    ds1 = ds.loc[(ds.index > dn) & (ds.index < dn + delta)]
    try:
        out.append(group_of_convective_storms(ds1))
    except:
        continue
    
df = pd.concat(out)

#%%%%


df.to_csv('nucleos')

    
