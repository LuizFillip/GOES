import base as b 
import os 
from time import time
import Webscrape as wb 
import datetime as dt 
from tqdm import tqdm 
import pandas as pd 


def goesURL(str_yr, str_mn):
    
    year = int(str_yr)
    
    base = "http://ftp.cptec.inpe.br/goes/"
    
    if year < 2018:
        base += 'goes13/retangular_4km/ch4_bin/'
    else:
        base += 'goes16/retangular/ch13/'
        
        
    return f'{base}{str_yr}/{str_mn}/'

def dowloadGOES(dn,  B = 'E'):
    
    str_mn = dn.strftime("%m")
    str_yr = dn.strftime("%Y")
    
    root = f'{B}:\\database\\goes\\'
    path_yr = os.path.join(root, str_yr)
    b.make_dir(path_yr)
    path_mn = os.path.join(path_yr, str_mn)
    b.make_dir(path_mn)
    url = goesURL(str_yr, str_mn)
    
    info = f'{str_mn}-{str_yr}'
    out = []
    
    files = os.listdir(path_mn)
    for href in tqdm(wb.request(url), info):
        
        if href.endswith('gz') or href.endswith('nc'):
            
            if href not in files:
                out.append(href)
                
                wb.download(
                    url, 
                    href, 
                    path_mn
                    )
            else:
                print(href, 'done')
            
   
    return None 

def woon_dowload():
    s = time()
    
    dates = pd.date_range(
        dt.datetime(2021, 9, 1),
        dt.datetime(2022, 12, 31), 
        freq = '1M'
        )
    
    for dn in dates:
        dowloadGOES(dn, B = 'D')
    
    e = time()
    
    print((e - s)/ 3600, 'hours')
    
    
woon_dowload()

# dn = dt.datetime(2020, 11, 1)


