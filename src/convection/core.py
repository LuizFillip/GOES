import gzip
import numpy as np
import pandas as pd 
 
import xarray as xr


def read_gzbin(
        f_name,  
        lat_max = 13.0, 
        lon_min = -100.0, 
        dy = 0.04
        ):
 
    with gzip.open(f_name, 'rb') as f:
        
        dados_binarios = np.frombuffer(
            f.read(), 
            dtype = np.int16
            )

        image_size = [1714, 1870]
        data_bin = dados_binarios.reshape(image_size)  
           
        ny, nx = tuple(image_size)

        lon = lon_min + np.arange(nx) * dy
        lat = lat_max - np.arange(ny) * dy   
        
        temp = data_bin / 100 - 273.13
        
        return lon, lat, temp
    
    
def read_dataset(fname):
    
    ds = xr.open_dataset(fname)
    
    ds['Band1'] = ds['Band1']  / 100 - 273.13
    
    data = ds['Band1'].values 
    lats = ds['lat'].values
    lons = ds['lon'].values 
    return lons, lats, data 





