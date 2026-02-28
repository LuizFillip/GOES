import os 
import datetime as dt

 

def walk_goes(dn, B = 'E'):
    
    mn = dn.strftime("%m")
    yr = dn.strftime("%Y")
    
    path =  f'{B}:\\database\\goes\\{yr}\\{mn}\\'
    
    return [os.path.join(path, f) for f in os.listdir(path)]

def fn2dn(fn):
    fmt = '%Y%m%d%H%M'
    date_string = fn.split('_')[1][:-3]
    return dt.datetime.strptime(date_string, fmt)


dn = dt.datetime(2012, 1, 2, 3)

def get_path_by_dn(dn):
    files = walk_goes(dn, B = 'D')
    
    return [f for f in files if fn2dn(f) == dn][0]