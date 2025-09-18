 
import pandas as pd 
import matplotlib.pyplot as plt 
import GOES as gs 

def run_in_latitudes(year):
    
    df = gs.load_nucleos(year)
    
    latitudes = range(-50, 21, 10)
    out = []
    
    for lat_min in latitudes:
        
        try:
            ds = count_in_sector(df, lat_min)
            out.append( 
                ds.to_frame(lat_min)
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
    
    ax.set(
        ylabel = 'Date', 
           xlabel = 'Latitude (°)')
    
    # df.to_csv('percent_latitudes_monthly')
    




def filter_areas(
        df, 
        area = 100):
    
    a1 = df.loc[
        (df['area'] > 0 ) & 
        (df['area'] < 100)
        ]
    
    a2 = df.loc[
        (df['area'] > 100 ) & 
        (df['area'] < 200)
        ]
    
    a3 = df.loc[
        (df['area'] > 200 )
        ]
    
    if area == 100:
        
        return a1
    elif area == 200:
        return a2 
    else:
        return a3

# def test_areas():
    
    
year = 2019

out = []
for year in range(2013, 2022):
    
    df = gs.load_nucleos(year)
    
    
    df = df.loc[~(df['area'] > 2000)]
    
    ds = gs.filter_space(
            df, 
            lon_min = -50, 
            lon_max = -40, 
            lat_min = -10, 
            lat_max = 10
            )
    
    sel = ds.resample('1D').count()['lat']
    out.append(sel / sel.max())
    
df = pd.concat(out)

#%%%

# df.loc[df.index.year >= 2018].plot() 
# df

df = gs.load_nucleos(year)

df 