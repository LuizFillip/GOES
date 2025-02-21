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
    
    y, x  = ds['wave'].values, ds['epb'].values
    
    ax.scatter(x, y, marker = '^', s = 150)
    
    fit = b.linear_fit(x, y)
    
    ax.plot(
        x, 
        fit.y_pred,
        lw = 2, 
        color = 'red', 
        label = 'linear fit'
        )
    
  
    r2 = fit.r2_score
    ax.text(
        0.5, 0.1, 
        f'$R^2$ = {r2}', 
        transform = ax.transAxes
        )
    
    return ax
    

def waves(stp = 'year'):
    df = b.load('GOES/data/ep_avg')
    
    df = select_sectors(
            df, 
            lat_min = -10, 
            lat_max = 10, 
            lon_min = -80, 
            lon_max = -40
            )
    
    df = df.loc[~((df['mean_90_110'] < 0) | 
                  (df['mean_90_110'] > 100))]
    
    df['month'] = df.index.month 
    df['year'] = df.index.year
    
    df = df.between_time('18:00', '05:00')
    
    df = df.groupby([stp])['mean_90_110'].mean()
    
    return df.to_frame('wave')

    
def plot_seasonal_evolution(eb, wv):
    fig, ax = plt.subplots(figsize = (14, 7), dpi = 300)
    
    ax.bar(eb.index, eb, width = 0.1)
    
    ax1 = ax.twinx()
    
    ax1.plot(wv.index, wv['mean_90_110'], lw = 2, color = 'red')

def epbs(time = 'year'):
    p = pb.BubblesPipe('events_5')
    
    ds = p.sel_type('midnight')
    
    df = p.time_group(ds, time = time)
    
    return df[[-70, -60, -50]].sum(axis = 1).to_frame('epb')


def join_data(stp):

    data = [epbs(stp), waves(stp)]
    
    return pd.concat(data, axis = 1)#.dropna()

fig, ax = plt.subplots(
    figsize = (14, 6), 
    ncols = 2,
    dpi = 300, 
    sharex = True, 
    sharey = True 
    )

plt.subplots_adjust(wspace = 0.1)

names = ['month', 'year']

for i, name in enumerate(names):
    
    plot_linear_scatter(ax[i], join_data(name))
    ax[i].set(title = name.title())
    
ax[0].set(ylabel = 'Average of Ep (J/Kg)')