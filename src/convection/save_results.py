import datetime as dt 
import GOES  as gs
import pandas as pd 
import base as b 
from tqdm import tqdm 

ref = dt.datetime(2023, 1, 1)
 

# def run_nucleos(ref, B = 'E', threshold = -40):
root = 'GOES/data/nucleos3/'
      
path_year = f'{root}{ref.year}/'

b.make_dir(path_year)

desc = f'Detection - {ref.date()}'

out = []

files = gs.walk_goes(ref, B= 'D')

for fn in tqdm(files, desc):
    
    lon, lat, temp = gs.read_dataset(fn)
    
    result = gs.compute_stats(
        lon, lat, temp, 
        gs.fn2dn(fn),
        threshold = -40
        )
    
    out.append(result)
   
    
df = pd.concat(out)

df.to_csv(f'{path_year}{ref.month}') 

# # return df 
 
    
# run_nucleos(ref, B = 'D', threshold = -40)