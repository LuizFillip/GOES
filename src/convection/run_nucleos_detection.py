import os 
from tqdm import tqdm 
import datetime as dt 
import base as b 
from GOES import find_nucleos

import GOES as gs

def nucleos_catalog(fname):
    ds = gs.CloudyTemperature(fname)
    df = find_nucleos(
        ds.data,
        ds.lon,
        ds.lat,
        dn=ds.dn,
        area_threshold=1,
        temp_threshold=-30,
        return_coords=True,
        connectivity=2,  # opcional: 8-conectado costuma juntar melhor
    )
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
    