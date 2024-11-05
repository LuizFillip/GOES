import GOES  as gs
from matplotlib import cm
import cartopy.crs as ccrs
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 
import GEO as gg 


def goes_cmap(path = 'GOES/src/colorbar.cpt'):
    cpt = gs.loadCPT(path)
    return cm.colors.LinearSegmentedColormap('cpt', cpt) 


class plotTopCloud(object):
    
    b.config_labels()

    def __init__(
            self, 
            data, 
            lons, 
            lats, 
            fig = None, 
            figsize = (12, 10)
            ):
        
        self.data = data 
        self.lons = lons
        self.lats = lats 
        
        if (fig is None):
            self.fig, self.ax = plt.subplots(
                dpi = 300, 
                figsize = figsize, 
                subplot_kw = 
                {'projection': ccrs.PlateCarree()}
                )
            
    def contour(self, ax):
        
        img = ax.imshow(
            self.data,
            aspect = 'auto', 
            extent = [self.lons[0], self.lons[-1], 
                      self.lats[0], self.lats[-1]],
            cmap = goes_cmap(), 
            vmin = -100, 
            vmax = 100
            )
        
        return img 
    
    @property 
    def figure_axes(self):
        return self.fig, self.ax 
    
    def colorbar(
            self, 
            img, ax,
            orientation = "vertical", 
            step = 20
            ):

        ticks = np.arange(-100, 100 + step, step)
        
        if orientation == 'horizontal':
            height = '10%' 
            width = "80%", 
            anchor = (-0.26, 0.7, 1.26, 0.55) 
        else:
            height = "100%"
            width = "5%"
            anchor = (.1, 0., 1, 1)
            
        b.colorbar(
               img, 
               ax, 
               ticks, 
               label = 'Temperature (°C)', 
               height = height, 
               width = width,
               orientation = orientation, 
               anchor = anchor
               )
        
    def reference_line(self, lon = None, lat = None):
        
        if lon is None:
            self.ax.axhline(lat, color = 'w', lw = 3)
        if lat is None:
            self.ax.axvline(lon, color = 'w', lw = 3)
            
        return None 
    
    def add_map(self, ax):
       
      
        lat_lims = dict(min = -40, max = 20, stp = 10)
        lon_lims = dict(min = -90, max = -30, stp = 10) 

        gg.map_attrs(
            ax, 2013, 
            lat_lims  = lat_lims, 
            lon_lims = lon_lims,
            grid = False,
            degress = None
            )

    def plot_regions(
            self, 
            x_stt, y_stt, 
            x_end, y_end, 
            number = None
            ):
        
      
        rect = plt.Rectangle(
            (x_stt, y_stt), 
            x_end - x_stt, 
            y_end - y_stt,
            edgecolor = 'k', 
            facecolor = 'none', 
            linewidth = 3
        )
        
        self.ax.add_patch(rect)
        
        if number is not None:
            middle_y = (y_end + y_stt) / 2
            middle_x = (x_end + x_stt) / 2
            
            self.ax.text(
                middle_x, 
                middle_y + 1, number, 
                transform = self.ax.transData
                )
            
        return None 


def test_plot(fname):
    ds = gs.CloudyTemperature(fname)
    
    dat, lon, lat = ds.data[::-1], ds.lon, ds.lat
    dn =  ds.dn
    
    ptc = gs.plotTopCloud(dat, lon, lat)
    
    ptc.add_map()
    ptc.colorbar()
    
    fig, ax = ptc.figure_axes 
    
    ax.set(title = dn)
    
    ds =  gs.find_nucleos(
              dat, 
              lon, 
              lat[::-1],
              dn 
             
              )
    for index, row in ds.iterrows():
        
        ptc.plot_regions(
            row['x0'], 
            row['y0'],
            row['x1'], 
            row['y1'], 
            # i = indexs
            )
        
    return fig 

