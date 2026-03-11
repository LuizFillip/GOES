# import pandas as pd 
# import scipy.io
# import numpy as np 
# import os 
# from tqdm import tqdm 
# import base as b 

# path_ep = os.getcwd() + '/GOES/data/Ep/'

# def filter_space(
#         df, 
#         lon_min = -50, 
#         lon_max = -40, 
#         lat_min = -10, 
#         lat_max = 10
#         ):
#     return  df.loc[
#         ((df['lon'] > lon_min) & (df['lon'] < lon_max)) &
#         ((df['lat'] > lat_min) & (df['lat'] < lat_max))
#     ]


# def format_altitudes_attrs(path):
#     df = scipy.io.loadmat(path)
    
#     alts = np.arange(20, 110.1, 0.1)
     
#     ds = pd.DataFrame(index = alts)
    
#     for key, vl in df.items():
        
#         if len(vl) == len(alts):
#             ds[key] = vl
#         if len(vl) == 1:
#             ds.attrs[key] = vl[0][0].round(3)
#         if 'Newx' in key:
#             new_key = key[:3].lower()
#             ds.attrs[new_key] = vl.mean().round(3)
    
#     return ds.round(3) 
 
# def coords_time(fn):
#     '''
#     ex:  'SABER_2012_001_03_50_10_14.76_307.18_GLOBAL.mat'
#     2012 é ano
#     001 é DOY (dia do ano de 001 até 365/366)
#     03 é hora
#     50 é minuto
#     10 é segundo 
#     14.76 é latitude (-90 até 90 grau)
#     307.18 é longitude ( 0 to 360 grau)
#     '''
     
#     import datetime as dt 
 
#     ls = fn.split('_')
    
#     year = int(ls[1])
#     doy = int(ls[2])
#     hour = int(ls[3])
#     minute = int(ls[4])
#     second = int(ls[5])
#     lat = float(ls[6])
#     lon = float(ls[7])
    
#     dn = dt.datetime(year, 1, 1) + dt.timedelta(
#         days = doy - 1, 
#         hours = hour,
#         minutes = minute, 
#         seconds = second
#         )
#     return dn, lat, lon

# def ep_data(path, fn):
#     dn, lat, lon = coords_time(fn)
#     df = format_altitudes_attrs(path + fn)
#     df['dn'] = dn 
#     df['lat'] = lat
#     df['lon'] = lon - 360
#     df['alt'] = df.index 
#     return df.set_index('dn') 

# def filter_bin_by_altitude(df):
#     bins = np.arange(20, 121, 10)   # 20–40, 40–60, ...
#     df['alt_bin'] = pd.cut(df['alt'], bins=bins)
    
#     ds = df.groupby(
#         ['dn', 'alt_bin', 'lat', 'lon']).agg({
#         'Ep_Tprime': ['mean', 'std', 'max'] 
#     })
    
#     ds.columns = [
#         ''.join(col).strip('_').replace(
#             'Tprime', '') if isinstance(col, tuple) else col
#         for col in ds.columns
#     ]
    
#     ds['alt'] = bins[:-1]
    
#     return ds  

# def pandas_attrs(df):
#     return pd.DataFrame(df.attrs, index = [df.index[0]]) 



# def run_saber(year, doy):
#     path = f'D:\\database\\{year}\\{doy:03d}\\'

#     files = os.listdir(path)
#     out_ep = []
#     out_at = []
#     desc = f'Run saber - {doy}'
#     for fn in tqdm(files, desc):
        
#         df = ep_data(path, fn)
#         out_ep.append(filter_bin_by_altitude(df))
#         out_at.append(pandas_attrs(df))
      
        
#     data = pd.concat(out_ep)
#     attrs = pd.concat(out_at)
    
#     return data, attrs 

# def run_year(year):
#     path_out = 'D:\\database\\SABER\\'

#     out_ep = []
#     out_at = []    
#     print('Starting,', year)
#     for doy in range(1, 366):
#         try:
#             data, attrs = run_saber(year, doy)
#             out_ep.append(data)
#             out_at.append(attrs)
#         except:
#             continue
        
#     df = pd.concat(out_ep)
#     ds = pd.concat(out_at)
    
#     df.to_csv(f'{path_out}ep\\{year}')
#     ds.to_csv(f'{path_out}attrs\\{year}')
    
#     return df, ds 

# year = 2014
# df, ds = run_year(year)

import calendar
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io
from tqdm import tqdm


ALTITUDES = np.round(np.arange(20.0, 110.1, 0.1), 1)
ALT_BINS = np.arange(20, 121, 10)
DEFAULT_OUTDIR = Path(r"D:\database\SABER")


def filter_space(
    df: pd.DataFrame,
    lon_min: float = -50,
    lon_max: float = -40,
    lat_min: float = -10,
    lat_max: float = 10,
) -> pd.DataFrame:
    """Filtra o DataFrame por limites espaciais."""
    mask = (
        df["lon"].between(lon_min, lon_max, inclusive="neither")
        & df["lat"].between(lat_min, lat_max, inclusive="neither")
    )
    return df.loc[mask].copy()


def coords_time(filename: str) -> tuple[datetime, float, float]:
    """
    Extrai datetime, latitude e longitude a partir do nome do arquivo.

    Exemplo:
    SABER_2012_001_03_50_10_14.76_307.18_GLOBAL.mat
    """
    stem = Path(filename).stem
    parts = stem.split("_")

    if len(parts) < 8:
        raise ValueError(f"Nome de arquivo inválido: {filename}")

    year = int(parts[1])
    doy = int(parts[2])
    hour = int(parts[3])
    minute = int(parts[4])
    second = int(parts[5])
    lat = float(parts[6])
    lon = float(parts[7])

    dn = datetime(year, 1, 1) + timedelta(
        days=doy - 1,
        hours=hour,
        minutes=minute,
        seconds=second,
    )

    # converter 0–360 para -180–180
    if lon > 180:
        lon -= 360

    return dn, lat, lon


