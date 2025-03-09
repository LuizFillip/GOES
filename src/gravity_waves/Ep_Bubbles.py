import pandas as pd
import base as b 
import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import numpy as np 
import GOES as gs 

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
    
    y = ds.iloc[:, 0].values
    x = ds.iloc[:, 1].values

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
        # xlim = [-1, 15], 
        # ylim = [8, 15]
        )
    

def get_averages_from_data(df2, df1):
   
    avg_results = {}
    
    vls = df1.index
    
    for i in range(len(vls) - 1):
        start_date = vls[i]
        end_date = vls[i + 1]
        
        subset = df2.loc[
            (df2.index >= start_date) & 
            (df2.index <= end_date)
            ]
        
        if not subset.empty:
            avg_results[start_date] = subset.mean()
    
    
    return pd.DataFrame(avg_results).T

nums = {'All': 'Overall', -70: 'Sector 3', 
        -60: 'Sector 2', -50: 'Sector 1'}

def plot_linear_scatter(ax, ds, marker):
    
    n = ds.columns[0] 
   
    label = f'{nums[n]}'
    
    y = ds.iloc[:, 0].values
    x = ds.iloc[:, 1].values
    
    ax.scatter(
        x, y, 
        marker = marker, 
        s = 150, 
        label = label
        )
    
    fit = b.linear_fit(x, y)
    
   
    line, = ax.plot(
        x, 
        fit.y_pred,
        lw = 2, 
        # label = label
        )

    return fit.r2_score

class PotentialEnergy(object):
    
    def __init__(self):
        
        return 
    


    

    
def plot_seasonal_evolution(eb, wv):
    fig, ax = plt.subplots(
        figsize = (14, 7), 
        dpi = 300
        )
    
    ax.bar(eb.index, eb, width = 0.1)
    
    ax1 = ax.twinx()
    
    ax1.plot(
        wv.index, 
        wv['mean_90_110'], 
        lw = 2, 
        color = 'red'
        )

def epbs(time = 'year', total = True):
    
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.2)
    
    ds = p.sel_type('midnight')
    
    df = p.time_group(ds, time = time)
    
    cols = [-70, -60, -50]
    
    if total:
        return df[cols].sum(axis = 1).to_frame('All')
    else:
        return df 


def Ep_by_sectors(
        time = 'month', 
        total = False
        ):
    
    df = b.load('GOES/data/ep_avg')
    
    df = df.loc[~(
        (df['mean_90_110'] < 0) | 
        (df['mean_90_110'] > 100))
        ]
    
    if total:
        df = select_sectors(
            df, 
            lat_min = -20, 
            lat_max = 10, 
            lon_min = -70, 
            lon_max = -40
            )
        
        return gs.group_by_time(
                df, 
                stp = time, 
                col = '90_110', 
                name = 'All'
                )
   
    
    year = 2016
    out = []
    for sector in np.arange(-80, -40, 10):
        
        # ds = df.loc[
        #     (df['lon'] > sector) &
        #     (df['lon'] < sector + 10)] 
        
        ds = pb.filter_region(
            df, year, sector)
        
        out.append(
            gs.group_by_time(
                ds, 
                stp = time, 
                name = sector
                )
            )
        
    return pd.concat(out, axis = 1)





def plot_all_sectors(ax, time, marker = 'x'):
    
    ds = Ep_by_sectors(
        time = time, 
        total = True)
    
    ds1 = epbs(
        time = time, 
        total = True)
    
    data = [ds, ds1]
     
    jj = pd.concat(data, axis = 1) 
    
    jj = jj.replace(np.nan, 0)
    r2 = plot_linear_scatter(
        ax, jj, marker
        )
    
    ax.text(
        0.55, 0.9, 
        f'$R^2$ = {r2}', 
        color = 'k', 
        transform = ax.transAxes
        )
    
    ax.set(
        ylabel = 'Ep (J/kg)',
        xlabel = 'Midnight EPBs',
        ylim = [11, 13], 
        xlim = [-20, 220]
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
    
    sectors =  np.arange(-70, -40, 10)[::-1]
    markers = ['^', 'o', 's']
    for i, col in enumerate(sectors):
        
        data = [ds[col], ds1[col]]
        
        jj = pd.concat(data, axis = 1) 
        
        jj = jj.replace(np.nan, 0)
        
        c, r2 = plot_linear_scatter(
            ax, jj, markers[i]
            )
        
        ax.text(
            0.55, 0.25 - (i/10), 
            f'$R^2$ = {r2}', 
            color = c, 
            transform = ax.transAxes
            )
    return None 

def plot_time_column(
        ax, 
        time = 'month', 
        l = '(a)'
        ):
    name =  f'{l}'
    
    ax.text(
        0.03, 0.9, name, 
        transform = ax.transAxes
        )
    plot_all_sectors(ax, time = time)
    
    # plot_sectors_div(ax, time = time)

    return None 

def plot_correlation_ep_epbs():
    
    fig, ax = plt.subplots(
        figsize = (14, 8), 
        ncols = 2,
        dpi = 300, 
        sharex = True, 
        sharey = True 
    )

    plt.subplots_adjust(wspace = 0)
    
    # plot_time_column(
    #         ax[0], 
    #         time = 'month', 
    #         l = '(a) Seasonal'
    #         )
    
    plot_time_column(
            ax[0], 
            time = 'year', 
            l = '(a) Solar cycle'
            )
    
    ax[0].set(
        ylabel = 'Ep (J/kg)',
        ylim = [9, 14], 
        xlim = [-20, 220]
        )
    
    ax[0].legend(
        ncol = 4,
        # title = 'Sectors',
        loc = 'upper center',
        fontsize = 30,
        columnspacing=0.2,
        bbox_to_anchor = (1, 1.2) 
        )
    
    fig.text(0.4, 0.01, 'Midnight EPBs events')
    
    return fig
    
# fig = plot_correlation_ep_epbs()
import core as c 

fig, ax = plt.subplots(
    figsize = (12, 6), 
    ncols = 2,
    dpi = 300, 
    sharex = True, 
    # sharey = True 
)

def plot_epb_and_solar_flux(ax):
    
    ds = epbs(time = 'year', total = True)
    
    df = c.geo_index(eyear = 2022)
    
    df = df.resample('1Y').mean()
    
    df.index = df.index.year
    
    jj = pd.concat([ds, df['f107a']], axis = 1)
    
    
    r2 = plot_linear_scatter(
        ax, jj, 's'
        )
    
    ax.text(
        0.55, 0.9, 
        f'$R^2$ = {r2}', 
        color = 'k', 
        transform = ax.transAxes
        )
    
    ax.set(
        ylabel = 'F10.7 SFU', 
        xlabel = 'Midnight EPBs'
        )
    
plt.subplots_adjust(wspace = 0.3)
plot_epb_and_solar_flux(ax[1])
plot_all_sectors(ax[0], time = 'year')

ax[0].text(
    0.03, 0.9, '(a)', 
    transform = ax[0].transAxes
    )

ax[1].text(
    0.03, 0.9, '(b)', 
    transform = ax[1].transAxes
    )