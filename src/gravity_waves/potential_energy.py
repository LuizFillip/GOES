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


def epbs(sample = '1M'):
    
    ds = b.load('database/epbs/events_class2')

    df = pb.sel_typing(
            ds, 
            typing = 'midnight', 
            indexes = False, 
            year = 2022
            )

    # df['sum'] = df[[-70]].sum(axis = 1)
    

    df = df.loc[df.index.year <= 2022]
    
    return df.resample(sample).size()

    

def save_avg_ep():
    out = []
    for year in range(2013, 2023):
    
        df = potential_energy(year = year)
        
        # df =  limits(
        #         df, 
        #         x0 = -70, 
        #         x1 = -40, 
        #         y0 = -20, 
        #         y1 = 10
        #         )
        
        out.append(df)
        
    df1 = pd.concat(out)
    df1.to_csv('GOES/data/ep_avg')

# save_avg_ep()

def plot_scatter_quadratic(ds):
    
    def r2_score(y, y_pred):
        ss_res = np.sum((y - y_pred) ** 2)  
        ss_tot = np.sum((y - np.mean(y)) ** 2)  
        return 1 - (ss_res / ss_tot)
    
    y, x= ds['ep'].values, ds['pb'].values

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


def plot_linear_scatter(ds):
    
    fig, ax = plt.subplots(dpi = 300)
    
   
    y, x  = ds['wave'].values, ds['epb'].values
    
    ax.scatter(x, y)
    
    fit = b.linear_fit(x, y)
    
    ax.plot(
        x, 
        fit.y_pred,
        lw = 2, 
        color = 'red', 
        label = 'linear fit'
        )
    
    ax.set(
        ylabel = 'Ep (J/k)', 
        xlabel = 'Midnight EPBs'
        )
    ax.text(
        0.1, 0.8, 
            fit.r2_score, 
            transform = ax.transAxes)
    
def plot_seasonal_corr(ds):  
    f, ax = plt.subplots(figsize = (12, 6))
    
    ax.bar(ds.index, ds['pb'], width = 12)
    
    ax1 = ax.twinx()
    
    # ax1.plot(ds['ep'], color = 'red')



def join_epb_waves(
        sample = '15D',
        col = 'mean_90_110'
        ):
    df1 = epbs(sample)
    
    df2 = b.load('GOES/data/ep_avg')
    
    df2 = select_sectors(
            df2, 
            lat_min = -20, 
            lat_max = 0, 
            lon_min = -70, 
            lon_max = -50
            )
    
    df2 = df2.between_time('20:00', '05:00')
    
    df2 = get_averages_from_data(df2, df1)

    ds = pd.concat([df2[col], df1], axis = 1).dropna()
    
    ds = ds.rename(
        columns = {col: 'ep', 0: 'pb'}
        )
    
    return ds 



cols = ['mean_20_60', 'mean_60_90', 'mean_90_110']

def bubbles(stp = 'year'):
    ds = b.load('database/epbs/events_class2')
    
    ds = pb.sel_typing(
             ds, 
             typing = 'midnight', 
             indexes = False, 
             year = 2022
             )
     

    ds['month'] = ds.index.month
    ds['year'] = ds.index.year
    cols = [-70, -60, -50]
    
    ds = ds.groupby(stp)[cols].sum().sum(axis = 1)
    
    return ds.to_frame('epb')


def waves(col, stp = 'year'):
    df = b.load('GOES/data/ep_avg')
    
    df = select_sectors(
            df, 
            lat_min = -30, 
            lat_max = 10, 
            lon_min = -70, 
            lon_max = -40
            )
    
    df['month'] = df.index.month
    df['year'] = df.index.year

    df = df.groupby(stp)[col].mean()
    
    df = df.to_frame('wave')
    return df

col = 'mean_90_110'
col = 'mean_60_90'
col = 'mean_20_60' 


data = [bubbles(), waves(col)]

ds = pd.concat(data, axis = 1).dropna()

plot_linear_scatter(ds)

ds