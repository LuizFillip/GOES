import pandas as pd 
import scipy.io
import numpy as np 


def latitudinal_data_ep(
        year = 2013,
        lat_min = -10,
        lat_max = 0
        ):
    
    key = f'Latitudinal_Monthly_Means_{abs(lat_min)}_{abs(lat_max)}'
    
    raw = scipy.io.loadmat('GOES/data/Monthly_Mean_EP.mat')

    values = raw[key][0][0]
    
    data = values[4]
    
    index = pd.date_range(
        '2013-01-01', 
        '2022-12-31', 
        freq = '1M'
        )
    
    heights = np.arange(20, 111)
    
    ds = pd.DataFrame(
        data, 
        index = index, 
        columns = heights
        )
    
    return ds.loc[ds.index.year == year]


def group_by_time(
        df, 
        stp = 'month', 
        col = '90_110', 
        name = 'wave'
        ):
    
    col = f'mean_{col}'
    
    df['month'] = df.index.month 
    df['year'] = df.index.year
    
    df = df.between_time(
        '18:00', '05:00')
    
    df = df.groupby([stp])[col].mean()

    return df.to_frame(name)