import base as b 
import os 
from time import time
import Webscrape as wb 
import datetime as dt 
from tqdm import tqdm 
import pandas as pd 


dn = dt.datetime(2013, 1, 1)


def pURL(str_yr, str_mn):
    
    base = "http://ftp.cptec.inpe.br/goes/goes13/retangular_4km/ch4_bin/"
    
    return f'{base}{str_yr}/{str_mn}/'


def dowloadGOES(dn, B = 'E'):
    
    str_mn = dn.strftime("%m")
    str_yr = dn.strftime("%Y")
    
    root = f'{B}:\\database\\goes\\'
    path_yr = os.path.join(root, str_yr)
    b.make_dir(path_yr)
    path_mn = os.path.join(path_yr, str_mn)
    b.make_dir(path_mn)
    url =  pURL(str_yr, str_mn)
    
    info = f'{str_mn}-{str_yr}'
    
    for href in tqdm(wb.request(url), info):
        
        if href.endswith('gz'):
            
            wb.download(
                url, 
                href, 
                path_mn
                )
            
    return None 

s = time()

dates = pd.date_range(
    dt.datetime(2013, 1, 1),
    dt.datetime(2017, 12, 31), 
    freq = '1M'
    )

for dn in dates:
    dowloadGOES(dn, B = 'E')


e = time()

print((e - s)/ 3600, 'hours')