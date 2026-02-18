from __future__ import annotations
from scipy.ndimage import label, find_objects
import numpy as np
import pandas as pd


def find_nucleos(
    lons: np.ndarray,
    lats: np.ndarray,
    data: np.ndarray,
    dn=None,
    area_threshold: float = 1.0,
    temp_threshold: float = -60.0,
    return_coords: bool = True,
    connectivity: int = 1,
) -> pd.DataFrame:
    """
    Detecta regiões (componentes conectados) onde data <= temp_threshold.
    
    Parâmetros
    ----------
    data : (ny, nx) array
        Campo 2D (ex.: temperatura). Eixo 0 = lat, eixo 1 = lon.
    lons : (nx,) array
        Longitudes correspondentes às colunas de data.
    lats : (ny,) array
        Latitudes correspondentes às linhas de data.
    dn : qualquer, opcional
        Timestamp para indexar o DataFrame.
    area_threshold : float
        Limite mínimo de área (em graus^2 se return_coords=True).
    temp_threshold : float
        Threshold: valores > threshold viram NaN; regiões são <= threshold.
    return_coords : bool
        True -> retorna lon/lat; False -> retorna índices i/j.
    connectivity : int
        1 = 4-conectado, 2 = 8-conectado.
    """

    data = np.asarray(data)
    lons = np.asarray(lons, dtype=float)
    lats = np.asarray(lats, dtype=float) #[::-1]

    if data.ndim != 2:
        raise ValueError("data precisa ser 2D (ny, nx)")
    ny, nx = data.shape
    if lons.shape[0] != nx:
        raise ValueError(f"len(lons)={len(lons)} não bate com nx={nx}")
    if lats.shape[0] != ny:
        raise ValueError(f"len(lats)={len(lats)} não bate com ny={ny}")

 
    # Máscara das regiões frias (True onde é "núcleo")
    cold = data <= temp_threshold
    cold &= np.isfinite(data)

    # Estrutura de conectividade
    if connectivity == 1:
        structure = np.array(
            [[0,1,0],
            [1,1,1],
            [0,1,0]], dtype=bool)
    elif connectivity == 2:
        structure = np.ones((3,3), dtype=bool)
    else:
        raise ValueError("connectivity deve ser 1 (4-conect) ou 2 (8-conect)")

    lab, nfeat = label(cold, structure=structure)
    objs = find_objects(lab)

    out = []
    for sl in objs:
        if sl is None:
            continue

        y_sl, x_sl = sl  # eixo 0 = y(lat), eixo 1 = x(lon)
        y0, y1 = y_sl.start, y_sl.stop   # [y0, y1)
        x0, x1 = x_sl.start, x_sl.stop   # [x0, x1)

        if return_coords:
            lon0, lon1 = lons[x0], lons[x1 - 1]
            lat0, lat1 = lats[y0], lats[y1 - 1]

            lon_min, lon_max = ((lon0, lon1) if lon0 <= lon1 else
                                (lon1, lon0))
            lat_min, lat_max = ((lat0, lat1) if lat0 <= lat1 else
                                (lat1, lat0))

            area = (lon_max - lon_min) * (lat_max - lat_min)
            if area >= area_threshold:
                out.append([lon_min, lon_max, lat_min, lat_max, area])
        else:
            # área em "pixels" se estiver em índices
            area = (x1 - x0) * (y1 - y0)
            if area >= area_threshold:
                out.append([x0, x1, y0, y1, area])

    if return_coords:
        columns = ["lon_min", "lon_max", "lat_min", "lat_max", "area"]
    else:
        columns = ["x_min", "x_max", "y_min", "y_max", "area_px" ]

    df = pd.DataFrame(out, columns=columns)

    if dn is not None:
        df["time"] = dn
        df = df.set_index("time")

    return df.dropna()