def _squeeze_mat_value(value):
    """Remove dimensões desnecessárias de arrays lidos do .mat."""
    return np.asarray(value).squeeze()


def format_altitudes_attrs(filepath: str | Path) -> pd.DataFrame:
    """
    Lê arquivo .mat e separa:
    - séries verticais com tamanho igual ao perfil de altitude
    - atributos escalares em df.attrs
    """
    raw = scipy.io.loadmat(filepath)
    ds = pd.DataFrame(index=ALTITUDES)

    for key, value in raw.items():
        if key.startswith("__"):
            continue

        arr = _squeeze_mat_value(value)

        # perfil vertical
        if arr.ndim == 1 and arr.size == ALTITUDES.size:
            ds[key] = np.round(arr.astype(float), 3)

        # escalar
        elif arr.ndim == 0 or arr.size == 1:
            try:
                ds.attrs[key] = round(float(arr), 3)
            except (TypeError, ValueError):
                pass

        # médias de variáveis contendo "Newx"
        if "Newx" in key and np.issubdtype(arr.dtype, np.number):
            try:
                new_key = key[:3].lower()
                ds.attrs[new_key] = round(float(np.nanmean(arr)), 3)
            except (TypeError, ValueError):
                pass

    return ds


def ep_data(filepath: str | Path) -> pd.DataFrame:
    """
    Monta DataFrame com:
    - índice temporal dn
    - lat, lon do arquivo
    - altitude
    - perfil vertical do .mat
    """
    filepath = Path(filepath)
    dn, lat, lon = coords_time(filepath.name)

    df = format_altitudes_attrs(filepath).copy()
    df["dn"] = dn
    df["lat"] = lat
    df["lon"] = lon
    df["alt"] = df.index.values

    return df.set_index("dn")


def filter_bin_by_altitude(df: pd.DataFrame, bins: np.ndarray = ALT_BINS) -> pd.DataFrame:
    """
    Agrupa por intervalos de altitude e calcula estatísticas de Ep_Tprime.
    """
    data = df.copy()
    data["alt_bin"] = pd.cut(data["alt"], bins=bins, right=True, include_lowest=True)

    grouped = (
        data.groupby(
            ["dn", "alt_bin", "lat", "lon"], 
            observed=False)["Ep_Tprime"]
        .agg(["mean", "std", "max"])
        .rename(columns={
            "mean": "Ep_mean",
            "std": "Ep_std",
            "max": "Ep_max",
        })
        .reset_index()
    )

    # centro do bin
    grouped["alt"] = grouped["alt_bin"].apply(
        lambda x: x.mid if pd.notna(x) else np.nan
    )

    return grouped.set_index("dn")


def pandas_attrs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte df.attrs em DataFrame com índice temporal.
    """
    if not df.attrs:
        return pd.DataFrame(index=[df.index[0]])

    return pd.DataFrame(df.attrs, index=[df.index[0]])


def run_saber(year: int, doy: int, root: str | Path = r"D:\database") -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processa todos os arquivos de um dia juliano.
    """
    day_path = Path(root) / str(year) / f"{doy:03d}"

    if not day_path.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {day_path}")

    files = sorted(day_path.glob("*.mat"))
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo .mat em {day_path}")

    out_ep = []
    out_at = []
    desc = f"Run SABER {year}-{doy:03d}"
    for file in files:
        try:
            df = ep_data(file)
            out_ep.append(filter_bin_by_altitude(df))
            out_at.append(pandas_attrs(df))
        except Exception as exc:
            print(f"Erro em {file.name}: {exc}")

    if not out_ep:
        msg = f"Nenhum arquivo processado com sucesso em {day_path}"
        raise ValueError(msg)

    data = pd.concat(out_ep, ignore_index = False)
    attrs = pd.concat(out_at, ignore_index = False) if out_at else pd.DataFrame()

    return data, attrs


def run_year(
    year: int,
    root: str | Path = r"D:\database",
    outdir: str | Path = DEFAULT_OUTDIR,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processa um ano completo e salva CSVs.
    """
    outdir = Path(outdir)
    ep_dir = outdir / "ep"
    attrs_dir = outdir / "attrs"
    ep_dir.mkdir(parents=True, exist_ok=True)
    attrs_dir.mkdir(parents=True, exist_ok=True)

    ndays = 366 if calendar.isleap(year) else 365

    out_ep = []
    out_at = []

    print(f"Starting year {year}")

    for doy in tqdm(range(1, ndays + 1), desc=f"Year {year}"):
        try:
            data, attrs = run_saber(year, doy, root=root)
            out_ep.append(data)
            out_at.append(attrs)
        except FileNotFoundError:
            continue
        except Exception as exc:
            print(f"Erro no ano={year}, doy={doy:03d}: {exc}")
            continue

    if not out_ep:
        raise ValueError(f"Nenhum dado processado para o ano {year}")

    df = pd.concat(out_ep, ignore_index=False)
    ds = pd.concat(out_at, ignore_index=False) if out_at else pd.DataFrame()

    df.to_csv(ep_dir / f"{year}")
    ds.to_csv(attrs_dir / f"{year}")

    return df, ds


# if __name__ == "__main__":
# for year in range(2015, 2018):
 
#     df, ds = run_year(year)