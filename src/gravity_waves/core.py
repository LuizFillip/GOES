import calendar
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io
from tqdm import tqdm


ALTITUDES = np.round(np.arange(20.0, 110.1, 0.1), 1)
ALT_BINS = np.arange(20, 121, 5)
DEFAULT_OUTDIR = Path(r"D:\database\SABER")



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


def filter_bin_by_altitude(
        df: pd.DataFrame, 
        bins: np.ndarray = ALT_BINS
        ) -> pd.DataFrame:
    """
    Agrupa por intervalos de altitude e calcula estatísticas de Ep_Tprime.
    """
    data = df.copy()
    data["alt_bin"] = pd.cut(data["alt"], bins = bins, right = True)

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
        lambda x: x.right if pd.notna(x) else np.nan
    )

    return grouped.set_index("dn")


def _pandas_attrs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte df.attrs em DataFrame com índice temporal.
    """
    if not df.attrs:
        return pd.DataFrame(index=[df.index[0]])

    return pd.DataFrame(df.attrs, index=[df.index[0]])

def _get_path_day(
        year: int, doy: int,
        root: str | Path = r"D:\database\SABERaw"
        ):
    day_path = Path(root) / str(year) / f"{doy:03d}"
    
    if not day_path.exists():
        msg = f"Pasta não encontrada: {day_path}"
        raise FileNotFoundError(msg)

    files = sorted(day_path.glob("*.mat"))
    if not files:
        msg = f"Nenhum arquivo .mat em {day_path}"
        raise FileNotFoundError(msg)
   
    return files
 
def run_saber(
        year: int, 
        doy: int,
        root: str | Path = r"D:\\database\\SABERaw", 
     
        ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processa todos os arquivos de um dia juliano.
    """
    files = _get_path_day(year, doy, root) 

    out_ep = []
    out_at = []
    desc = f"Run SABER {year}-{doy:03d}"
  
    for file in files:
        try:
            df = ep_data(file)
            out_ep.append(filter_bin_by_altitude(df))
            out_at.append(_pandas_attrs(df))
        except Exception as exc:
            print(f"Erro em {file.name}: {exc}")

 

    data = pd.concat(out_ep, ignore_index = False)
    attrs = pd.concat(out_at, ignore_index = False) if out_at else pd.DataFrame()

    return data, attrs


def run_year(
    year: int,
    root: str | Path = r"D:/database/SABERaw",
    outdir: str | Path = DEFAULT_OUTDIR,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processa um ano completo e salva CSVs.
    """
    outdir = Path(outdir)
    ep_dir = outdir / 'step_5' / "ep"
    # attrs_dir = outdir / "attrs"
    ep_dir.mkdir(parents=True, exist_ok=True)
    # attrs_dir.mkdir(parents=True, exist_ok=True)

    ndays = 366 if calendar.isleap(year) else 365

    out_ep = []
    # out_at = []

    print(f"Starting year {year}")

    for doy in tqdm(range(1, ndays + 1), desc=f"Year {year}"):
        try:
            data, attrs = run_saber(
                year, doy, root = root)
            out_ep.append(data)
            # out_at.append(attrs)
        except FileNotFoundError:
            continue
        except Exception as exc:
            print(f"Erro no ano={year}, doy={doy:03d}: {exc}")
            continue

    if not out_ep:
        raise ValueError(f"Nenhum dado processado para o ano {year}")

    df = pd.concat(out_ep, ignore_index=False)
    # ds = pd.concat(out_at, ignore_index=False) if out_at else pd.DataFrame()

    df.to_csv(ep_dir / f"{year}")
    # ds.to_csv(attrs_dir / f"{year}")

    return df#, ds


# if __name__ == "__main__":
# for year in range(2012, 2018):
 
#     df, ds = run_year(year)


def test_day():
    
    df, ds = run_saber(2013, 2)
    
    ds = pd.pivot_table(
        df, columns = df.index, index = 'alt', values = 'Ep_mean')
    
    import matplotlib.pyplot as plt 
    
    
    img = plt.contourf( 
        ds.columns, 
        ds.index, 
        ds.values, 30, cmap = 'jet')
    
    
    plt.colorbar(img)