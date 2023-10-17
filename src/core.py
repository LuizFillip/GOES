import gzip
import numpy as np
import xarray as xr

import pandas as pd 

def read_gzbin(f_name):
 
    with gzip.open(f_name, 'rb') as f:
        
        dados_binarios = np.frombuffer(
            f.read(), 
            dtype = np.int16
            )

        image_size = [1714, 1870]
        
        data_bin = dados_binarios.reshape(image_size)
    
        return data_bin / 100 - 273.13



ds = xr.open_dataset('S10635336_202110231400.nc')
data = (ds['Band1'].values / 100) * -1





def grid_mean(lon, lat, data, grid_size = 100):
    
    num_grids_x = data.shape[0] // grid_size
    num_grids_y = data.shape[1] // grid_size

    grid_means = np.zeros((num_grids_x, num_grids_y))

    new_lats = np.zeros(num_grids_y)
    new_lons = np.zeros(num_grids_x)


    for i in range(num_grids_x):
        
        new_lons[i] = lon[i * grid_size:(i + 1) * grid_size].mean()
        new_lats[i] = lat[i * grid_size:(i + 1) * grid_size].mean()
        
        for j in range(num_grids_y):
            
            
            grid = data[i * grid_size:(i + 1) * grid_size, 
                        j * grid_size:(j + 1) * grid_size]
            
            grid_mean = np.mean(grid)
            grid_means[i, j] = grid_mean

    return new_lons, new_lats, grid_means


def structured_data(nlons, nlats, grid):
    x, y = np.meshgrid(nlons, nlats)
    
    x = x.reshape(-1)
    y = y.reshape(-1)
    grid_means = grid.reshape(-1)
    
    return np.column_stack((x, y, grid_means))

def recover_dataframe(structured_data):
    ns = ['lon', 'lat', 'temp']
    df = pd.DataFrame(
        structured_data, 
        columns = ns
        )
    
    return pd.pivot_table(
        df, columns = ns[0], index = ns[1], values = ns[2])


lat = ds.lat.values
lon = ds.lon.values

nlons, nlats, grid = grid_mean(
    lon, lat, data, grid_size = 50
    )

map_attrs(nlons, nlats, grid)
