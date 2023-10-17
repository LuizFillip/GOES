<<<<<<< HEAD
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
=======
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:59:32 2023

@author: Luiz
"""

import xarray as xr
import numpy as np
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib import ticker, cm
import time 
import cartopy.io.img_tiles as cimgt



# Carregue seus dados binários aqui (depende do formato)
def read_gzbin(f_name, threshold):
    # import necessary libraries
    import numpy as np
    import gzip
    from datetime import datetime
    
    # extract date and time from file name
    date_str = f_name[-15:-3]
    date_obj = datetime.strptime(date_str, '%Y%m%d%H%M')#%S
    
    # read binary data from gzip-compressed file
    with gzip.open(f_name, 'rb') as f:
        uncompressed_data = f.read()
        dados_binarios = np.frombuffer(uncompressed_data, dtype=np.int16)

        
        # reshape binary data into a 2D numpy array
        imageSize = [1800,1800]
        dados_binarios = dados_binarios.reshape(imageSize)
        
        # Define x and y positions
        dlon=np.arange(dados_binarios.shape[1]) * 0.04 - 100
        dlat=np.arange(dados_binarios.shape[0]) * 0.04 - 50
        
        
        # return the 2D numpy array, dlon, dlat, and date_obj
        return dados_binarios, dlon, dlat, date_obj


caminho = 'C:/2023/Beckup_note/ANDERSON/PCI_D_inpe_2023\
/mapas_temp_nuvem_python/03-06-2005-goes12_ch4/'                              

# f_name='gcr.050602.0200_0200g.ch4'
nome = 'S10216956_200506020330.gz'

f_name = caminho+nome

saida = caminho 

#Deletes values higher than -65 celcius degress
threshold = 0. 
data, dlon, dlat, date_obj = read_gzbin(f_name, threshold)
###====================================================================
>>>>>>> cf7f95ccc0c59f8414b62e2c7b376b9ca550b840
