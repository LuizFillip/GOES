import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def map_attrs(lons, lats, data):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (9, 9),
        subplot_kw = 
            {
            'projection': ccrs.PlateCarree()
            }
        )
    
    gg.map_features(ax)
    
    lat_lim = gg.limits(
        min = -70, 
        max = 40, 
        stp = 10
        )
    lon_lim = gg.limits(
        min = -90, 
        max = -20, 
        stp = 10
        )    
    
    gg.map_boundaries(ax, lon_lim, lat_lim)
    
    gg.mag_equator(
        ax,
        2013,
        degress = None
        )
    
    # data[(data > -40)] = np.nan 
    
    
    ax.contourf(
        lons, 
        lats,
        data, 
        cmap = 'rainbow'
        )
        