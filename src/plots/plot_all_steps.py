import GOES  as gs 
import datetime as dt 
import matplotlib.pyplot as plt 
import numpy as np 
import cartopy.crs as ccrs
from scipy.ndimage import binary_erosion

def border_points_from_mask(
        temp, lon, lat, 
        threshold, 
        lon_min=None, lon_max=None, 
        lat_min=None, lat_max=None
        ):
    """
    Retorna os pontos de borda (lon, lat) da
    região fria temp <= threshold.
    Pode opcionalmente restringir a um retângulo.
    """

    temp = np.asarray(temp)
    lon = np.asarray(lon, float)
    lat = np.asarray(lat, float)

    # se houver bbox, recorta
    if lon_min is not None:
        lon1, lon2 = sorted([lon_min, lon_max])
        lat1, lat2 = sorted([lat_min, lat_max])

        lon_mask = (lon >= lon1) & (lon <= lon2)
        lat_mask = (lat >= lat1) & (lat <= lat2)

        if not lon_mask.any() or not lat_mask.any():
            return np.array([]), np.array([])

        temp = temp[np.ix_(lat_mask, lon_mask)]
        lon = lon[lon_mask]
        lat = lat[lat_mask]

    # máscara fria
    mask = np.isfinite(temp) & (temp <= threshold)

    if not np.any(mask):
        return np.array([]), np.array([])

    # borda = máscara original menos interior erodido
    interior = binary_erosion(mask)
    border = mask & ~interior

    # grade 2D
    lon2d, lat2d = np.meshgrid(lon, lat)

    return lon2d[border], lat2d[border]

def plot_semi_axis(ax, e):
    xc_e, yc_e = e.center
    w_e = e.width
    h_e = e.height
    ang_e = e.angle
    
    theta = np.deg2rad(ang_e)
    
    a = h_e / 2
    b = w_e / 2
    
    # eixo maior
    x_major = [xc_e - a*np.sin(theta),
               xc_e + a*np.sin(theta)]
    y_major = [yc_e + a*np.cos(theta),
               yc_e - a*np.cos(theta)]
    
    # eixo menor
    x_minor = [xc_e - b*np.cos(theta), 
               xc_e + b*np.cos(theta)]
    y_minor = [yc_e - b*np.sin(theta), 
               yc_e + b*np.sin(theta)]
    
    ax.plot(x_major, y_major, 'k-', transform=ccrs.PlateCarree())
    ax.plot(x_minor, y_minor, 'k-', transform=ccrs.PlateCarree())

def angle_from_rectangle(lon_min, lon_max, lat_min, lat_max, descending=True):
    rect_width = lon_max - lon_min
    rect_height = lat_max - lat_min

    ang = np.degrees(np.arctan2(rect_height, rect_width))
    return -ang if descending else ang

def whole_map(ax, nl):
    gs.plot_cloud_top_temperature(
        lon, lat, temp, ax = ax,
        add_colorbar=False, 
        cbar_ticks=None,
    )
    for _, row in nl.iterrows():
          gs.plot_rectangle(
            ax,
            row["lon_min"], row["lon_max"],
            row["lat_min"], row["lat_max"],
            dot_size = 10
        )
 
def contour_from_threshold(
        temp, lon, lat, threshold,
        lon_min=None, lon_max=None,
        lat_min=None, lat_max=None
        ):
    """
    Retorna segmentos do contorno da máscara temp <= threshold.
    """
    temp = np.asarray(temp)
    lon = np.asarray(lon, float)
    lat = np.asarray(lat, float)

    if lon_min is not None:
        lon1, lon2 = sorted([lon_min, lon_max])
        lat1, lat2 = sorted([lat_min, lat_max])

        lon_mask = (lon >= lon1) & (lon <= lon2)
        lat_mask = (lat >= lat1) & (lat <= lat2)

        if not lon_mask.any() or not lat_mask.any():
            return []

        temp = temp[np.ix_(lat_mask, lon_mask)]
        lon = lon[lon_mask]
        lat = lat[lat_mask]

    lon2d, lat2d = np.meshgrid(lon, lat)
    mask = np.isfinite(temp) & (temp <= threshold)

    if not np.any(mask):
        return []

    fig, ax_tmp = plt.subplots()
    cs = ax_tmp.contour(
        lon2d, lat2d, mask.astype(float), levels=[0.5])
    plt.close(fig)

    segments = []
    for seglist in cs.allsegs[0]:
        segments.append(seglist)   # cada seglist é array Nx2: [lon, lat]

    return segments

