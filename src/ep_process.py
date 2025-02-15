import numpy as np 
import base as b 
import matplotlib.pyplot as plt 
import GOES as gs

b.config_labels(fontsize = 22)



def corr_for_each_height(df, ds, temp = -50):
    
    heights = np.arange(20, 111)
    
    # filtered_data = filter_temperature(df, temp, step  = 10)
    
    nucleos = gs.to_percent(df)
    
    x = nucleos.values 
    
    correlation = []
    
    for h in heights:
        y = ds[h].values
        correlation.append(np.corrcoef(x, y)[0, 1])
        
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



def plot_latitudes(year, ax, lat, temp):
    
    
    lat_min = lat
    lat_max = lat + 10
    ds = gs.load_nucleos(
        year,
        lat_min = lat_min,
        lat_max = lat_max
        )
    
    
    name = f'{lat_min}/{lat_max}'
    # for temp in np.arange(-80, -20, 10):
    temp = -30
    # try:
    plot_correlation_height(
        ax, 
        latitudinal_data_ep(year, lat_min, lat_max), 
        ds, 
        temp, name
        )
        # except:
        #     pass 
        

temp = -60 
lats = np.arange(-40, 20, 10 )

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



