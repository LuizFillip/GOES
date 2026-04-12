import gzip
import numpy as np
import xarray as xr
import base as b 
import GOES as gs
 
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

def load_top_cloud(dn):
    fn = gs.get_path_by_dn(dn)
    
    if dn.year >= 2018:
        return read_dataset(fn)
    else:
        return read_gzbin(fn)


def load_nuclei(year):
    path = f"GOES/data/nucleos_40/{year}"
    df = b.load(path).copy()
 
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    return df 
def filter_space(
        df, lon_min, lon_max, 
                 lat_min, lat_max):
        
    return df.loc[
        (df['lon'] > lon_min) &
        (df['lon'] < lon_max) & 
        (df['lat'] > lat_min) &
        (df['lat'] < lat_max)
        ]

def nucleos_by_time(
    year = 2013,
    freq = "1D",
    area = 0,
    lon_min = -70,
    lon_max = -50,
    lat_min = -10,
    lat_max = 0,
):
    df = load_nuclei(year)
    
    df = filter_space(
            df,
            lon_min = lon_min,
            lon_max = lon_max,
            lat_min = lat_min,
            lat_max = lat_max,
        )
    
    df = df.loc[df["area"] > area]
    
    if freq is not None:
        ds = df.resample(freq).size().rename("nucleos")
        return ds.to_frame()
    else:
        return df 

def test_load_top_cloud():
    import datetime as dt 
    
    dn = dt.datetime(2013, 1, 1)
    load_top_cloud(dn)