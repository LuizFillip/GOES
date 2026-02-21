import datetime as dt 
import GOES  as gs
import pandas as pd 
 
from tqdm import tqdm 


def run_days(ref):
    desc = f'Detection - {ref.date()}'
    files = gs.walk_goes(ref, B= 'D')
    
    out = []
    
    for fn in tqdm(files, desc):
        
        try:
            lon, lat, temp = gs.read_gzbin(fn)
            
            result = gs.compute_stats(
                lon, lat, temp, 
                gs.fn2dn(fn),
                threshold = -40
            )
        except:
            print(fn)
            continue

    out.append(result)  

    return pd.concat(out)

def run_months(year):
    
    root = 'GOES/data/nucleos3/'
    
    out = []

    for month in range(1, 13):
        
        ref = dt.datetime(year, month, 1)
        
        path_save = f'{root}{ref.year}{ref.month:02d}/'

        df = run_days(ref)
        
        df.to_csv(path_save) 
        out.append(df)
        
    return pd.concat(out)


def main():
    out = []
    
    for year in range(2012, 2018):
        
        out.append(run_months(year)) 
            
    df = pd.concat(out)
    
    df.to_csv('nucleos_2012_2018')
        
 
# main()