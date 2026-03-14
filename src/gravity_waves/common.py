import numpy as np 
import re
import GOES as gs
import base as b


def make_regular_bins(series_min, series_max, step):
    """
    Cria bins regulares incluindo o máximo.
    """
    vmin = np.floor(series_min / step) * step
    vmax = np.ceil(series_max / step) * step
    return np.arange(vmin, vmax + step, step)


def round_interval(s):
    nums = re.findall(r"-?\d+\.?\d*", s)
    return f"({round(float(nums[0]))}, {round(float(nums[1]))}]"

def load_ep_data(
        year, 
        alt = 100, ep_col="Ep_mean"
        ):
    """
    Carrega e filtra os dados de EP para um ano.
    """
    path = f"D:\\database\\SABER\\ep\\{year}"
    df = b.load(path).copy()

  
    df["alt_bin"] = df["alt_bin"].apply(round_interval)
     
    df["alt"] = df["alt_bin"].str.extract(
       r"\(([-\d\.]+),")[0].astype(int)

    if alt is not None and "alt" in df.columns:
        df = df.loc[df["alt"] == alt]

    return df
 
def wave_avg_heights(
    year=2013,
    freq="1D",
    values="Ep_mean",
    lon_min=-70,
    lon_max=-50,
    lat_min=-10,
    lat_max=0,
):
    df = load_ep_data(year, alt=100, ep_col="Ep_mean", ep_max_valid=100)
  
    df = gs.filter_space(
            df,
            lon_min = lon_min,
            lon_max = lon_max,
            lat_min = lat_min,
            lat_max = lat_max,
        )
    ds = df.pivot_table(
        index = df.index,
        columns  = "alt",
        values = values,
        aggfunc = "mean",
    ).sort_index(axis = 1)

    return ds.resample(freq).mean()


