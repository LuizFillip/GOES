import matplotlib.pyplot as plt 
import numpy as np
import base as b 

year = 2012 
path = f'D:\\database\\SABER\\ep\\{year}'
df = b.load(path)

#%%%%
import pandas as pd 

ds = pd.pivot_table(
    df, columns = 'alt', index = df.index, values = 'Ep_max')

ds = ds.resample('1D').mean().T
from scipy.ndimage import gaussian_filter

grid = ds.values
smooth = gaussian_filter(grid, sigma=1.5)

plt.pcolormesh(
    ds.columns, 
    ds.index, 
    smooth, 
    cmap = 'plasma'
    )