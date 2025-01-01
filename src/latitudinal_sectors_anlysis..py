import base as b 
import pandas as pd 
import matplotlib.pyplot as plt 

def select_sectors(
        df, 
        lat_min = -20, 
        lat_max = -10, 
        lon_min = -80, 
        lon_max = -30
        ):
      
    
    ds = df.loc[
        ((df['Lon'] > lon_min) & 
         (df['Lon'] < lon_max)) &
        ((df['Lat'] > lat_min) & 
         (df['Lat'] < lat_max))
        ]
    return ds 

def load_nucleos(year):
    
    infile = f'GOES/data/nucleos/{year}'
    
    df = b.load(infile)
    
    df['Lon'] = (df['x1'] + df['x0']) / 2
    df['Lat'] = (df['y1'] + df['y0']) / 2
    
    return df 



def count_in_sector(df, lat_min, sample = '1M'):
    
    ds = select_sectors(
            df, 
            lat_min = lat_min, 
            lat_max = lat_min + 10, 
            )
    
    ds = ds.resample(sample).size() 
    
    return (ds / ds.values.max()) * 100

year = 2019


def run_in_latitudes(year):
    
    df = load_nucleos(year)
    
    latitudes = range(-50, 21, 10)
    out = []
    
    for lat_min in latitudes:
        
        try:
            out.append( 
                count_in_sector(df, lat_min).to_frame(lat_min)
                )
        except:
            continue 
        
        
    return pd.concat(out, axis = 1)

def run_in_years():
    out = []
    
    for year in range(2013, 2023):
        
        out.append( run_in_latitudes(year))
    
    return pd.concat(out)

def plot_contour(ds):
    
    fig, ax = plt.subplots(
        figsize = (16, 10),    dpi = 300)
    
    img = ax.contourf(
        ds.columns, 
        ds.index, 
        ds.values  
        )
    
    plt.colorbar(img)
    
    ax.set(ylabel = 'Date', xlabel = 'Latitude (°)')
    
    # df.to_csv('percent_latitudes_monthly')