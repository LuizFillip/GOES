import numpy as np 

def extract_convection_region(
        ax, lon, lat, temp, 
        x0, x1, y0, y1,
        threshold=-40, cmap=None, levels=None):
    x0, x1 = sorted([x0, x1])
    y0, y1 = sorted([y0, y1])

    lon_mask = (lon >= x0) & (lon <= x1)
    lat_mask = (lat >= y0) & (lat <= y1)

    lon_idx = np.where(lon_mask)[0]
    lat_idx = np.where(lat_mask)[0]

    if lon_idx.size == 0 or lat_idx.size == 0:
        return  # nada para plotar

    sub_lon = lon[lon_idx]
    sub_lat = lat[lat_idx]
    sub_temp = temp[np.ix_(lat_idx, lon_idx)]

    sub_temp = np.where(sub_temp > threshold, np.nan, sub_temp)

    return sub_lon, sub_lat, sub_temp
