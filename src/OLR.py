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


ds = b.load('test_goes')

dn = dt.datetime(2013, 1, 5)
delta = dt.timedelta(days = 1)
ds = ds.loc[(ds.index > dn) & (ds.index < dn + delta)]


orig_df = ds.loc[ds['area'] > 10]


df = orig_df.copy() 

def coord_diff_on_data(df):

    df['dx0'] =  df['x0'].diff().abs()
    df['dy0'] =  df['y0'].diff().abs()
    df['dx1'] =  df['x1'].diff().abs()
    df['dy1'] =  df['y1'].diff().abs()
    
    df = df.replace(np.nan, 0)
    
    mask = (df[['dx0', 'dy0', 'dx1', 'dy1']] < 1).sum(axis=1) >= 4
    
    df_filtered = df[mask].copy()
    
    df_filtered['time_diff'] = df_filtered.index.to_series(
            ).diff().fillna(
        pd.Timedelta(seconds=0)
        )
    return df_filtered

def sequentioal_blocks(df):
    
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
    
    # Adiciona o último bloco se não estiver vazio
    if bloco_atual:
        blocos_sequenciais.append(pd.DataFrame(bloco_atual))
    
    for bloco in blocos_sequenciais:
        bloco.drop(columns=['time_diff'], inplace=True)
    

# fig, ax = plt.subplots(
#      dpi = 300, 
#      figsize = (10, 10),
#      subplot_kw = 
#      {'projection': ccrs.PlateCarree()}
#      )

# import matplotlib

    
# colors = list(matplotlib.colors.cnames.keys())

# colors = [c for c in colors if 'dark' in c]


# colors

# for i, bloco in enumerate(blocos_sequenciais):
#     # tracker_plot(ax, bloco, color = colors[i])
    
    
# # blocos_sequenciais