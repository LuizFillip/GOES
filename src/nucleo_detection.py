from scipy.ndimage import label, find_objects
import numpy as np 
import pandas as pd 
import GOES as gs 
import os 
from tqdm import tqdm 
import datetime as dt 


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
        
        if by_indexes:
            if (x_end == xmax):
                x_end = -1
            if (y_end == ymax):
                y_end = -1
            
            x_stt, x_end = lons[x_stt], lons[x_end]
            y_stt, y_end = lats[y_stt], lats[y_end] 
        
        area = abs((y_end - y_stt) * (x_end - x_stt))
        
        if area > area_threshold:
            out.append([x_stt, x_end, y_stt, y_end, area])
            
    columns = ['x0', 'x1', 'y0', 'y1', 'area']
    
    ds = pd.DataFrame(out, columns = columns)
    
    ds['time'] = dn
    
    return ds.set_index('time')
        

def nucleos_catalog(fname):
    
    ds = gs.CloudyTemperature(fname)
    data = ds.data
    lons = ds.lon 
    lats = ds.lat
    
    ds = find_nucleos(
            data, 
            lons, 
            lats[::-1], 
            ds.dn
            )

    return ds 
def goes_path(dn, b = 'E'):
    
    mn = dn.strftime("%m")
    yr = dn.strftime("%Y")
    return f'{b}:\\database\\goes\\{yr}\\{mn}\\'
    

def walk_goes(dn, b = 'E'):
    
    path = goes_path(dn, b)
    
    return [os.path.join(path, f) for f in os.listdir(path)]


def run_nucleos(dn, b = 'E'):
    io = dn.strftime('%Y-%m')
    out = []
    for file in tqdm(walk_goes(dn, b), io):
        
        out.append(nucleos_catalog(file))
        
    return pd.concat(out)


dates = pd.date_range(
    dt.datetime(2013, 1, 1),
    dt.datetime(2017, 12, 31), 
    freq = '1M'
    )

def start_process(dates):
    out = []
    for dn in dates:
       
        out.append(run_nucleos(dn, b = 'D'))

    df = pd.concat(out)
    
    df.to_csv('test_goes2') 
    
# start_process(dates)

# fname = 'GOES/data/S10635346_201801010000.nc'

fname = 'S10635346_201904011030.nc'

