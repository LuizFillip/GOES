import matplotlib.pyplot as plt 
import numpy as np
import base as b 

temp = -60 
lats = np.arange(-40, 20, 10 )

def corr_for_each_height():
    
    root = 'GOES/data/means'
    c_path = f'{root}/cloud/lat_20_temp_50'
    e_path = f'{root}/ep/lat_20_temp_50'

    x = b.load(c_path).values.flatten()

    ds = b.load(e_path)
    
    correlation = []
    
    for h in ds.columns:
        y = ds[h].values.flatten()
        
        # print(len(x), len(y))
        if len(x) == len(y):
            corr_value = np.corrcoef(x, y)[0, 1]  #
        else:
            corr_value = np.nan
        correlation.append(corr_value)
    return correlation

def plot_correlation_height(
        ax,
        ds, df, 
        temp, name):
    
    heights = np.arange(20, 111)
    
    correlation = corr_for_each_height(df, ds, temp)
    
    io_temp = f'{temp}°/{temp - 10}°C'

    ax.plot(correlation, heights, label = io_temp)  
    ax.legend(loc = 'lower right')
    
    ax.set(
        title = f'latitudes: {name}°',
        # xlabel = 'Correlation', 
        # ylabel = 'Altitude (km)', 
        xlim = [-1, 1.4]
        )
    
    ax.axvline(0, color = 'k', linestyle = '--')
    
    return None 

def plot_latitudes_corr_for_temp(year):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2, 
        ncols = 3, 
        figsize = (16, 12), 
        sharex = True, 
        sharey = True 
        )
    
    plt.subplots_adjust(hspace = 0.1, wspace = 0.1)
    
    for i, ax in enumerate(ax.flat):
        
        plot_latitudes(year, ax, lats[i], temp)   
    
    fontsize = 40
    
    fig.text(
        0.04, 0.35, 
        'Altitudes (km)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.43, 0.05, 
        'Correlation', 
        fontsize = fontsize
        )
    
    fig.suptitle(year)

# df1['109'].plot() 
 