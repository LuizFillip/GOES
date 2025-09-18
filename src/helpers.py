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
        lon_min = -50, 
        lon_max = -40, 
        lat_min = -10, 
        lat_max = 10
        ):
    return  df.loc[
        ((df['lon'] > lon_min) & (df['lon'] < lon_max)) &
        ((df['lat'] > lat_min) & (df['lat'] < lat_max))
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
