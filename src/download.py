import pandas as pd
import os 
from time import time
import Webscrape as wb 
import datetime as dt 
import GOES as gs


dn = dt.datetime(2013, 1, 1)
str_mn = dn.strftime("%m")
str_yr = dn.strftime("%Y")

def pURL(str_yr, str_mn):
    
    base = "http://ftp.cptec.inpe.br/goes/goes13/retangular_4km/ch4_bin/"
    
    return f'{base}{str_yr}/{str_mn}/'

path_to_save = 'E:\\database\\goes\\'

out_mean = []
out_sum = []

url =  pURL(str_yr, str_mn)

s = time()
for href in wb.request(url):
    
    if href.endswith('gz'):
        
        print('downloading', href)
        
        wb.download(
            url, 
            href, 
            path_to_save
            )
        
        fname = os.path.join(
            path_to_save, href
            )
        dn = gs.fname2date(fname)
        
        print('processing', dn)

        df_mean, df_sum = gs.get_mean_sum(
           gs.binary_to_dataset(fname), dn)
        
        out_mean.append(df_mean)
        out_sum.append(df_sum)
        
ds1 = pd.concat(out_sum)
ds = pd.concat(out_mean)

ds.to_csv('mean_convect')
ds1.to_csv('sum_convect')

e = time()

print((e - s) / 3600)