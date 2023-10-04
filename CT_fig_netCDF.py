# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:10:27 2023

@author: Hisashi
"""
import os
import shutil
import xarray as xr
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import goes_download as gd

import make_gif as movie

def day_of_year(year, month, day):
    dt = datetime(year, month, day)
    day_of_year = dt.timetuple().tm_yday
    return f'{day_of_year:03d}'

fname=os.path.basename(__file__) #name of the file


FOLDER_BASE = '/media/hisashi/D/Banco_Dados'

year = '2021'
month = '10'
dom = '25'
doy = day_of_year(int(year), int(month), int(dom))

# =============================================================================
gd.download_goes16(int(year), int(month), int(dom))
# =============================================================================



fps=15


# files_dir=f'D:/Drive/CPTEC/{year}/{month}'
files_dir=f'{FOLDER_BASE}/CPTEC/{year}/{month}/{dom}/'

Files_list=os.listdir(files_dir)
Files_list.sort()
plt.ioff()


for i,file in enumerate(Files_list):
    Path_file=os.path.join(files_dir, file)
    
    
    
    data = xr.open_dataset(Path_file)
    temp=data.Band1.values/100 -273.13
    # temp[temp>=-40]=np.nan
    extent=[data['lon'].min(), data['lon'].max(), data['lat'].min(), data['lat'].max()]
    
    
   
    
    date_str = file[-15:-3]
    date_obj = datetime.strptime(date_str, '%Y%m%d%H%M')
    
    
    
    
    plt.rcParams.update({'font.size': 35})
    # plt.ioff()
    fig=plt.figure(figsize=(35,35))
        
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution='110m',color='k')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.STATES)
    # extent=[int(dlon.min()), int(dlon.max()), int(dlat.min()), int(dlat.max())]
    
    # lat_min = -65; lat_max = -40
    # lon_min = -40; lon_max = -20
    
    lat_min = -40; lat_max = -10
    lon_min = -75; lon_max = -35
    
    # extend = [-77,-30,-40,10]
    
    extend = [lon_min,lon_max,lat_min,lat_max]
    
    # extend = [-100,-24,-56,13]
    ax.set_extent(extend, crs=ccrs.PlateCarree())
    
    # ax.text(0.5, 1.05, '[/CPTEC/CT_fig.py]', va='bottom', ha='center',
    #         rotation='horizontal', rotation_mode='anchor',
    #         transform=ax.transAxes)
    
    ax.text(0.5, 1.01, '{} [{}]'.format(date_obj.strftime("%d-%b, %Y %Hh:%Mmin"),fname),
            va='bottom', ha='center',
            rotation='horizontal', rotation_mode='anchor',
            transform=ax.transAxes)
    ax.text(-0.1, 0.55, 'Latitude', va='bottom', ha='center',
            rotation='vertical', rotation_mode='anchor',
            transform=ax.transAxes)
    ax.text(0.5, -0.08, 'Longitude', va='bottom', ha='center',
            rotation='horizontal', rotation_mode='anchor',
            transform=ax.transAxes)
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=2,color='gray', alpha=0.5, linestyle=':')
    
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
    
    
    
    # =============================================================================
    # 
    # =============================================================================
    
    
    
    cmap = plt.cm.BuPu_r  # the original colormap
    cmap = mcolors.ListedColormap(cmap(np.linspace(0.0, 1.0, 10)))
    
    
    im=plt.imshow(temp, extent=extent,origin='lower',cmap=cmap,vmax=-50,vmin=-80)
    
    # contour_levels = [-75, -70, -65]
    # plt.contour(temp, extent=extent, cmap=cmap, levels=contour_levels, linewidths=3)  # Adjust the 'levels' parameter as needed
    
    # plt.clabel(contour, inline=True, fmt='%1.1f', colors='black', fontsize=8)
    cbar=plt.colorbar(shrink=0.62)
    cbar.set_label('Cloud top [ºC]')
    
    
    # plt.show()
    
    # fig_dir='D:/Drive/CPTEC/2023/figs/slice_'
    fig_dir=f'{FOLDER_BASE}/CPTEC/{year}/figs'
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)
    
    fig_name=file.split('/')[-1].split('.')[0].split('_')[-1]
    fig_name=f'/{fig_dir}/{fig_name}.png'
    fig.savefig(fig_name, bbox_inches='tight', dpi=100)
    
    plt.close(fig)
    
    print('Progress: {:.2f} % | {:03d}/{}'.format(100.*(i+1)/len(Files_list),i+1,len(Files_list)))



movie_dir = f'{FOLDER_BASE}/Produtos/{year}/{doy}/movies/'
if not os.path.exists(movie_dir):
    os.makedirs(movie_dir) 
    
movie.make_movie(fig_dir, #Dir of source of images
                 movie_dir, #output dir
                 f'{date_obj.strftime("%Y%j")}_CPTEC_{fps}fps', #outputname
                 fps=fps)

movie_dir = f'/home/hisashi/Dropbox/Python/spyder_home/CPTEC/Storm_Movies/'
if not os.path.exists(movie_dir):
    os.makedirs(movie_dir) 
    
movie.make_movie(fig_dir, #Dir of source of images
                 movie_dir, #output dir
                 f'{date_obj.strftime("%Y%j")}_CPTEC_{fps}fps', #outputname
                 fps=fps)


# Delete the directory
shutil.rmtree(fig_dir)


























