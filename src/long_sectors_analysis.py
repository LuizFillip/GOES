import base as b 
import numpy as np 
import pandas as pd
import GEO as gg


def filter_region(df, year, sector):
    '''filter region'''
    corners = gg.set_coords(year)

    xlim, ylim = corners[sector]
    
    return df.loc[
        (df.lon > xlim[0]) & 
        (df.lon < xlim[1]) & 
        (df.lat > ylim[0]) & 
        (df.lat < ylim[1])
        ]



def get_mean_sum(df, dn):
    
    out_mean = {}
    
    for sector in np.arange(-80, -40, 10):
        
        ds = filter_region(df, dn.year, sector)
 
        data = ds['temp'].values
     
        out_mean[sector] = np.nanmean(data)

    return pd.DataFrame(out_mean, index = [dn])


import base as b 

df = b.load('test_goes')

df = df.loc[df['area'] > 10]
# df = df.between_time('22:00', '06:00')
# ds = df.resample('1H').count()

# ds['area'].plot(figsize = (12, 6))

df