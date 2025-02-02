import pandas as pd
import base as b 
import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import numpy as np 

path_ep = 'GOES/data/Ep/'

def limits(
        df, 
           x0 = -80, x1 = -40, 
           y0 = -10, y1 = 0):
    return  df.loc[
        ((df['lon'] >= x0) & (df['lon'] < x1)) &
        ((df['lat'] >= y0) & (df['lat'] <= y1))
        ]


def potential_energy(year = 2019):
    
    df = pd.read_csv(f'{path_ep}{year}', sep = '\s+')

    df.index = pd.to_datetime(
        df['Date'] + ' ' + 
        df[['Hour', 'Minute', 'Second']
           ].astype(str).agg(':'.join, axis=1))
    
    df = df.drop(
        columns = [
        'Year', 'DOY', 'Date', 
        'Hour', 'Minute', 'Second']
        )
    
    df = df.rename(
        columns = {'Lon': 'lon', 
                   'Lat': 'lat'}
        )
    return df

def epbs(sample = '1M'):
    
    ds = b.load('database/epbs/events_class2')

    df = pb.sel_typing(
            ds, 
            typing = 'midnight', 
            indexes = False, 
            year = 2022
            )

    df['sum'] = df[[-50, -60, -70]].sum(axis = 1)

    df = df.loc[df.index.year <= 2022]
    
    return df.resample(sample).size()

    

def save_avg_ep():
    out = []
    for year in range(2013, 2023):
    
        df = potential_energy(year = year)
        
        df =  limits(
                df, 
                x0 = -70, 
                x1 = -40, 
                y0 = -20, 
                y1 = 10
                )
        
        out.append(df)
        
    df1 = pd.concat(out)
    df1.to_csv('GOES/data/ep_avg_15')



def plot_scatter_quadratic(ds):
    
    def r2_score(y, y_pred):
        ss_res = np.sum((y - y_pred) ** 2)  
        ss_tot = np.sum((y - np.mean(y)) ** 2)  
        return 1 - (ss_res / ss_tot)
    
    x, y = ds['ep'].values, ds['pb'].values

    coeffs = np.polyfit(x, y, 2)
    
    # Extract coefficients
    a, b, c = coeffs
    print(f"Quadratic equation: y = {a:.3f}x² + {b:.3f}x + {c:.3f}")
    
    # Generate points for plotting
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = np.polyval(coeffs, x_fit)
    
    plt.scatter(x, y, color='k', label="Data")
    plt.plot(x_fit, y_fit, label="Quadratic Fit", color="r")
    
    y_pred = np.polyval(coeffs, x)
    
    print(r2_score(y, y_pred))

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
    
    mean = ds.groupby("pb")["ep"].mean()
    print(mean)
    y, x  = ds['ep'].values, ds['pb'].values
    
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
        xlabel = 'Midnight EPBs', 
        xlim = [-1, 15], 
        ylim = [8, 15]
        )
    
    print(fit.r2_score) 
    
def plot_seasonal_corr():  
    f, ax = plt.subplots(figsize = (12, 6))
    
    ax.plot(ds['pb'])
    
    ax1 = ax.twinx()
    
    ax1.plot(ds['ep'], color = 'red')

#

sample = '15D'
df1 = epbs(sample)

df2 = b.load('GOES/data/ep_all')

df2 = df2.between_time('18:00', '05:00')

df2 = get_averages_from_data(df2, df1)

col = 'mean_90_110'
# col = 'mean_60_90'
# col = 'mean_20_60'
ds = pd.concat([df2[col], df1], axis = 1).dropna()

ds = ds.rename(columns = {col: 'ep', 0: 'pb'})

plot_linear_scatter(ds)

# plot_scatter_quadratic(ds)