import numpy as np 
import base as b 
import matplotlib.pyplot as plt 
import GOES as gs

b.config_labels(fontsize = 22)











def count_in_sector(ds, sample = '1M'):
    
    ds = ds.resample(sample).size() 
    
    return (ds / ds.values.max()) * 100

def select_temp(df, temp = -50):
    return df.loc[
        (df['temp'] > temp) & 
        (df['temp'] < temp + 10)]

lat = -10
year = 2013

def pipe_clouds(year, lat, temp = -50):
    
    lat_min = lat
    lat_max = lat + 10
    
    ds = gs.load_nucleos(year)
    
    ds  = gs.filter_space(
            ds, 
            x0 = -80, 
            x1 = -40, 
            y0 = lat_min, 
            y1 = lat_max
            )
    
    ds = select_temp(ds, temp = temp)
    
    return count_in_sector(
        ds, sample = '1M')

import pandas as pd 
from tqdm import tqdm 

def concat_years(lat, temp = -50):
    
    out_cloud = []
    out_waves = []
    for year in tqdm(range(2013, 2023)):
        
        try:
            data1 = pipe_clouds(year, lat, temp)
            
            out_cloud.append(data1)
        except:
          
            continue
        
        lat_min = lat
        lat_max = lat + 10
        
        data = gs.latitudinal_data_ep(
            year, lat_min, lat_max)
        
        out_waves.append(data) 
        
    cl = pd.concat(out_cloud)
    wv = pd.concat(out_waves)
    
    return cl, wv
temp = -50

def run_in_latitude(temp = -50):
    
    root = 'GOES/data/means'
    
    for lat in range(-50, 10, 10): 
    
        cl, wv = concat_years(lat, temp)
        
        name = f'lat{lat}_temp{temp}'.replace('-', '_')
        
        cl.to_csv(f'{root}/cloud/{name}')
        wv.to_csv(f'{root}/ep/{name}')
