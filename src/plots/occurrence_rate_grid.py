import pandas as pd 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from scipy.ndimage import gaussian_filter
import GEO as gg
import datetime as dt 
import GOES as gs 
import base as b 
import numpy as np 

b.sci_format(fontsize = 20)
 
def rel_occ_area_temp(
        df: pd.DataFrame, 
        lon_bins, 
        lat_bins
        ) -> dict[str, pd.DataFrame]:
    """
    Retorna mapas (lat_bin x lon_bin) para:
      - occ: contagem de núcleos
      - area_sum_km2: soma das áreas (km²)
      - tmin_mean: média das mínimas por célula
      - tmean_mean: média das médias por célula
      - tmin_aw: média de temp_min ponderada pela área
      - tmean_aw: média de temp_mean ponderada pela área
    """

    d = df.copy()

    # centro geométrico (para atribuição de célula)
    d["lon"] = (d["lon_min"] + d["lon_max"]) / 2
    d["lat"] = (d["lat_min"] + d["lat_max"]) / 2

    # área real em km²
    d["area_km2"] = gs.bbox_area_km2(
        d["lon_min"], d["lon_max"],
        d["lat_min"], d["lat_max"]
        )

    # bins
    d["lon_bin"] = pd.cut(d["lon"], lon_bins, labels=lon_bins[:-1])
    d["lat_bin"] = pd.cut(d["lat"], lat_bins, labels=lat_bins[:-1])

    g = d.groupby(["lat_bin", "lon_bin"], observed=True)

    # ocorrência e área
    occ = g.size().rename("occ").reset_index()
    area_sum = g["area_km2"].sum().rename("area_sum_km2").reset_index()

    # médias simples
    tmin_mean = g["temp_min"].mean().rename("tmin_mean").reset_index()
    tmean_mean = g["temp_mean"].mean().rename("tmean_mean").reset_index()

    # ponderado por área (mais físico para “impacto”)
    def _aw(x, col):
        w = x["area_km2"].to_numpy()
        v = x[col].to_numpy()
        ok = np.isfinite(v) & np.isfinite(w) & (w > 0)
        if ok.sum() == 0:
            return np.nan
        return np.average(v[ok], weights=w[ok])

    tmin_aw = g.apply(lambda x: _aw(x, "temp_min")).rename("tmin_aw").reset_index()
    tmean_aw = g.apply(lambda x: _aw(x, "temp_mean")).rename("tmean_aw").reset_index()

    def to_grid(df_long, value):
        return pd.pivot_table(df_long, index="lat_bin", columns="lon_bin", values=value).fillna(0)

    return {
        "occ": to_grid(occ, "occ"),
        "area_sum_km2": to_grid(area_sum, "area_sum_km2"),
        "tmin_mean": pd.pivot_table(
            tmin_mean, index="lat_bin", columns="lon_bin", values="tmin_mean"),
        "tmean_mean": pd.pivot_table(
            tmean_mean, index="lat_bin", columns="lon_bin", values="tmean_mean"),
        "tmin_aw": pd.pivot_table(
            tmin_aw, index="lat_bin", columns="lon_bin", values="tmin_aw"),
        "tmean_aw": pd.pivot_table(
            tmean_aw, index="lat_bin", columns="lon_bin", values="tmean_aw"),
    }


def occurrence_rate_grid(
        nl_season, 
        lon_bins, 
        lat_bins, 
        n_total
        ):

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
    counts["occurrence_%"] = (
        counts["hits"] / n_total
        ) * 100
    values = "occurrence_%"
        
    grid = pd.pivot_table(
        counts,
        index = "lat_bin",
        columns = "lon_bin",
        values = values 
    )

    return grid.fillna(0)

def occurrence_kernel_smooth(
        nl_season, 
        lon_bins, 
        lat_bins, 
        sigma = 1.5
        ):
    
    n_total = len(nl_season.index.unique())
    
    grid = occurrence_rate_grid(
        nl_season,
        lon_bins,
        lat_bins,
        n_total  
    )

    smooth = gaussian_filter(grid.values, sigma = sigma)

    return pd.DataFrame(
        smooth,
        index = grid.index,
        columns = grid.columns
    )

def get_bins(nl, step = 2):
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    return lon_bins, lat_bins 




    



def plot_occurrence_rate_grid(
        ax,
        nl,
        lon_bins,
        lat_bins, 
        cmap = 'jet', 
        vmax = 30 
        ):
    
    n_total = len(nl.index.unique())

    grid = occurrence_rate_grid(
        nl,
        lon_bins,
        lat_bins,
        n_total= n_total
    )
    
    img = ax.pcolormesh(
        grid.columns,
        grid.index,
        grid.values,
        cmap= cmap, 
        vmin = 0, 
        # vmax = vmax
    ) 
    return img 
    

def plot_kernel_smooth(
        ax, nl, 
        lon_bins, 
        lat_bins, 
        sigma = 1.5
        ):
    
    grid = occurrence_kernel_smooth(
            nl, 
            lon_bins, 
            lat_bins, 
            sigma = sigma
            )
      
    img = ax.pcolormesh(
        grid.columns,
        grid.index,
        grid.values,
        cmap="jet", 
    )
        
    ax.set(title = f'Gaussian filter ($\sigma$ = {sigma})')
    
    return img




infile = 'GOES/data/nucleos3/201301'

df = b.load(infile)