import GOES  as gs 
import datetime as dt 
import matplotlib.pyplot as plt 
import numpy as np 
import cartopy.crs as ccrs
from scipy.ndimage import binary_erosion
import base as b 


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



def whole_map(
        ax, nl, 
        lon, lat, temp, 
        add_colorbar = True
        ):
    
    gs.plot_cloud_top_temperature(
        lon, lat, temp,
        ax = ax,
        add_colorbar = add_colorbar, 
        cbar_ticks = None,
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
        ax, lon, lat, temp, l, threshold
        ):
    
    sub_lon, sub_lat, sub, segments =  remove_lower_temperatures(
        lon, lat, temp, l, threshold)

    
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
    
    return None 
    
def remove_lower_temperatures(lon, lat, temp, l, threshold = -40 ):
    
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
  
    
    
    

def plot_whole_map_with_steps(dn, num = 44, threshold = -40):
    
    fn = gs.get_path_by_dn(dn)
    lon, lat, temp = gs.read_gzbin(fn)
    
     
    nl = gs.find_nucleos(
          lon,
          lat,
          temp,
          dn=None,
          temp_threshold= threshold,
      )
     
    fig, ax = plt.subplots(
         ncols = 2,
         nrows = 2,
         dpi = 300, 
         figsize = (14, 14),
         subplot_kw = {"projection": ccrs.PlateCarree()}
         )
    
    plt.subplots_adjust(hspace = 0.1)
    gs.plot_vir_image(ax[0, 0], dn)
    whole_map(ax[0, 1], nl, lon, lat, temp, add_colorbar = False)
    
    
    row = nl.iloc[num] # case um
    
    l = limits(row)
    
    _, _, m, _ = gs.plot_cloud_top_temperature(
        lon, lat, temp, 
        ax = ax[1, 0],
        lat_min = l.lat_min, lat_max = l.lat_max,
        lon_min = l.lon_min, lon_max = l.lon_max,
        lon_step = l.step, 
        lat_step = l.step,
        add_colorbar = False, 
        cbar_ticks = None,
    )
    
     
    gs.plot_rectangle(
        ax[1, 0],
        l.lon0, l.lon1,
        l.lat0, l.lat1,
    )
    
    plot_areas_with_temp_removed(ax[1, 1], lon, lat, temp, l, threshold)
    
    
    b.plot_letters(
            ax, 
            x = 0.02, 
            y = 0.85, 
            offset = 0, 
            fontsize = 35,
            num2white = 0
            )
     
    ticks = np.arange(-100, 100, 20)
    
    cax = ax[0, 0].inset_axes([0.35, 1.25, 1.5, 0.07])
    
    cb = plt.colorbar(
        m, 
        orientation = 'horizontal',
        cax = cax,
        ticks = ticks 
        )
     
    cb.set_label('Temperature (°C)')
    
    fig.suptitle(dn.strftime('%d %B %Y %H:%M UT'), y = 1.)
    return fig
    
  
    
dn = dt.datetime(2013, 1, 29, 1, 0)
dn = dt.datetime(2013, 1, 1, 0, 0)

fig = plot_whole_map_with_steps(dn, num = 44, threshold = -40)

path_to_save = 'G:\\Meu Drive\\Papers\\Convective_analysis\\'

figname = 'vir_and_top_cloud'
fig.savefig(path_to_save + figname, dpi = 400)