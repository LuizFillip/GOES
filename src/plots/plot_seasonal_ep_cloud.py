import pandas as pd 
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os
import numpy as np 
import GOES as gs 
import base as b 

df = b.load('test_keo')

ds = pd.pivot_table(
    df, 
    columns = df.index, 
    index =  'lat', values = 'temp') 

def plot_keo(ds):
    fig, ax = plt.subplots(dpi = 300)
    # levels = np.linspace(-100, 100, 30)
    ax.pcolormesh(
        ds.columns, 
        ds.index, 
        ds.values, 
        vmin = -100, 
        vmax = 100,
        cmap = gs.goes_cmap()
        )
    
    ax.set(ylim = [-40, 10])
    
    
# ds = df.loc[df['lat'] == -15] 

# ds['temp'].plot()

plot_keo(ds)

df 