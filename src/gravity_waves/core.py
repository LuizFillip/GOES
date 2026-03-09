import pandas as pd 
import scipy.io
import numpy as np 
import os 
from tqdm import tqdm 
import base as b 

path_ep = os.getcwd() + '/GOES/data/Ep/'

def filter_space(
        df, 
        lon_min = -50, 
        lon_max = -40, 
        lat_min = -10, 
        lat_max = 10
        ):
    return  df.loc[
        ((df['lon'] > lon_min) & (df['lon'] < lon_max)) &
        ((df['lat'] > lat_min) & (df['lat'] < lat_max))
    ]


def format_altitudes_attrs(path):
    df = scipy.io.loadmat(path)
    
    alts = np.arange(20, 110.1, 0.1)
     
    ds = pd.DataFrame(index = alts)
    
    for key, vl in df.items():
        
        if len(vl) == len(alts):
            ds[key] = vl
        if len(vl) == 1:
            ds.attrs[key] = vl[0][0].round(3)
        if 'Newx' in key:
            new_key = key[:3].lower()
            ds.attrs[new_key] = vl.mean().round(3)
    
    return ds.round(3) 
 
def coords_time(fn):
    '''
    ex:  'SABER_2012_001_03_50_10_14.76_307.18_GLOBAL.mat'
    2012 é ano
    001 é DOY (dia do ano de 001 até 365/366)
    03 é hora
    50 é minuto
    10 é segundo 
    14.76 é latitude (-90 até 90 grau)
    307.18 é longitude ( 0 to 360 grau)
    '''
     
    import datetime as dt 
 
    ls = fn.split('_')
    
    year = int(ls[1])
    doy = int(ls[2])
    hour = int(ls[3])
    minute = int(ls[4])
    second = int(ls[5])
    lat = float(ls[6])
    lon = float(ls[7])
    
    dn = dt.datetime(year, 1, 1) + dt.timedelta(
        days = doy - 1, 
        hours = hour,
        minutes = minute, 
        seconds = second
        )
    return dn, lat, lon

def ep_data(path, fn):
    dn, lat, lon = coords_time(fn)
    df = format_altitudes_attrs(path + fn)
    df['dn'] = dn 
    df['lat'] = lat
    df['lon'] = lon - 360
    df['alt'] = df.index 
    return df.set_index('dn') 

def filter_bin_by_altitude(df):
    bins = np.arange(20, 121, 10)   # 20–40, 40–60, ...
    df['alt_bin'] = pd.cut(df['alt'], bins=bins)
    
    ds = df.groupby(
        ['dn', 'alt_bin', 'lat', 'lon']).agg({
        'Ep_Tprime': ['mean', 'std', 'max'] 
    })
    
    ds.columns = [
        ''.join(col).strip('_').replace(
            'Tprime', '') if isinstance(col, tuple) else col
        for col in ds.columns
    ]
    
    ds['alt'] = bins[:-1]
    
    return ds  

def pandas_attrs(df):
    return pd.DataFrame(df.attrs, index = [df.index[0]]) 



def run_saber(year, doy):
    path = f'D:\\database\\{year}\\{doy:03d}\\'

    files = os.listdir(path)
    out_ep = []
    out_at = []
    desc = f'Run saber - {doy}'
    for fn in tqdm(files, desc):
        
        df = ep_data(path, fn)
        out_ep.append(filter_bin_by_altitude(df))
        out_at.append(pandas_attrs(df))
      
        
    data = pd.concat(out_ep)
    attrs = pd.concat(out_at)
    
    return data, attrs 

def run_year(year):
    path_out = 'D:\\database\\SABER\\'

    out_ep = []
    out_at = []    
    print('Starting,', year)
    for doy in range(1, 366):
        try:
            data, attrs = run_saber(year, doy)
            out_ep.append(data)
            out_at.append(attrs)
        except:
            continue
        
    df = pd.concat(out_ep)
    ds = pd.concat(out_at)
    
    df.to_csv(f'{path_out}ep\\{year}')
    ds.to_csv(f'{path_out}attrs\\{year}')
    
    return df, ds 

# year = 2013
# df, ds = run_year(year)