class limits:
    
    def __init__(self, row, step = 5):
    
        self.lon0, self.lon1 = row["lon_min"], row["lon_max"]
        self.lat0, self.lat1 = row["lat_min"], row["lat_max"]
    
    
        self.lat_min = round(self.lat0) - step
        self.lat_max = round(self.lat1) + step 
        self.lon_min = round(self.lon0) - step
        self.lon_max = round(self.lon1) + step 
        
        self.step = step


def plot_areas_with_temp_removed(
        ax, l, 
        sub_lon, 
        sub_lat, 
        sub, 
        segments
        ):
    
    gs.plot_cloud_top_temperature(
        sub_lon, sub_lat, sub, 
        ax = ax,
        lat_min = l.lat_min, 
        lat_max = l.lat_max,
        lon_min = l.lon_min, 
        lon_max = l.lon_max,
        lon_step = l.step, 
        lat_step = l.step,
        add_colorbar = False, 
        cbar_ticks = None,
    )
    
    gs.plot_rectangle(
        ax,
        l.lon0, l.lon1,
        l.lat0, l.lat1,
    )
      
    for seg in segments:
        ax.scatter(
            seg[:, 0], 
            seg[:, 1], 
            s = 3, 
            c = 'magenta',
            transform = ccrs.PlateCarree(),
            zorder = 6
            )
    
def remove_lower_temperatures(l, threshold = -40 ):
    
    lon_mask = (lon >= l.lon0) & (lon <= l.lon1)
    lat_mask = (lat >= l.lat0) & (lat <= l.lat1)
 
    sub = temp[np.ix_(lat_mask, lon_mask)]
    sub_lat = lat[lat_mask]
    sub_lon = lon[lon_mask]
             
    sub[sub > threshold] = np.nan
 
    segments = contour_from_threshold(
        sub, sub_lon, sub_lat,
        threshold= threshold,
        lat_min = l.lat_min, 
        lat_max = l.lat_max,
        lon_min = l.lon_min, 
        lon_max = l.lon_max,
        )

    
    return sub_lon, sub_lat, sub, segments

def section_plot(lon, lat, temp, threshold = -50):
    
    fig, ax = plt.subplots(
        ncols = 3,
        dpi = 300, 
        figsize = (16, 12),
        subplot_kw = {"projection": ccrs.PlateCarree()}
        )
    
    nl = gs.find_nucleos(
         lon,
         lat,
         temp,
         dn=None,
         temp_threshold= threshold,
     )
    
    whole_map(ax[0], nl)
  
    row = nl.iloc[44] # case um
 
    l = limits(row)
 
    gs.plot_cloud_top_temperature(
        lon, lat, temp, 
        ax = ax[1],
        lat_min = l.lat_min, lat_max = l.lat_max,
        lon_min = l.lon_min, lon_max = l.lon_max,
        lon_step = l.step, 
        lat_step = l.step,
        add_colorbar = False, 
        cbar_ticks = None,
    )
    
     
    gs.plot_rectangle(
        ax[1],
        l.lon0, l.lon1,
        l.lat0, l.lat1,
    )
    
    
    
    sub_lon, sub_lat, sub, segments =  remove_lower_temperatures(
        l, threshold)
  
    
    plot_areas_with_temp_removed(
           ax[-1], l, sub_lon, sub_lat, sub, segments)
    
    


threshold = -40

dn = dt.datetime(2013, 1, 29, 1, 0)
dn = dt.datetime(2013, 1, 1, 0, 0)

fn = gs.get_path_by_dn(dn)
lon, lat, temp = gs.read_gzbin(fn)


section_plot(lon, lat, temp, threshold = -40)

# nl = gs.find_nucleos(
#      lon,
#      lat,
#      temp,
#      dn=None,
#      temp_threshold= threshold,
#  )
  
# row = nl.iloc[44] # case um




