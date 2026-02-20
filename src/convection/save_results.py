import datetime as dt 
import GOES  as gs
import pandas as pd 
import base as b 
from tqdm import tqdm 

ref = dt.datetime(2023, 1, 1)

def join_data(year):
    root_save = 'GOES/data/'
    path_to_save = f'{root_save}/nucleos2'
    b.make_dir(path_to_save )
    infile = f'{root_save}/{year}/'
    
    out = []
    io = 'Joining'
    
    for file in tqdm(os.listdir(infile), io):
        
        out.append(b.load(infile + file))
        
    df = pd.concat(out)
    
    df.to_csv(f'{path_to_save}/{year}')
        
    return None 
 

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