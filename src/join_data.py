import os 
import pandas as pd 
import base as b 
from tqdm import tqdm 

def join_data():
    
    for year in range(2018, 2023, 1):
    
        infile = f'GOES/data/{year}/'
        
        out = []
        io = f'{year}'
        
        for file in tqdm(os.listdir(infile), io):
            
            out.append(b.load(infile + file))
            
        df = pd.concat(out)
        
        df.to_csv(f'GOES/data/nucleos/{year}')