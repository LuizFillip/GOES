import datetime as dt 
import GOES  as gs
import pandas as pd 
from tqdm import tqdm 

def test_one_file():
    ref = dt.datetime(year, 1, 1)
    
    files = gs.walk_goes(ref, 'D')
    
    fn = files[2]
               
    lon, lat, temp = gs.read_gzbin(fn)
    
    result = gs.compute_stats(
        lon, lat, temp, 
        gs.fn2dn(fn),
        threshold = -40
    )
    
    result

def run_days(ref, threshold = -40, B = 'D'):
    desc =  ref.strftime('%B')
 
    files = gs.walk_goes(ref, B)
    
    out = []
    
    for fn in tqdm(files, desc):
     
        lon, lat, temp = gs.read_gzbin(fn)
        
        result = gs.compute_stats(
            lon, lat, temp, 
            gs.fn2dn(fn),
            threshold = threshold
        )
        out.append(result)  
  

    return pd.concat(out)

def run_months(year):
    
    root = 'GOES/data/nucleos3/'
    
    out = []
    print('Find convections in', year)
    for month in range(1, 13):
        
        ref = dt.datetime(year, month, 1)
        
        path_save = f'{root}{ref.year}{ref.month:02d}/'

        df = run_days(ref)
        
        df.to_csv(path_save) 
        out.append(df)
        
    return pd.concat(out)


def run_all_years(start, end):
    out = []
    
    for year in range(start, end + 1):
        
        out.append(run_months(year)) 
            
    df = pd.concat(out)
    
    df.to_csv('nucleos_2012_2018')
        
 
# main()
year = 2013
df = run_months(year)
path = 'GOES/data/nucleos/'
df.to_csv(f'{path}{year}')

