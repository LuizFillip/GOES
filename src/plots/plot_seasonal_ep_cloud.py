import pandas as pd 
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os
import datetime as dt 
import GOES as gs 
import base as b 

from scipy.ndimage import gaussian_filter

b.sci_format()
 
 

def occurrence_rate_grid(
        nl_season, lon_bins, lat_bins, n_total):

    df = nl_season.copy()

    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["lon_bin"] = pd.cut(
        df["lon"], lon_bins, 
        labels=lon_bins[:-1]
        )
    
    df["lat_bin"] = pd.cut(
        df["lat"], lat_bins, 
        labels=lat_bins[:-1]
        )

    counts = (
        df.groupby(["lon_bin", "lat_bin"])
          .size()
          .to_frame("hits")
          .reset_index()
    )

    counts["occurrence_%"] = (counts["hits"] / n_total) * 100

    grid = pd.pivot_table(
        counts,
        index="lat_bin",
        columns="lon_bin",
        values="occurrence_%"
    )

    return grid.fillna(0)

def occurrence_kernel_smooth(
        nl_season, lon_bins, lat_bins, sigma=1.5):
    
    n_total = len(nl_season.index.unique())
    
    grid = occurrence_rate_grid(
        nl_season,
        lon_bins,
        lat_bins,
        n_total= n_total
    )

    smooth = gaussian_filter(grid.values, sigma=sigma)

    return pd.DataFrame(
        smooth,
        index=grid.index,
        columns=grid.columns
    )

dn = dt.datetime(2013, 2, 1)

fn = gs.get_path_by_dn(dn)

lon, lat, temp = gs.read_gzbin(fn)