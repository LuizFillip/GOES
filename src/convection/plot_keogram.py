import GOES  as gs 
import numpy as np
import datetime as dt 
import pandas as pd 
from tqdm import tqdm 


# ax  = gs.plot_cloud_top_temperature(lon, lat, temp, dn = gs.fn2dn(fn))

# ax.axvline(-60, lw = 2, color = 'w')


def structured_data(nlons, nlats, grid):
    x, y = np.meshgrid(nlons, nlats)
    
    x = x.reshape(-1)
    y = y.reshape(-1)
    grid_means = grid.reshape(-1)
    
    data = np.column_stack((x, y, grid_means))

    return pd.DataFrame(
        data, 
        columns = ['lon', 'lat', 'temp']
        )

def select_lon(lon, lat, temp, dn, lon_sel = -60):
    df = structured_data(lon, lat, temp)
    
    ds = df.loc[df['lon'] == lon_sel]
    
    ds['time'] = dn
    
    ds = ds.set_index('time')
    
    return ds 



def run_by_month(ref, lon_sel = -60):
    
    files = gs.walk_goes(ref, B="D")
    
    out = []
    desc = f'Nucleo keogram - {ref.date()}'
    
    for fn in tqdm(files, desc):
        
        dn = gs.fn2dn(fn)
        
        if (dn.hour == 0 or dn.hour == 6):
            lon, lat, temp = gs.read_gzbin(fn)
            
            out.append(
                select_lon(
                    lon, lat, temp, dn,
                    lon_sel = lon_sel)
                )
        
    return pd.concat(out)

def run_by_year( year = 2015):
      
    out = []
    for month in range(1, 13):
        
        ref = dt.datetime(year, month, 1)
      
        out.append(run_by_month(ref))
        
    df = pd.concat(out)
    
    df.to_csv('test_keo')
    
    return df 
    
# df = run_by_year( year = 2015)