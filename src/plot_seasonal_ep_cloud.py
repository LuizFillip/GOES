import pandas as pd 
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os
import numpy as np 

import base as b 

b.config_labels(fontsize = 25)
pathfile = r"F:/SABER_ALL_DATA/SABER_PROCESS_EP_DAILY_2024/Trabalho_Luiz/Plots/"  


def load(infile, date_index = False):
    
    try:
        df = pd.read_csv(infile, index_col = 0)
        df.index = pd.to_datetime(df.index) #, format='ISO8601')
        
    except:
        df = pd.read_csv(
            infile, delimiter = ';', index_col = 0
            )
        df.index = pd.to_datetime(df.index, format='ISO8601')

    
    if date_index:
        df.index = df.index.date

    return df.sort_index()




def limits(df, 
           x0 = -80, x1 = -40, 
           y0 = -10, y1 = 0):
    return  df.loc[
        ((df['Lon'] > x0) & (df['Lon'] < x1)) &
        ((df['Lat'] > y0) & (df['Lat'] < y1))
        ]

x0 = -80
x1 = -40
y0 = -50
y1 = 20


path_nucleos = 'GOES/data/nucleos/'
path_ep = 'GOES/data/Ep/'

def potential_energy(year = 2019, sample = 'M'):
    
    df = pd.read_csv(f'{path_ep}{year}', sep = '\s+')

    df.index = pd.to_datetime(
        df['Date'] + ' ' + 
        df[['Hour', 'Minute', 'Second']
           ].astype(str).agg(':'.join, axis=1))
    
    df = df.drop(
        columns = [
        'Year', 'DOY', 'Date', 
        'Hour', 'Minute', 'Second']
        )
    
    df = limits(df, x0, x1 , y0, y1)
    
    # print(df['Lat'].min(), df['Lat'].max())
    
    return df.resample(sample).mean()

def load_nucleos(year = 2019, sample = '15D'):
    
    df = load(f'{path_nucleos}/{year}')
    
    df['Lon'] = (df['x1'] + df['x0']) / 2
    df['Lat'] = (df['y1'] + df['y0']) / 2
    
    df = limits(df, x0, x1, y0, y1)
    df = df.resample(sample).size() 
    df = (df / df.values.max()) * 100
    
    return df


def plot_seasonal(df, ds, title):

    fig, ax = plt.subplots(
          dpi = 300, 
          figsize = (12, 8)
          )
        
    sdf = gaussian_filter(df, sigma = 1)

    ax.plot(
        df.index,
        sdf, 
        lw = 3, 
        color = 'blue'
        )

    ax.set(
        ylim = [0, 100], 
        ylabel = r'Convective activity (%)',
        xlabel = 'Years'
        )
    
    
    ax1 = ax.twinx()
    sds = gaussian_filter(ds, sigma = 1)
    
    ax1.plot(ds.index, sds, lw = 3, color = 'red')
    
    io = f': Lat = {y0}/{y1}, Lon = {x0}/{x1}'
    
    ax1.set(
        title = title.title() + io,
        ylabel = 'GW potential energy (J/Kg)', 
        xlabel = 'Years'
        )
    
    # print(df)
    con_ds = pd.concat([ds, df], axis = 1).dropna()

    x, y = con_ds.iloc[:, 0].values, con_ds.iloc[:, 1].values
    correlation = np.corrcoef(x, y)[0, 1]
    corr_text = f'Correlation: {correlation:.3f}'
    
    ax.text(
         0.95, 0.05, 
         corr_text, 
         transform=ax.transAxes, 
         fontsize=35, 
         verticalalignment='bottom', 
         horizontalalignment='right'
     )
    return fig

def save_figures(fig, output_path):
     
     plt.tight_layout()
     plt.savefig(output_path)
     plt.close(fig)
     
     return None 

def get_couples(col, sample = 'M'):
    
    out_1 = []
    out_2 = []
    
    for year in range(2013, 2023, 1):
        out_1.append(load_nucleos(year , sample))
        out_2.append(potential_energy(year, sample)[col])
        
    
    return pd.concat(out_1), pd.concat(out_2)

cols = ['mean_20_30', 'mean_30_40', 
        'mean_40_50', 'mean_50_60', 
        'mean_60_70', 'mean_70_80', 
        'mean_80_90', 'mean_90_100', 
        'mean_100_110']

save = False 

cols = ['mean_20_60', 'mean_60_90', 'mean_90_110']

def plot_figures_by_col(cols):
    
    for i, col in enumerate(cols):
        df, ds = get_couples(col)
        fig = plot_seasonal(df, ds, title = col)
        
        if save:
            output_path = os.path.join(pathfile, f"fig_{i}.png")
            save_figures(fig, output_path)

# col = 'mean_90_110'
# col = 'mean_60_90'
# df, ds = get_couples(col)
# fig = plot_seasonal(df, ds, title = col)
