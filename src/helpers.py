import pandas as pd 
import base as b 

def load(infile, date_index = False):
    
    try:
        df = pd.read_csv(infile, index_col = 0)
        df.index = pd.to_datetime(df.index) 
        
        
    except:
        df = pd.read_csv(
            infile, 
            delimiter = ';', 
            index_col = 0
            )
        df.index = pd.to_datetime(
            df.index, 
            format = 'ISO8601'
            )
        
    if date_index:
        df.index = df.index.date

    return df.sort_index()



def filter_space(
        df, 
        x0 = -80, 
        x1 = -30, 
        y0 = 10, 
        y1 = 0
        ):
    try:
        return  df.loc[
            ((df['lon'] > x0) & (df['lon'] < x1)) &
            ((df['lat'] > y0) & (df['lat'] < y1))
        ]
    except:
        return df.loc[
            ((df['x0'] > x0) & (df['x1'] < x1)) &
            ((df['y0'] > y0) & (df['y1'] < y1))
        ]


def load_nucleos(year = 2013):
    
    df = b.load(f'GOES/data/nucleos2/{year}')
    
    try:
        df['lon'] = (df['lon_max'] + df['lon_min']) / 2
        df['lat'] = (df['lat_max'] + df['lat_min']) / 2
    except:
        df['lon'] = (df['x1'] + df['x0']) / 2
        df['lat'] = (df['y1'] + df['y0']) / 2
    
    return df 

path_ep = 'GOES/data/Ep'

def potential_energy(year = 2019):
    
    df = pd.read_csv(f'{path_ep}{year}', sep = '\s+')

    df.index = pd.to_datetime(
        df['Date'] + ' ' + 
        df[['Hour', 'Minute', 'Second']
           ].astype(str).agg(':'.join, axis=1))
    
    df = df.drop(
        columns = [
        'Year', 'DOY', 'Date', 
        'Hour', 'Minute', 'Second']
        )
    
    df = df.rename(
        columns = {
            'Lon': 'lon', 
            'Lat': 'lat'
            }
        )
    return df
