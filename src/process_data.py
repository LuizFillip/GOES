import pandas as pd 
import datetime as dt 
import GOES as gs 
from time import time 
import os 

def woon_dowload(year = 2013):
    s = time()
    
    dates = pd.date_range(
        dt.datetime(year, 1, 1),
        dt.datetime(year, 2, 1), 
        freq = '1M'
        )
    
    for dn in dates:
        print('Download')
        gs.dowloadGOES(dn, B = 'E')
        print('Get_nucleos')
        gs.run_nucleos(dn, b = 'E')
    
    e = time()
    
    print((e - s)/ 3600, 'hours')
    
woon_dowload(year = 2013)