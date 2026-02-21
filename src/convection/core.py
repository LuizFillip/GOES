import gzip
import numpy as np
import pandas as pd 
import datetime as dt 
import os 
import xarray as xr


def read_gzbin(f_name,  lat_max =  12.0, lon_min = -100.0, dy = 0.04):
 
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





class CloudyTemperature(object):
 
    @property
    def to_dataset(self):
        data = self.structured_data(
            self.lon, 
            self.lat, 
            self.data
            )
        ds = pd.DataFrame(
            data, 
            columns = ['lon', 'lat', 'temp']
            )
        
        ds['time'] = self.dn
        
        return ds 
    
 
    @staticmethod
    def structured_data(nlons, nlats, grid):
        x, y = np.meshgrid(nlons, nlats)
        
        x = x.reshape(-1)
        y = y.reshape(-1)
        grid_means = grid.reshape(-1)
        
        return np.column_stack((x, y, grid_means))



