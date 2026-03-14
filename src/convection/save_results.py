from pathlib import Path
import datetime as dt
import pandas as pd
from tqdm import tqdm
import GOES as gs


ROOT_OUT = "GOES/data/nucleos3/"
ROOT_JOINED = Path("GOES/data/nucleos_40")


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
    for fn in tqdm(files, desc=desc, leave=True):
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
        out_dir: Path = ROOT_OUT
        ) -> pd.DataFrame:
    """
    Processa um mês e salva o resultado em CSV.
    """
    ref = dt.datetime(year, month, 1)
    df = run_days(ref, threshold = threshold, freq = "D")
 
    df.to_csv(out_dir, index = True)

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
        
        out_dir = Path(f"{root_out}{year}{month:02d}")
        
        if out_dir.exists():
            continue
        
        df_month = run_month(
            year, month, 
            threshold = threshold,
            out_dir = out_dir
            )
        if not df_month.empty:
            out.append(df_month)
       
 
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
                threshold = threshold, 
                root_out = root_out
                )
            if not df_year.empty:
                out.append(df_year)
        except Exception as exc:
            print(f"Erro no ano {year}: {exc}")

    if not out:
        return pd.DataFrame()

    df = pd.concat(out, ignore_index = False)

    # joined_out.mkdir(parents = True, exist_ok = True)
    out_file = joined_out / f"nucleos_{start}_{end}_thr{abs(int(threshold))}"
    df.to_csv(out_file, index = True)

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
    import base as b  
    
    out = []
    desc = f'Joining {year}'
    for month in tqdm(range(1, 13), desc):
        monthly_dir = Path(ROOT_OUT) / f"{year}{month:02d}"
        out.append(b.load(monthly_dir))
        
    df = pd.concat(out).sort_index()

    df.to_csv(ROOT_JOINED / f"{year}", index=True)

    return df



def main():
 
    year = 2017
     
    df = run_year(year, threshold = -40)
    ROOT_JOINED.mkdir(parents=True, exist_ok=True)
    df.to_csv(ROOT_JOINED / f"{year}", index=True)

# main()
