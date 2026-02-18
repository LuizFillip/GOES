import os 
import datetime as dt

def walk_goes(dn, B = 'E'):
    
    mn = dn.strftime("%m")
    yr = dn.strftime("%Y")
    
    path =  f'{B}:\\database\\goes\\{yr}\\{mn}\\'
    
    return [os.path.join(path, f) for f in os.listdir(path)]

def fn2dn(fn):
    fmt = '%Y%m%d%H%M.nc'
    date_string = fn.split('_')[1]
    return dt.datetime.strptime(date_string, fmt)