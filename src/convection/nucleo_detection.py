from scipy.ndimage import label, find_objects
import numpy as np 
import pandas as pd 
import GOES as gs 
import os 
from tqdm import tqdm 
import datetime as dt 
import base as b 


def find_nucleos(
        data, 
        lons, 
        lats,
        dn,
        area_threshold = 1,
        temp_threshold = -60,
        by_indexes = True
        ):
    
    data = np.where(data > temp_threshold, np.nan, data)
    
    lab_array, num_features = label(~np.isnan(data))
        
    ymax, xmax = data.shape
    
    out = []
    for i, region in enumerate(find_objects(lab_array)):
       
        x_stt, x_end = region[1].start, region[1].stop
        y_stt, y_end = region[0].start, region[0].stop
        
        dat  = data[x_stt: x_end, y_stt: y_end]
        
        if dat.size > 0 and not np.all(np.isnan(dat)):
            avg_temp = np.nanmean(dat)
        else:
            avg_temp = np.nan 
        
        if by_indexes:
            if (x_end == xmax):
                x_end = -1
            if (y_end == ymax):
                y_end = -1
            
            x_stt, x_end = lons[x_stt], lons[x_end]
            y_stt, y_end = lats[y_stt], lats[y_end] 
        
        area = abs((y_end - y_stt) * (x_end - x_stt))
        
        if area > area_threshold:
            out.append(
                [x_stt, x_end, y_stt, y_end, area, avg_temp]
                )
            
    columns = ['lon_min', 'lon_max', 
               'lat_min', 'lat_max', 
               'area', 'temp']
    
    ds = pd.DataFrame(out, columns = columns)
    
    ds['time'] = dn
    
    return ds.set_index('time').dropna()
        

def nucleos_catalog(fname):
    
    ds = gs.CloudyTemperature(fname)
    data = ds.data
    lons = ds.lon 
    lats = ds.lat
    
    ds = find_nucleos(
            data, 
            lons, 
            lats[::-1], 
            ds.dn,
            area_threshold = 1,
            temp_threshold = -30,
            by_indexes = True
            )

    return ds 
  

def walk_goes(dn, B = 'E'):
    
    mn = dn.strftime("%m")
    yr = dn.strftime("%Y")
    
    path =  f'{B}:\\database\\goes\\{yr}\\{mn}\\'
    
    return [os.path.join(path, f) for f in os.listdir(path)]


def run_nucleos(dn, B = 'E'):
    root = 'GOES/data/'
          
    path_year = f'{root}{dn.year}/'
    
    b.make_dir(path_year)
    
    io = 'Detection'
    
    out = []
    
    for file in tqdm(walk_goes(dn, B), io):
        try:
            out.append(nucleos_catalog(file))
        except:
            continue
        
    df = pd.concat(out)
    
    df.to_csv(f'{path_year}{dn.month}') 
    
    return df 

def start_process(year):
    
    root = 'GOES/data/'
          
    path_year = f'{root}{year}/'
    
    b.make_dir(path_year)
    
    dates = pd.date_range(
        dt.datetime(year, 10, 1),
        dt.datetime(year, 12, 31), 
        freq = '1M'
        )
    
    for dn in dates:
        df = run_nucleos(dn, B = 'D')
        
        df.to_csv(f'{path_year}{dn.month}') 
    
    return None 


# start_process(2022)
def test_run():
    fname = 'E:\\database\\goes\\2019\\04\\S10635346_201904010030.nc'
    dn = gs.fname2date(fname)
    ds = gs.CloudyTemperature(fname)
    dat, lon, lat = ds.data, ds.lon, ds.lat
    lat = lat[::-1]
    
    df = find_nucleos(
            dat, 
            lon, 
            lat,
            dn,
            area_threshold = 1,
            temp_threshold = -30,
            by_indexes = True
            )
    