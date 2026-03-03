from __future__ import annotations
from pathlib import Path
from tqdm import tqdm
import base as b
import scrap as wb
import GOES as gs
import datetime as dt 
import requests
from io import BytesIO
from PIL import Image

def goes_url(year: int, month: int) -> str:
    base = "http://ftp.cptec.inpe.br/goes/"

    if 2003 <= year < 2013:
        base += "goes12/retangular_4km/ch4_bin/"
    elif 2013 <= year < 2018:
        base += "goes13/retangular_4km/ch4_bin/"
    else:  # year >= 2018
        base += "goes16/retangular/ch13/"

    return f"{base}{year:04d}/{month:02d}/"


def ensure_goes_dir(drive: str, year: int, month: int) -> Path:
    root = Path(f"{drive}:\\database\\goes")
    path = root / f"{year:04d}" 
    b.make_dir(str(path))
    path = path / f"{month:02d}"
    b.make_dir(str(path))
    return path


def _is_candidate_file(name: str) -> bool:
    # cptec costuma ter .gz e/ou .nc
    return name.endswith(".gz") or name.endswith(".nc")


def _minute_filter_ok(filename: str, only_minute_zero: bool) -> bool:
    if not only_minute_zero:
        return True
    try:
        return gs.fn2dn(filename).minute == 0
    except Exception:
        # se não conseguir parsear, ignora (não baixa)
        return False


def download_goes_month(
    year: int,
    month: int,
    drive: str = "D",
    only_minute_zero: bool = True,
    skip_existing: bool = True,
    ) -> list[str]:
    """
    Baixa arquivos GOES do mês (CPTEC FTP) 
    para drive:\\database\\goes\\YYYY\\MM\\
    Retorna lista dos arquivos baixados.
    """
    url = goes_url(year, month)
    out_dir = ensure_goes_dir(drive, year, month)

    hrefs = wb.request(url)  # deve retornar iterável de strings
    downloaded: list[str] = []

    desc = f"Download GOES {year:04d}-{month:02d}"
    for href in tqdm(hrefs, desc=desc):
        
        if not _is_candidate_file(href):
            continue
        # if not _minute_filter_ok(href, only_minute_zero):
        #     continue
       
        out_path = out_dir / href
        if skip_existing and out_path.exists():
            continue
        
        wb.download(url, href, str(out_dir))
        downloaded.append(href)

    return downloaded


def download_main(year = 2012, start = 1, end = 12):
    
    for month in range(start, end + 1):
 
        downloaded = download_goes_month(
            year, 
            month, 
            drive = "D", 
            only_minute_zero=True
            )
        print(f"{month:02d}/{year}: {len(downloaded)} arquivos baixados")
        

def image_url(dn):
    url = 'https://ftp.cptec.inpe.br/goes/goes13/goes13_web/ams_ir2_alta'
    url += f'/{dn.year}/{dn.month:02d}/'
    hrefs = wb.request(url)

    hrefs = [h for h in hrefs if 'jpg' in h]
    hrefs = wb.request(url)
    
   
    fname = [href for href in hrefs if fn2dn(href) == dn][0]

    return url + fname    

def fn2dn(fname):
    dn = fname.split('_')[-1][:-4]
    try:
        return dt.datetime.strptime(dn, '%Y%m%d%H%M%S')
    except:
        return ''



def imshow_url(url):
    r = requests.get(url, timeout = 30)
    r.raise_for_status()
 
    return Image.open(BytesIO(r.content))

# download_main(2013)