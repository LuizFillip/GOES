import numpy as np
import GOES  as gs
 
R = 6371.0  # km

def area_mask_km2(data, lats, lons, temp_threshold):
    data = np.asarray(data)
    lats = np.asarray(lats, float)
    lons = np.asarray(lons, float)

    # garante lat crescente e data alinhado
    if lats[0] > lats[-1]:
        lats = lats[::-1]
        data = data[::-1, :]

    mask = np.isfinite(data) & (data <= temp_threshold)  # pixels "coloridos"

    # bordas dos pixels (assumindo grid quase regular)
    dlat = np.abs(np.median(np.diff(lats)))
    dlon = np.abs(np.median(np.diff(lons)))

    # área por linha de latitude (varia com cos(lat))
    lat_rad = np.deg2rad(lats)
    dlat_rad = np.deg2rad(dlat)
    dlon_rad = np.deg2rad(dlon)

    # área de 1 pixel na latitude i (km²)
    pixel_area_by_lat = (R**2) * dlat_rad * dlon_rad * np.cos(lat_rad)  # (ny,)

    # soma área onde mask é True
    area_km2 = np.sum(mask * pixel_area_by_lat[:, None])
    return float(area_km2)

def cold_area_in_bbox_km2(
        temp, lon, lat, threshold, lon_min, lon_max, lat_min, lat_max, R=6371.0):
    lon1, lon2 = sorted([lon_min, lon_max])
    lat1, lat2 = sorted([lat_min, lat_max])

    lon = np.asarray(lon, float)
    lat = np.asarray(lat, float)
    temp = np.asarray(temp)

    # indices do recorte
    lon_mask = (lon >= lon1) & (lon <= lon2)
    lat_mask = (lat >= lat1) & (lat <= lat2)
    if not lon_mask.any() or not lat_mask.any():
        return np.nan

    sub = temp[np.ix_(lat_mask, lon_mask)]
    sub_lat = lat[lat_mask]
    sub_lon = lon[lon_mask]

    # máscara fria
    mask = np.isfinite(sub) & (sub <= threshold)

    # resolução (assumindo quase regular)
    dlat = np.abs(
        np.median(np.diff(sub_lat))
        ) if len(sub_lat) > 1 else np.abs(np.median(np.diff(lat)))
    dlon = np.abs(
        np.median(np.diff(sub_lon))) if len(sub_lon) > 1 else np.abs(np.median(np.diff(lon)))

    dlat_rad = np.deg2rad(dlat)
    dlon_rad = np.deg2rad(dlon)
    lat_rad = np.deg2rad(sub_lat)

    # área por linha de latitude
    pixel_area_by_lat = (R**2) * dlat_rad * dlon_rad * np.cos(lat_rad)  # (ny_sub,)
    return float(np.sum(mask * pixel_area_by_lat[:, None]))

def cold_stats_in_bbox(
        temp, lon, lat, 
        threshold,
        lon_min, lon_max, lat_min, lat_max):
    
    lon1, lon2 = sorted([lon_min, lon_max])
    lat1, lat2 = sorted([lat_min, lat_max])

    lon = np.asarray(lon, float)
    lat = np.asarray(lat, float)
    temp = np.asarray(temp)

    lon_mask = (lon >= lon1) & (lon <= lon2)
    lat_mask = (lat >= lat1) & (lat <= lat2)

    if not lon_mask.any() or not lat_mask.any():
        return np.nan, np.nan

    sub = temp[np.ix_(lat_mask, lon_mask)]

    # máscara fria
    cold = sub <= threshold
    sub = np.where(cold, sub, np.nan)

    if np.all(np.isnan(sub)):
        return np.nan, np.nan

    mean_temp = np.nanmean(sub)
    max_temp  = np.nanmax(sub)   
    min_temp  = np.nanmin(sub)

    return float(mean_temp), float(max_temp), float(min_temp)


def bbox_area_km2_vec(lon_min, lon_max, lat_min, lat_max, R=6371.0):
    lon1 = np.deg2rad(np.minimum(lon_min, lon_max))
    lon2 = np.deg2rad(np.maximum(lon_min, lon_max))
    lat1 = np.deg2rad(np.minimum(lat_min, lat_max))
    lat2 = np.deg2rad(np.maximum(lat_min, lat_max))
    
    return (R**2) * (lon2 - lon1) * (np.sin(lat2) - np.sin(lat1))

def bbox_area_km2(lon_min, lon_max, lat_min, lat_max):
    
    lon1, lon2 = np.deg2rad(sorted([lon_min, lon_max]))
    lat1, lat2 = np.deg2rad(sorted([lat_min, lat_max]))

    return (R**2) * (lon2 - lon1) * (np.sin(lat2) - np.sin(lat1))


def compute_stats(lon, lat, temp, dn, threshold = -40):
    
    nl = gs.find_nucleos(       
        lon,
        lat,
        temp,
        dn= dn,
        temp_threshold=threshold,
    )
    
    nl["cold_km2"] = nl.apply(
        lambda r: cold_area_in_bbox_km2(
            temp=temp,
            lon=lon,
            lat=lat,
            threshold=threshold,
            lon_min=r.lon_min, lon_max=r.lon_max,
            lat_min=r.lat_min, lat_max=r.lat_max,
        ),
        axis=1
    )
    
    nl["bbox_km2"] = bbox_area_km2_vec(
        nl.lon_min, nl.lon_max, nl.lat_min, nl.lat_max)
    
    stats = nl.apply(
        lambda r: cold_stats_in_bbox(
            temp=temp,
            lon=lon,
            lat=lat,
            threshold=threshold,
            lon_min=r.lon_min,
            lon_max=r.lon_max,
            lat_min=r.lat_min,
            lat_max=r.lat_max,
        ),
        axis=1
    )
    
    nl["mean_temp"] = [s[0] for s in stats]
    nl["max_temp"]  = [s[1] for s in stats]
    nl["min_temp"]  = [s[2] for s in stats]
    
    return nl.round(3)


