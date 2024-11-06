import base as b 
import core as c 
import pandas as pd
import GEO as gg
import datetime as dt
import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import numpy as np 




def group_by_month(df):

    ds = df.groupby(
        ['month', 'sector']
        ).size().reset_index(name='occs')
    
    ds = pd.pivot_table(
        ds, 
        columns = 'sector', 
        index = 'month', 
        values = 'occs'
        )


def number_of_nucleos(sector):
    
    df = b.load('nucleos2')

    df['start'] = pd.to_datetime(df['start'])

    df = df.loc[
        (df['start'].dt.time < dt.time(6, 0)) |
        (df['start'].dt.time > dt.time(21, 0)) |
        (df['area'] > 10)
                ]

    df['month'] = df.index.to_period('M').to_timestamp()
    
    ds = df.groupby(
        ['month', 'sector']
        ).size().reset_index(name='occs')
    
    ds = pd.pivot_table(
        ds, 
        columns = 'sector', 
        index = 'month', 
        values = 'occs'
        )
    
    ds = ds.replace(float('nan'), 0)
    
    ds.index = pd.to_datetime(ds.index)
    
    
    return ds.loc[:, [sector]].astype(int)


def number_of_bubbles(sector):
    
    ds = b.load('events_class2')

    df = pb.sel_typing(
            ds, 
            typing = 'midnight', 
            indexes = False, 
            year = 2023
            )
    
    df = c.seasonal_yearly_occurrence(
            df, 
            sector
            )
    df.index = pd.to_datetime(df.index)
    
    return df



sector = -70 

def concat_nucleos_and_bubbles(sector):
    
    ds1 = number_of_nucleos(sector)
    
    ds2 = number_of_bubbles(sector)
    
    ds = pd.concat([ds1, ds2], axis = 1)
    
    ds.columns = [ 'cloud', 'epb']
    
    ds = ds.dropna()
    
    return ds 


def plot_scatter_correlation():
    
    sectors = np.arange(-80, -40, 10)
    
    fig, ax = plt.subplots(
        figsize = (12, 6),
        sharex=True, 
        sharey=True, 
        dpi = 300, 
        ncols = len(sectors)
        )
    
    
    for i, sector in enumerate(sectors):
        
        ds = concat_nucleos_and_bubbles(sector)
    
        ax[i].scatter(ds['epb'], ds['cloud'], )
        
        ax[i].set(title = sector, xlabel = '')
    

def split_in_sector():
    
    df = b.load('nucleos2')
    
    df['start'] = pd.to_datetime(df['start'])
    
    df = df.loc[
        (df['start'].dt.time < dt.time(6, 0)) |
        (df['start'].dt.time > dt.time(21, 0)) |
        (df['area'] > 40)
                ]
    
    
    df['month'] = df.index.month
    
    
    df['month'] = df.index.to_period('M').to_timestamp()
    
    ds = df.groupby(
        ['month', 'sector']
        ).size().reset_index(name='occs')
    
    ds = pd.pivot_table(
        ds, 
        columns = 'sector', 
        index = 'month', 
        values = 'occs'
        )
    
    ds.index = (ds.index.year + ds.index.month / 12)
    
    ds.index = np.round(ds.index, 2)


# ds = df.groupby(
#     ['month', 'sector']
#     ).size().reset_index(name='occs')

# ds = pd.pivot_table(
#     ds, 
#     columns = 'sector', 
#     index = 'month', 
#     values = 'occs'
#     )

# plt.plot(ds)

# ds.plot(lw = 3, subplots = True)

plot_scatter_correlation()