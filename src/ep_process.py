import pandas as pd 
import scipy.io
import numpy as np 
import base as b 
import matplotlib.pyplot as plt 

b.config_labels(fontsize = 22)

def ep_data(key):
    raw = scipy.io.loadmat('GOES/data/Monthly_Mean_EP.mat')

    values = raw[key][0][0]
    
    data = values[4]
    
    index = pd.date_range(
        '2013-01-01', 
        '2022-12-31', 
        freq = '1M'
        )
    
    heights = np.arange(20, 111)
    
    ds = pd.DataFrame(data, index = index, columns = heights)
    
    return ds.loc[ds.index.year == 2013]


def filter_space(
        df, 
        x0 = -80, 
        x1 = -30, 
        y0 = 10, 
        y1 = 0
        ):
    return  df.loc[
        ((df['Lon'] > x0) & (df['Lon'] < x1)) &
        ((df['Lat'] > y0) & (df['Lat'] < y1))
        ]

def to_percent(df):
    df = df.resample('1M').size() 
    return (df / df.values.max()) * 100

def load_nucleos(
        year = 2013,
        lat_min = -10,
        lat_max = 0
    ):
    
    df = b.load(f'GOES/data/nucleos2/{year}')
    
    df['Lon'] = (df['lon_max'] + df['lon_min']) / 2
    df['Lat'] = (df['lat_max'] + df['lat_min']) / 2
    
    df = filter_space(
        df, 
        y0 = lat_min, 
        y1 = lat_max
        )
    
    return df 

def filter_temperature(df, temp, step  = 10):
 
    return df.loc[
        (df['temp'] < temp) & 
        (df['temp'] > temp - step)
        ]
    

def filter_areas(area = 100):
    
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

def corr_for_each_height(df, ds, temp = -50):
    
    heights = np.arange(20, 111)
    
    filtered_data = filter_temperature(df, temp, step  = 10)
    
    nucleos = to_percent(filtered_data)
    
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



def plot_latitudes(ax, lat, temp):
    
    
    lat_min = lat
    lat_max = lat + 10
    ds = load_nucleos(
        lat_min = lat_min,
        lat_max = lat_max
        )
    
    key = f'Latitudinal_Monthly_Means_{abs(lat_min)}_{abs(lat_max)}'
    
    name = f'{lat_min}/{lat_max}'
    for temp in np.arange(-80, -20, 10):
        try:
            plot_correlation_height(
                ax, 
                ep_data(key), 
                ds, 
                temp, name
                )
        except:
            pass 
        

temp = -60 
lats = np.arange(-40, 20, 10 )

def plot_latitudes_corr_for_temp():
    
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
        
        plot_latitudes(ax, lats[i], temp)   
    
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
    
# df = load_nucleos(
#         year = 2013,
#         lat_min = -10,
#         lat_max = 0
#     )

