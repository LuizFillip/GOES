import pandas as pd 
import datetime as dt 
import GOES as gs 
from time import time 
import os 
import base as b 
from tqdm import tqdm 

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

def woon_dowload(
        year = 2013, 
        start = 6,
        B = 'E', 
        delete = False
        ):
    
    s = time()
    
    dates = pd.date_range(
        dt.datetime(year, start, 1),
        dt.datetime(year, 12, 31), 
        freq = '1M'
        )
    
    for dn in dates:
        print('Starting', dn.strftime('%Y-%m'))
        path = gs.dowloadGOES(dn, B)
        gs.run_nucleos(dn, B)
        
        if delete:
            os.remove(path)
    
    join_data(year)
    
    e = time()
    
    print((e - s)/ 3600, 'hours')
    
    return None 
    
# woon_dowload(year = 2018, start = 9)
