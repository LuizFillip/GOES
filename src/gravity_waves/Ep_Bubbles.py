import pandas as pd
import base as b 
import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import numpy as np 

path_ep = 'GOES/data/Ep/'



def select_sectors(
        df, 
        lat_min = -20, 
        lat_max = -10, 
        lon_min = -80, 
        lon_max = -30
        ):
      
    ds = df.loc[
        ((df['lon'] > lon_min) & 
         (df['lon'] < lon_max)) &
        ((df['lat'] > lat_min) & 
         (df['lat'] < lat_max))
        ]
    return ds 


    

def plot_scatter_quadratic(ds):
    
    def r2_score(y, y_pred):
        ss_res = np.sum((y - y_pred) ** 2)  
        ss_tot = np.sum((y - np.mean(y)) ** 2)  
        return 1 - (ss_res / ss_tot)
    
    y, x = ds['wave'].values, ds['epb'].values

    coeffs = np.polyfit(x, y, 2)
    
    # Extract coefficients
    a, b, c = coeffs
    print(f"Quadratic equation: y = {a:.3f}x² + {b:.3f}x + {c:.3f}")
    
    # Generate points for plotting
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = np.polyval(coeffs, x_fit)
    
    f, ax = plt.subplots()
    ax.scatter(x, y, color='k', label="Data")
    ax.plot(x_fit, y_fit, label="Quadratic Fit", color="r")
    
    y_pred = np.polyval(coeffs, x)
    
    print(r2_score(y, y_pred))
    
    ax.set(
        ylabel = 'Ep (J/k)', 
        xlabel = 'Midnight EPBs', 
        xlim = [-1, 15], 
        ylim = [8, 15]
        )
    

def get_averages_from_data(df2, df1):
   
    avg_results = {}
    
    vls = df1.index
    
    for i in range(len(vls) - 1):
        start_date = vls[i]
        end_date = vls[i + 1]
        
        subset = df2.loc[(df2.index >= start_date) & 
                          (df2.index <= end_date)]
        
        if not subset.empty:
            avg_results[start_date] = subset.mean()
    
    
    return pd.DataFrame(avg_results).T


def plot_linear_scatter(ax, ds):
    n = ds.columns[0] 
    
    y = ds.iloc[:, 0].values
    x = ds.iloc[:, 1].values
    
    ax.scatter(x, y, marker = '^', s = 150)
    
    fit = b.linear_fit(x, y)
    
   
    line, = ax.plot(
        x, 
        fit.y_pred,
        lw = 2, 
        # color = 'red', 
        label = f'{n}'
        )
    
    ax.set(xlim = [0, 80])
    # 
    
    
    return line.get_color(), fit.r2_score

class PotentialEnergy(object):
    
    def __init__(self):
        
        return 
    
def group_by_time(
        df, 
        stp = 'month', 
        col = '90_110', 
        name = 'wave'
        ):
    
    col = f'mean_{col}'
    
    df['month'] = df.index.month 
    df['year'] = df.index.year
    
    df = df.between_time(
        '18:00', '05:00')
    
    df = df.groupby([stp])[col].mean()

    return df.to_frame(name)

    

    
def plot_seasonal_evolution(eb, wv):
    fig, ax = plt.subplots(
        figsize = (14, 7), 
        dpi = 300
        )
    
    ax.bar(eb.index, eb, width = 0.1)
    
    ax1 = ax.twinx()
    
    ax1.plot(
        wv.index, wv['mean_90_110'], 
        lw = 2, color = 'red')

def epbs(time = 'year', total = True):
    p = pb.BubblesPipe('events_5')
    
    ds = p.sel_type('midnight')
    
    df = p.time_group(ds, time = time)
    
    cols = [-70, -60, -50]
    
    if total:
        return df[cols].sum(
        axis = 1).to_frame('All')
    else:
        return df 





  



def Ep_by_sectors(time = 'month', total = False):
    
    df = b.load('GOES/data/ep_avg')
    
    df = df.loc[~(
        (df['mean_90_110'] < 0) | 
        (df['mean_90_110'] > 100))
        ]
    
    if total:
        df = select_sectors(
            df, 
            lat_min = -10, 
            lat_max = 10, 
            lon_min = -70, 
            lon_max = -40
            )
        
        return group_by_time(
                df, 
                stp = time, 
                col = '90_110', 
                name = 'All'
                )
   
    
    year = 2013
    out = []
    for sector in np.arange(-80, -40, 10):
        
        ds = pb.filter_region(
            df, year, sector)
        
        out.append(
            group_by_time(
                ds, 
                stp = time, 
                name = sector
                )
            )
        
    return pd.concat(out, axis = 1)





def plot_all_sectors(ax, time):
    
    ds = Ep_by_sectors(
        time = time, total = True)
    
    ds1 = epbs(
        time = time, total = True)
    
    data = [ds, ds1]
     
    jj = pd.concat(data, axis = 1) 
    
    jj = jj.replace(np.nan, 0)
    c, r2 = plot_linear_scatter(
        ax, jj
        )
    
    ax.text(
        0.55, 0.3 + 0.1, 
        f'$R^2$ = {r2}', 
        color = c, 
        transform = ax.transAxes
        )
    
    return None 
    
def plot_sectors_div(ax, time):

    ds = Ep_by_sectors(
        time = time, 
        total = False)
    
    ds1 = epbs(
        time = time, 
        total = False
        )
    
    sectors =  np.arange(-70, -40, 10)
    
    for i, col in enumerate(sectors):
        
        data = [ds[col], ds1[col]]
        
        jj = pd.concat(data, axis = 1) 
        
        jj = jj.replace(np.nan, 0)
        
        c, r2 = plot_linear_scatter(
            ax, jj
            )
        
        ax.text(
            0.55, 0.3 - (i/10), 
            f'$R^2$ = {r2}', 
            color = c, 
            transform = ax.transAxes
            )

fig, ax = plt.subplots(
    figsize = (16, 10), 
    ncols = 2,
    dpi = 300, 
    sharex = True, 
    sharey = True 
    )

plt.subplots_adjust(wspace = 0.1)

ax[0].text(0.03, 0.9, '(a) Month', 
           transform = ax[0].transAxes)
plot_all_sectors(ax[0], time = 'month')

plot_sectors_div(ax[0], time = 'month')

ax[1].text(
    0.03, 0.9, '(b) Year', 
           transform = ax[1].transAxes)

plot_all_sectors(ax[1], time = 'year')

plot_sectors_div(ax[1], time = 'year')

ax[0].set(ylim = [9, 14], xlim = [0, 120])

ax[0].legend(
    ncol = 4,
    title = 'Sectors',
    loc = 'upper center',
    fontsize = 30,
    bbox_to_anchor = (1, 1.2) 
    )