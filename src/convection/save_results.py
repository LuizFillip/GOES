from pathlib import Path
import datetime as dt

import pandas as pd
from tqdm import tqdm
import GOES as gs


ROOT_OUT = Path("GOES/data/nucleos3")
ROOT_JOINED = Path("GOES/data/nucleos_40")


def run_days(
        ref: dt.datetime, 
        threshold: float = -40, 
        freq: str = "D"
        ) -> pd.DataFrame:
    """
    Processa todos os arquivos GOES retornados por 
    walk_goes para uma data de referência.
    """
    files = gs.walk_goes(ref, freq)

    if not files:
        return pd.DataFrame()

    out = []
    desc = ref.strftime("%B")
    desc = f"Processing {desc}"
    for fn in tqdm(files, desc=desc, leave=False):
        try:
            lon, lat, temp = gs.read_gzbin(fn)

            result = gs.compute_stats(
                lon,
                lat,
                temp,
                gs.fn2dn(fn),
                threshold=threshold,
            )
            out.append(result)

        except Exception as exc:
            print(f"Erro ao processar {fn}: {exc}")

    if not out:
        return pd.DataFrame()

    return pd.concat(out, ignore_index=False)


def run_month(
        year: int, 
        month: int, 
        threshold: float = -40, 
        root_out: Path = ROOT_OUT
        ) -> pd.DataFrame:
    """
    Processa um mês e salva o resultado em CSV.
    """
    ref = dt.datetime(year, month, 1)
    df = run_days(ref, threshold=threshold, freq="D")

    out_dir = root_out / f"{year}{month:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"nucleos_{year}{month:02d}_thr{abs(int(threshold))}"
    df.to_csv(out_file, index=True)

    return df


def run_year(
        year: int, 
        threshold: float = -40, 
        root_out: Path = ROOT_OUT
        ) -> pd.DataFrame:
    """
    Processa todos os meses do ano, salva
    cada mês e retorna o ano concatenado.
    """
    print(f"Find convections in {year}")

    out = []
    for month in range(1, 13):
        try:
            df_month = run_month(
                year, month, threshold=threshold, root_out=root_out)
            # if not df_month.empty:
            out.append(df_month)
        except Exception as exc:
            print(f"Erro no ano={year}, mês={month:02d}: {exc}")

    if not out:
        return pd.DataFrame()

    return pd.concat(out, ignore_index=False)


def run_all_years(
    start: int,
    end: int,
    threshold: float = -40,
    root_out: Path = ROOT_OUT,
    joined_out: Path = ROOT_JOINED,
) -> pd.DataFrame:
    """
    Processa um intervalo de anos e salva um CSV consolidado.
    """
    out = []

    for year in range(start, end + 1):
        try:
            df_year = run_year(
                year, 
                threshold=threshold, root_out=root_out)
            if not df_year.empty:
                out.append(df_year)
        except Exception as exc:
            print(f"Erro no ano {year}: {exc}")

    if not out:
        return pd.DataFrame()

    df = pd.concat(out, ignore_index=False)

    joined_out.mkdir(parents=True, exist_ok=True)
    out_file = joined_out / f"nucleos_{start}_{end}_thr{abs(int(threshold))}.csv"
    df.to_csv(out_file, index=True)

    return df


def join_year(
    year: int = 2013,
    threshold: float = -40,
    root_in: Path = ROOT_OUT,
    root_out: Path = ROOT_JOINED,
) -> pd.DataFrame:
    """
    Junta os CSVs mensais de um ano.
    """
    out = []

    for month in range(1, 13):
        monthly_dir = root_in / f"{year}{month:02d}"
        monthly_file = monthly_dir / f"nucleos_{year}{month:02d}_thr{abs(int(threshold))}.csv"

        if monthly_file.exists():
            out.append(pd.read_csv(monthly_file, index_col=0, parse_dates=True))

    if not out:
        return pd.DataFrame()

    df = pd.concat(out, ignore_index=False)

    root_out.mkdir(parents=True, exist_ok=True)
    df.to_csv(root_out / f"{year}.csv", index=True)

    return df


def test_one_file(threshold: float = -40):
    ref = dt.datetime(2013, 1, 1)
    files = gs.walk_goes(ref, "D")

    if len(files) < 3:
        msg = "Menos de 3 arquivos encontrados para o teste."
        raise ValueError(msg)

    fn = files[2]

    lon, lat, temp = gs.read_gzbin(fn)

    result = gs.compute_stats(
        lon,
        lat,
        temp,
        gs.fn2dn(fn),
        threshold=threshold,
    )

    return result


# if __name__ == "__main__":
year = 2014
# month = 2
df = run_year(year, threshold=-40)
ROOT_JOINED.mkdir(parents=True, exist_ok=True)
df.to_csv(ROOT_JOINED / f"{year}", index=True)

# import os 
# ref = dt.datetime(year, month, 1) 

# files = gs.walk_goes(ref, 'D')

# for fn in files:
#     dn = gs.fn2dn(fn)
    
#     if dn.minute == 15 or dn.minute == 45:
#         os.remove(fn)