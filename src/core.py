import gzip
import numpy as np
import pandas as pd 
import datetime as dt 
from tqdm import tqdm 
import os 
import xarray as xr



        
def read_gzbin(f_name):
 
    with gzip.open(f_name, 'rb') as f:
        
        dados_binarios = np.frombuffer(
            f.read(), 
            dtype = np.int16
            )

        image_size = [1714, 1870]
        # image_size = [1200, 1335]
        data_bin = dados_binarios.reshape(image_size)
    
        return data_bin / 100 - 273.13

def read_dataset(fname):
    
    ds = xr.open_dataset(fname)
    
    ds['Band1'] = ds['Band1']  / 100 - 273.13
    
    data = ds['Band1'].values 
    lats = ds['lat'].values
    lons = ds['lon'].values 
    return lons, lats, data 


def fname2date(fname):
    dn = fname.split('_')[-1][:-3]
    try:
        return dt.datetime.strptime(dn, '%Y%m%d%H%M')
    except:
        return dt.datetime.strptime(dn, '%Y%m%d%H%M%S')




class CloudyTemperature(object):
    
    def __init__(self, fname):
        self.fname = fname
        
        self.dn = fname2date(fname)
        
        if self.dn.year < 2018:
            self.data = read_gzbin(fname)
            shape = self.data.shape
            self.lon = np.arange(shape[1]) * 0.04 - 100
            self.lat = np.arange(shape[0]) * 0.04 - 50
        else:
            lon, lat, data = read_dataset(fname)
            self.lon = lon
            self.lat = lat
            self.data = data
            
            
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
    
    @property
    def to_pivot(self):
        ds = self.to_dataset()
        return pd.pivot_table(
            ds, 
            columns = 'lon', 
            index = 'lat', 
            values = 'temp'
            )
    
    @staticmethod
    def structured_data(nlons, nlats, grid):
        x, y = np.meshgrid(nlons, nlats)
        
        x = x.reshape(-1)
        y = y.reshape(-1)
        grid_means = grid.reshape(-1)
        
        return np.column_stack((x, y, grid_means))




def load_files(ref_day):
    path = 'E:\\database\\goes\\'

    files = os.listdir(path)

    if ref_day is not None:
        files  = [f for f in files if fname2date(f) < ref_day]
   
    return [os.path.join(path, f) for f in files]

def CloudTopKeogram(files, lon = -55):
    out = []
    
    for fname in tqdm(files, 'KEO'):

        CT = CloudyTemperature(fname)
        
        ds = CT.to_dataset()
        out.append(ds.loc[ds['lon'] == lon])
     
    ds = pd.concat(out)
    
    # # fig = plot_keogram(ds1, ax = None)
    # time = ds1.columns
    # time = [b.dn2float(t, sum_from = None) for t in time]
    # lats = ds1.index
    # data = ds1.values[::-1]
    return pd.pivot_table(
        ds, 
        values = 'temp', 
        columns = 'time', 
        index = 'lat'
        )



