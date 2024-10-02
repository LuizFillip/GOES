import gzip
import numpy as np
import base as b
import pandas as pd 
import GEO as gg 
import datetime as dt 
import matplotlib.pyplot as plt 
import GOES 
from matplotlib import cm
import cartopy.crs as ccrs

b.config_labels()


def mapping_plot(data, dlon, dlat, ax = None):

    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
    
   
    path = 'GOES/src/IR4AVHRR6.cpt'
    
    cmap = cm.colors.LinearSegmentedColormap(
        'cpt', GOES.loadCPT(path)) 
    
    if ax is None:
    
        fig, ax = plt.subplots(
                 figsize = (12, 12), 
                 dpi = 300, 
                 subplot_kw = 
                 {'projection': ccrs.PlateCarree()}
                 )
    
    gg.map_attrs(
        ax, 2013, 
        lat_lims  = lat_lims, 
        lon_lims = lon_lims,
        grid = False,
        degress = None
        )
    
    
    ax.contourf(dlon, dlat, data, 50, cmap = cmap)
    
    # plt.colorbar(img)
    
    return ax
    
# fig, ax = plt.subplots(
#           figsize = (12, 12), 
#           dpi = 300, 
#           subplot_kw = 
#           {'projection': ccrs.PlateCarree()}
#           )
    # mapping_plot(data, dlon, dlat, ax = ax)
 # table = pd.pivot_table(
 #     ds, 
 #     columns = ns[0], 
 #     index = ns[1], 
 #     values = ns[2]
 #     )
 # dlon = table.columns
 # dlat = table.index
        
        
def read_gzbin(f_name):
 
    with gzip.open(f_name, 'rb') as f:
        
        dados_binarios = np.frombuffer(
            f.read(), 
            dtype = np.int16
            )

        image_size = [1714, 1870]
        # image_size = [1200, 1335]
        data_bin = dados_binarios.reshape(image_size)
    
        return data_bin / 100 - 273.13


def fname2date(fname):
    dn = fname.split('_')[-1][:-3]
    return dt.datetime.strptime(dn, '%Y%m%d%H%M')




fname = 'GOES/data/S10236964_201301010000.gz'
fname = 'GOES/data/S11232404_201312010800.gz'
fname = 'GOES/data/S10236964_201306020530.gz'

def structured_data(nlons, nlats, grid):
    x, y = np.meshgrid(nlons, nlats)
    
    x = x.reshape(-1)
    y = y.reshape(-1)
    grid_means = grid.reshape(-1)
    
    return np.column_stack((x, y, grid_means))

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

def binary_to_dataset(fname):
    data = read_gzbin(fname)
    
    dlon = np.arange(data.shape[1]) * 0.04 - 100
    dlat = np.arange(data.shape[0]) * 0.04 - 50
        
    ns = ['lon', 'lat', 'temp']
    
    return pd.DataFrame(
        structured_data(dlon, dlat, data), 
        columns = ns
        )

def get_mean_sum(df, dn):
    
    out_mean = {}
    out_sum = {}
    for sector in np.arange(-80, -40, 10):
        
        ds = filter_region(df, dn.year, sector)
 
        data = ds['temp'].values
     
        out_sum[sector] = np.nansum(data)
        out_mean[sector] = np.nanmean(data)
    
    df_mean = pd.DataFrame(out_mean, index = [dn])
    df_sum = pd.DataFrame(out_sum, index = [dn])

    return df_mean, df_sum


import os 
from time import time
import Webscrape as wb 

dn = dt.datetime(2013, 1, 1)
str_mon = dn.strftime("%m")
str_yer = dn.strftime("%Y")

url = f"http://ftp.cptec.inpe.br/goes/goes13/retangular_4km/ch4_bin/{str_yer}/{str_mon}/"

path_to_save = 'E:\\database\\goes\\'

out_mean = []
out_sum = []

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
        dn = fname2date(fname)
        
        print('processing', dn)

        df_mean, df_sum = get_mean_sum(
           binary_to_dataset(fname), dn)
        
        out_mean.append(df_mean)
        out_sum.append(df_sum)
        
ds1 = pd.concat(out_sum)
ds = pd.concat(out_mean)

ds.to_csv('mean_convect')
ds1.to_csv('sum_convect')

e = time()

print((e - s) / 3600)