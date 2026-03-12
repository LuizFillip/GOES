import numpy as np 
import GOES as gs 
import pandas as pd 

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

def occurrence_area_weighted(nl, lon_bins, lat_bins):
    df = nl.copy()
 
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["area_km2"] = gs.bbox_area_km2(
        df["lon_min"], df["lon_max"],
        df["lat_min"], df["lat_max"]
    )

    df["lon_bin"] = pd.cut(df["lon"], lon_bins, labels=lon_bins[:-1])
    df["lat_bin"] = pd.cut(df["lat"], lat_bins, labels=lat_bins[:-1])

    weighted = (
        df.groupby(["lon_bin", "lat_bin"])["area_km2"]
          .sum()
          .reset_index()
    )

    grid = pd.pivot_table(
        weighted,
        index="lat_bin",
        columns = "lon_bin",
        values = "area_km2"
    )

    return grid.fillna(0)
