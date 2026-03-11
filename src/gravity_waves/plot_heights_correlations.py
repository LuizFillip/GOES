import matplotlib.pyplot as plt 
import GOES as gs
import base as b 
import pandas as pd 
import numpy as np 
  
def wave(year = 2013, freq = '1D', values = 'Ep_mean'):
    path = f'D:\\database\\SABER\\ep\\{year}'
    df = b.load(path)
    df = df.loc[(df[values] > 0 ) & (df[values] < 100)]
    df = gs.filter_space(
            df, 
            lon_min = -70, 
            lon_max = -50, 
            lat_min = -10, 
            lat_max = 0
            )
    ds = pd.pivot_table(
        df, 
        columns = 'alt', 
        index = df.index, 
        values = values
        )
    
    ds = ds.resample(freq).mean() 
    
    return ds 
    
def nucleos(year = 2013,freq = '1D', area = 0):
    
    df = b.load(f'GOES/data/nucleos_40/{year}')
    
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2
    
    df = gs.filter_space(
            df, 
            lon_min = -70, 
            lon_max = -50, 
            lat_min = -10, 
            lat_max = 0
            )
    
    df = df.loc[df['area'] > area]
    
    ds = df.resample(freq).size()
    
    ds.index = pd.to_datetime(ds.index)
    return ds.to_frame('nucleos')


def all_nucleos_for_one_height(
        year = 2013, 
        alt = 100, 
        area = 30
        ):
 
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 4)
        )
    
    ax1 = ax.twinx()
    
    df = wave(year = year)
    
 
 
    ax1.scatter(df.index, df[alt],  color = 'b',  alpha = 0.3) 
    mean = df[alt].rolling(window=7, center=True).mean()
    ax1.plot(mean, lw = 2, color = 'b') 
    
    
    ax1.set(ylabel = 'Ep average (J/kg)')
    
    b.change_axes_color(
            ax1, 
            color = 'b',
            axis = "y", 
            position = "right"
            )
    
    ds = nucleos(year = year, area = area)
    ax.scatter(ds.index, ds, alpha = 0.3)
    mean = ds.rolling(window = 7, center=True).mean()
    ax.plot(mean, lw = 2) 
    
    
    b.format_month_axes( ax, month_locator = 1)
    
    ax.set(
        ylabel = 'Number of nucleos', 
        title = f'Nucleos higher than {area} and Ep at {alt} km ', 
        xlabel = f'Months ({year})'
           )
    
    
    
# all_nucleos_for_one_height(
#         year = 2013, 
#         alt = 100, 
#         area = 30
#         )

def plot_correlation_ep_number_cels(x, y):
    
    
    fig, ax = plt.subplots(
        figsize = (6, 6), 
        sharex = True,
     
        dpi = 300)
    
    
    
    fit = b.linear_fit(x, y)
    
    corr = np.corrcoef(x, y)[1, 0]
     
    ax.plot(
        x, y, 
        markersize = 5, 
        linestyle = 'none',
      
        marker ='o', 
   
        markeredgecolor = 'black',
        markeredgewidth = 3
        )
     
    ax.plot(
        x, fit.y_pred, 
        color = 'red',
        lw = 3,  
        )
    
    ax.text(
        0.7, 0.86,
        f'r = {round(corr, 2)}', 
        transform = ax.transAxes
        )
    
    ax.legend()

freq = '30D'
year = 2012
s1 = nucleos(year = year, freq = freq, area = 0)

s2 = wave(year = year, freq = freq, values = 'Ep_mean')

# df = pd.concat([s1, s2], axis = 1).dropna()

# heights = np.arange(20, 120, 10)
# x = df['nucleos'].values
# corr = []
# for alt in heights:
#     y = df[alt].values
#     corr.append(np.corrcoef(x, y)[1, 0])
    
    
# plt.plot(corr, heights)

df = b.load(f'GOES/data/nucleos_40/{year}')

df 