import gzip
import numpy as np
import xarray as xr
# import GOES as gs
import pandas as pd 
import GEO as gg 

def read_gzbin2(fname):
    with gzip.open(fname, 'rb') as f:
        uncompressed_data = f.read()
        data = np.frombuffer(
            uncompressed_data, dtype= np.dtype('>i2'))
        image_size = [1200, 1335]
        
        reshaped_array = data.reshape(image_size)
        
    return reshaped_array / 100 - 273.13
        
        
def read_gzbin(f_name):
 
    with gzip.open(f_name, 'rb') as f:
        
        dados_binarios = np.frombuffer(
            f.read(), 
            dtype = np.int16
            )

        image_size = [1714, 1870]
        
        data_bin = dados_binarios.reshape(image_size)
    
        return data_bin / 100 - 273.13





def fname2date(fname):
    dn = fname.split('_')[-1][:-3]
    return dt.datetime.strptime(dn, '%Y%m%d%H%M')


import datetime as dt 


fname = 'GOES/data/S10236964_201301010000.gz'
# fname = 'GOES/data/S11232404_201401022300.gz'
data = read_gzbin2(fname)

import matplotlib.pyplot as plt 
import GOES 
from matplotlib import cm
import cartopy.crs as ccrs


def mapping_plot(data):

    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
    dlon = np.arange(data.shape[1]) * 0.04 - 100
    dlat = np.arange(data.shape[0]) * 0.04 - 50
    path = 'GOES/src/IR4AVHRR6.cpt'
    
    cmap = cm.colors.LinearSegmentedColormap(
        'cpt', GOES.loadCPT(path)) 
    
    
    fig, ax = plt.subplots(
             figsize = (12, 12), 
             dpi = 300, 
             subplot_kw = 
             {'projection': ccrs.PlateCarree()}
             )
    
    gg.map_attrs(
        ax, 2013, 
        lat_lims  = lat_lims, 
        lon_lims = lon_lims,
        grid = False,
        degress = None
        )
    
    
    img = ax.contourf(dlon, dlat, data, 50, cmap = cmap)
    
    plt.colorbar(img)
    
    
data 

# mapping_plot(data)