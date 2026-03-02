import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GOES as gs
import matplotlib.colors as colors 
import datetime as dt 
from scipy.ndimage import gaussian_filter

R = 6371  # km

def bbox_area_km2(lon_min, lon_max, lat_min, lat_max):
    lon1 = np.radians(lon_min)
    lon2 = np.radians(lon_max)
    lat1 = np.radians(lat_min)
    lat2 = np.radians(lat_max)

    return (R**2) * np.abs(lon2 - lon1) * np.abs(np.sin(lat2) - np.sin(lat1))

def occurrence_area_weighted(df, lon_bins, lat_bins):
 
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["area_km2"] = bbox_area_km2(
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
        columns="lon_bin",
        values="area_km2"
    )

    return grid.fillna(0)

 

def plot_raw_occurrence_area_weighted(dn,  cmap = 'plasma'):
   
    lon_bins, lat_bins = gs.get_bins(nl, step = 2)
    
 
    grid = occurrence_area_weighted(nl, lon_bins, lat_bins)
    smooth = gaussian_filter(grid.values, sigma=1.5)
  
    vmax = np.nanpercentile(grid.values, 99)   
    norm = colors.Normalize(vmin=0, vmax=vmax)
    
 
    fig, ax = gs.map_defout(ncols=2)
    
    # Painel 1
    img1 = ax[0].pcolormesh(
        grid.columns,
        grid.index,
        grid.values,
        cmap = cmap,   # melhor que jet
        norm = norm,
        shading = "auto"
    )
    
    ax[0].set_title("Raw occurrence")
    
    # Painel 2
    img2 = ax[1].pcolormesh(
        grid.columns,
        grid.index,
        smooth,
        cmap= cmap,
        norm=norm,
        shading="auto"
    )
    
    ax[1].set_title("Smoothed occurrence")
    
    cax = ax[1].inset_axes([1.03, 0, 0.04, 1])
     
    cbar = fig.colorbar(
        img1,
        ax=ax,
        orientation="vertical",
        cax  = cax
    )
    
    cbar.set_label("Area-weighted occurrence (km²)")
    
    fig.suptitle(dn.strftime('%Y-%m-%d %H:%M'), y = 0.8)
    
    plt.tight_layout()
    plt.show()
    
    return fig 
    
 

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
    d["area_km2"] = bbox_area_km2(
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


dn = dt.datetime(2013, 2, 1)

 
fn = gs.get_path_by_dn(dn)

lon, lat, temp = gs.read_gzbin(fn)

nl = gs.find_nucleos(       
    lon,
    lat,
    temp,
    dn=None,
    temp_threshold= -40,
)

lon_bins, lat_bins = gs.get_bins(nl, step = 2)

grid = rel_occ_area_temp(nl, lon_bins, lat_bins)

keys = list(grid.keys())
grid = grid[keys[3]]

vmax = np.nanpercentile(grid.values, 99)   
norm = colors.Normalize(vmin = 0, vmax = vmax)


sigma = 1.5

smooth = gaussian_filter(grid.values, sigma=sigma)
fig, ax = gs.map_defout(ncols=1)

cmap = 'jet'
img1 = ax.pcolormesh(
    grid.columns,
    grid.index,
    smooth,
    cmap= cmap,   # melhor que jet
    # norm=norm,
    # shading="auto"
)

cax  = ax.inset_axes([1.03, 0, 0.04, 1])
 
cbar = fig.colorbar(
    img1,
    ax=ax,
    orientation="vertical",
 
    cax  = cax
)