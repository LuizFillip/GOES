
import numpy as np
import pandas as pd
import re
import GOES as gs
import base as b


DEFAULT_BOUNDS = {
    "lon_min": -70,
    "lon_max": -50,
    "lat_min": -10,
    "lat_max": 0,
}




def join_wave_nucleos(
    year=2013,
    freq="1M",
    ep_vls="Ep_max",
    area=30,
    lon_min=-70,
    lon_max=-50,
    lat_min=-10,
    lat_max=0,
):
    s1 = gs.nucleos_by_time(
        year=year,
        freq=freq,
        area=area,
        lon_min=lon_min,
        lon_max=lon_max,
        lat_min=lat_min,
        lat_max=lat_max,
    )

    s2 = gs.wave_avg_heights(
        year=year,
        freq=freq,
        values=ep_vls,
        lon_min=lon_min,
        lon_max=lon_max,
        lat_min=lat_min,
        lat_max=lat_max,
    )

    df = pd.concat([s1, s2], axis=1).dropna()

    # Para comparação sazonal/mensal dentro de um único ano
    df["month"] = df.index.month
    df = df.groupby("month", as_index=True).mean()

    return df

