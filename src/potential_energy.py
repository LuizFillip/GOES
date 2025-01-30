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

    
sample = '15D'

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

# f, ax = plt.subplots(figsize = (16, 8))
df1 = epbs(sample)

# df1 = b.load('GOES/data/ep_avg_15')


# 


#

# # ds = ds.loc[~(ds['ep'] > 10.5)]

def plot_scatter(ds):
    
    y, x = ds['ep'].values, ds['pb'].values

# plt.scatter(x_vls, y_vls)

    # fit = b.linear_fit(y, x)
    
    # plt.plot(
    #     x_vls, 
    #     fit.y_pred,
    #     lw = 2, 
    #     color = 'red'
    #     )
    
    # fit.r2_score

    coeffs = np.polyfit(x, y, 2)
    
    # Extract coefficients
    a, b, c = coeffs
    print(f"Quadratic equation: y = {a:.3f}x² + {b:.3f}x + {c:.3f}")
    
    # Generate points for plotting
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = np.polyval(coeffs, x_fit)
    
    plt.scatter(x, y, color='red', label="Data")
    plt.plot(x_fit, y_fit, label="Quadratic Fit", color="blue")
    
    y_pred = np.polyval(coeffs, x)
    
    print(r2_score(y, y_pred))
def r2_score(y, y_pred):
    ss_res = np.sum((y - y_pred) ** 2)  # Residual sum of squares
    ss_tot = np.sum((y - np.mean(y)) ** 2)  # Total sum of squares
    return 1 - (ss_res / ss_tot)

# r2

df2 = b.load('GOES/data/ep_all')


avg_results = {}

vls = df1.index

for i in range(len(vls) - 1):
    start_date = vls[i]
    end_date = vls[i + 1]
    
    subset = df2.loc[(df2.index >= start_date) & 
                      (df2.index <= end_date)]
    
    # Compute mean values for the range
    if not subset.empty:
        avg_results[start_date] = subset.mean()

# Convert dictionary to DataFrame
df_avg = pd.DataFrame(avg_results).T

ds = pd.concat([df_avg['mean_60_90'], df1], axis = 1).dropna()

ds = ds.rename(columns = {'mean_60_90': 'ep', 0: 'pb'})

ds.plot()