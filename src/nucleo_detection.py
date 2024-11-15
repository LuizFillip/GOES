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
        try:
            out.append(nucleos_catalog(file))
        except:
            continue
    return pd.concat(out)




def start_process(year):
    
    root = 'GOES/data/'
          
    path_year = f'{root}{year}/'
    
    b.make_dir(path_year)
    
    dates = pd.date_range(
        dt.datetime(year, 8, 1),
        dt.datetime(year, 12, 31), 
        freq = '1M'
        )
    
    for dn in dates:
        df = run_nucleos(dn, b = 'D')
        
        df.to_csv(f'{path_year}{dn.month}') 

start_process(2021)

