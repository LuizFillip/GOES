# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 14:09:09 2026

@author: Luiz
"""

dn = dt.datetime(2020, 1, 1, 1, 1)
folder = dn.strftime('%Y\\%m\\S10635346_%Y%m%d%H%M.nc')
fname = f'D:\\database\\goes\\{folder}'

fname = "D:\\database\\goes\\2020\\01\\S10635346_202001010000.nc"

ds = gs.CloudyTemperature(fname)

dat, lon, lat = ds.data, ds.lon, ds.lat

df_temp  = pd.DataFrame(dat, columns = lon, index = lat)

df_temp.to_csv('GOES/data/test')