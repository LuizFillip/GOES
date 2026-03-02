import pandas as pd 
import scipy.io
import numpy as np 
import os 

path_ep = os.getcwd() + '/GOES/data/Ep/'

def filter_space(
        df, 
        lon_min = -50, 
        lon_max = -40, 
        lat_min = -10, 
        lat_max = 10
        ):
    return  df.loc[
        ((df['lon'] > lon_min) & (df['lon'] < lon_max)) &
        ((df['lat'] > lat_min) & (df['lat'] < lat_max))
    ]


def potential_energy(year = 2019):
    
    df = pd.read_csv(f'{path_ep}{year}.txt', sep = '\s+')

    df.index = pd.to_datetime(
        df['Date'] + ' ' + 
        df[['Hour', 'Minute', 'Second']
           ].astype(str).agg(':'.join, axis=1)
        )
    
    df = df.drop(
        columns = [
        'Year', 'DOY', 'Date', 
        'Hour', 'Minute', 'Second']
        )
    
    df = df.rename(
        columns = {
            'Lon': 'lon', 
            'Lat': 'lat'
            }
        )
    return df


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


 

import base as b  
# df = latitudinal_data_ep(
#         year = 2013,
#         lat_min = -10,
#         lat_max = 0
#         )

# df = b.load()
infile = 'GOES/data/Select_ep_data_lat_lon_2013.txt'
# raw = scipy.io.loadmat(infile)

# raw 

df = pd.read_csv(infile, sep = '\s+')

