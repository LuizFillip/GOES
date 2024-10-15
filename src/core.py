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
from tqdm import tqdm 
import os 
from scipy.ndimage import label, find_objects

b.config_labels()


def goes_cmap():
    
    path = 'GOES/src/colorbar.cpt'
    
    return cm.colors.LinearSegmentedColormap(
        'cpt', GOES.loadCPT(path)) 


def mapping_plot(data, lons, lats, ax = None, ref_lon = None):

    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 10) 

    if ax is None:
    
        fig, ax = plt.subplots(
                 figsize = (12, 12), 
                 dpi = 300, 
                 # subplot_kw = 
                 # {'projection': ccrs.PlateCarree()}
                 )
    
    # gg.map_attrs(
    #     ax, 2013, 
    #     lat_lims  = lat_lims, 
    #     lon_lims = lon_lims,
    #     grid = False,
    #     degress = None
    #     )
    
    
    # img = ax.contourf(dlon, dlat, data, 30, cmap = goes_cmap())
    img = ax.imshow(
        data, 
        aspect = 'auto',
        # extent = [lons[0], lons[-1], lats[0], lats[-1]],
        cmap = goes_cmap()
        )
    ticks = np.arange(np.nanmin(data), np.max(data), 20)
    
    b.colorbar(
           img, 
           ax, 
           ticks, 
           label = 'Temperature (°C)', 
           height = "100%", 
           width = "10%",
           orientation = "vertical", 
           anchor = (.25, 0., 1, 1)
           )
    if ref_lon is not None:
        ax.axvline(ref_lon, color = 'w', lw = 3)
    return fig, ax
    
    
        
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


def structured_data(nlons, nlats, grid):
    x, y = np.meshgrid(nlons, nlats)
    
    x = x.reshape(-1)
    y = y.reshape(-1)
    grid_means = grid.reshape(-1)
    
    return np.column_stack((x, y, grid_means))



class CloudyTemperature(object):
    
    def __init__(self, fname):
        self.fname = fname
        self.data = read_gzbin(fname)
        shape = self.data.shape
        self.lon = np.arange(shape[1]) * 0.04 - 100
        self.lat = np.arange(shape[0]) * 0.04 - 50
    
        
    @property
    def to_dataset(self):
        data = structured_data(self.lon, self.lat, self.data)
        ds = pd.DataFrame(
            data, 
            columns = ['lon', 'lat', 'temp']
            )
        
        ds['time'] = fname2date(self.fname)
        
        return ds 
    
    @property
    def to_pivot(self):
        ds = self.to_dataset()
        return pd.pivot_table(
            ds, 
            columns = 'lon', 
            index = 'lat', 
            values = 'temp'
            )
    


   


def load_files(ref_day):
    path = 'E:\\database\\goes\\'

    files = os.listdir(path)
    
    return [os.path.join(path, f) for f in files 
            if fname2date(f) < ref_day]

def CloudTopKeogram(fname, lon = -55):
    out = []
    
    for file in tqdm(files, 'MakeKEO'):

        CT = CloudyTemperature(fname)
        
        ds = CT.to_dataset()
        out.append(ds.loc[ds['lon'] == lon])
     
    ds = pd.concat(out)
    
    # # fig = plot_keogram(ds1, ax = None)
    # time = ds1.columns
    # time = [b.dn2float(t, sum_from = None) for t in time]
    # lats = ds1.index
    # data = ds1.values[::-1]
    return pd.pivot_table(
        ds, 
        values = 'temp', 
        columns = 'time', 
        index = 'lat'
        )






def plot_colobar(ticks, img, ax):

    

    b.colorbar(
            img, 
            ax, 
            ticks, 
            label = 'Temperature (°C)', 
            height = "100%", 
            width = "5%",
            orientation = "vertical", 
            anchor = (0.1, 0., 1, 1)
            )
    
    b.colorbar(
            img, 
            ax, 
            ticks, 
            label = 'Temperature (°C)', 
            height = '10%' , 
            width = "80%",
            orientation = "horizontal", 
            anchor = (-0.26, 0.7, 1.26, 0.55)
            )
    
    return 


def find_nucleos(
        data, 
        lons, 
        lats,
        ax = None,
        area_treshold = 40,
        step = 0.5, 
        by_indexes = True
        ):
        
    labeled_array, num_features = label(~np.isnan(data))
        
    ymax, xmax = data.shape
    
    for i, region in enumerate(find_objects(labeled_array)):
       
        x_stt, x_end = region[1].start, region[1].stop
        y_stt, y_end = region[0].start, region[0].stop
        
        
        area = (y_end - y_stt) * (x_end - x_stt)
        
        if area > area_treshold:
            
            if by_indexes:
                if (x_end == xmax):
                    x_end = -1
                if (y_end == ymax):
                    y_end = -1
                
                x_stt, x_end = lons[x_stt], lons[x_end]
                y_stt, y_end = lats[y_stt], lats[y_end] 
            
            if ax is not None:
                rect = plt.Rectangle(
                    (x_stt, y_stt), 
                    x_end - x_stt, 
                    y_end - y_stt,
                    edgecolor = 'red', 
                    facecolor = 'none', 
                    linewidth = 2 
                    )
            
                ax.add_patch(rect)
                # middle_y = (y_end + y_stt) / 2
                # middle_x = (x_end + x_stt) / 2
                # ax.text(
                #     middle_x, 
                #     middle_y + 1, i, 
                #     transform = ax.transData
                #     )
    return
        
ref_day = dt.datetime(2013, 1, 2)
files = load_files(ref_day)

fname = files[0]
ds = CloudyTemperature(fname)
data = ds.data[::-1]
lons = ds.lon 
lats = ds.lat


fig, ax = plt.subplots(
    dpi = 300, 
    figsize = (16, 12)
    )


img = ax.imshow(
    data,
    aspect = 'auto', 
    extent = [lons[0], lons[-1], lats[0], lats[-1]],
    cmap = goes_cmap()
    
    )

ticks = np.arange(np.nanmin(data), np.max(data), 20)
b.colorbar(
       img, 
       ax, 
       ticks, 
       label = 'Temperature (°C)', 
       height = "100%", 
       width = "5%",
       orientation = "vertical", 
       anchor = (.1, 0., 1, 1)
       )
data = np.where(data > -40, np.nan, data)

find_nucleos(
        data, 
        lons, 
        lats[::-1],
        ax,
        area_treshold = 60,
        step = 0.5
        )

