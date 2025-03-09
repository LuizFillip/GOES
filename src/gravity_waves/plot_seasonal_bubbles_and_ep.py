import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import pandas as pd 
import GOES as gs 
def plot_seasonal_ep():
    
    ds = gs.Ep_by_sectors(
            time = 'month', 
            total = False
            )
    
    fig, ax = plt.subplots(
        figsize = (12, 6), dpi = 300)
    
    cols = [ -70, -60, -50]
    mks = ['s', 'o', '^']
    
    for i, col in enumerate(cols[::-1]):
        name = f'Sector {i + 1}'
        ax.plot(
            ds[col], 
            marker = mks[i], 
            lw = 2, 
            label = name
            )
    
    ax.set(
        ylabel = 'Ep (J/kg)',
        xlabel = 'Months',
        ylim = [10, 13],
        xticks = np.arange(1, 13, 1),
        xticklabels = b.month_names(
            sort = True, language = 'en'),
        
        )
    
    ax.legend()


def format_ep(col):
    df = b.load('GOES/data/ep_avg')
    
    df = df.loc[~(
        (df[col] < 0) | 
        (df[col] > 100))
        ]
    
    df = df.between_time('18:00', '05:00')
    
    return df

def linear_score(ds):
    
    y = ds.iloc[:, 0].values
    x = ds.iloc[:, 1].values
    
    
    fit = b.linear_fit(x, y)
    
    return fit.r2_score

p = pb.BubblesPipe('events_5', drop_lim = 0.2)

ds = p.sel_type('midnight')

col = 'mean_90_110'
df = format_ep(col)
year = 2013


fig, ax = plt.subplots(
    dpi = 300, 
    nrows = 3,
    sharex= True, 
    sharey= True,
    figsize = (14, 12)
    )

time = '1M'

for i, sector in enumerate(np.arange(-70, -40, 10)):
    
    df_lon = ds.loc[ds['lon'] == sector]
    
    df_size = df_lon.resample(time).size()
    
    ax[i].plot(df_size, label = sector)
    
    ds_ep = df.loc[(df['lon'] > sector) &
                   (df['lon'] < sector + 10)] 
    
    ds_mean = ds_ep.resample(time).mean()[col]
    
    ax1 = ax[i].twinx()

    ax1.plot(ds_mean, label = sector, color = 'red')
    
    ds1 = pd.concat(
        [df_size, ds_mean], axis = 1
        ).interpolate().dropna()
    # print(ds1)
    print(linear_score(ds1), sector)
    
    ax1.set(ylim = [9, 15])
    
# ax.legend()


  