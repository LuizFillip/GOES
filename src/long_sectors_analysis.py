import base as b 
import core as c 
import pandas as pd
import GEO as gg
import datetime as dt




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
    
    df = b.load('nucleos')

    df['start'] = pd.to_datetime(df['start'])

    df = df.loc[
        (df['start'].dt.time < dt.time(6, 0)) |
        (df['start'].dt.time > dt.time(21, 0)) |
        (df['area'] > 40)
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

import PlasmaBubbles as pb 

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


import matplotlib.pyplot as plt 
import numpy as np 

sector = -70 

def concat_nucleos_and_bubbles(sector):
    
    ds1 = number_of_nucleos(sector)
    
    ds2 = number_of_bubbles(sector)
    
    ds = pd.concat([ds1, ds2], axis = 1)
    
    ds.columns = [ 'cloud', 'epb']
    
    ds = ds.dropna()
    
    return ds 



fig, ax = plt.subplots(
    figsize = (12, 6),
    sharex=True, 
    sharey=True, 
    dpi = 300, ncols = 3)


for i, sector in enumerate(np.arange(-70, -40, 10)):
    
    ds = concat_nucleos_and_bubbles(sector)

    ax[i].scatter(ds['cloud'], ds['epb'])
    
    ax[i].set(title = sector, xlabel = '')
