import pandas as pd 
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os
import numpy as np 
import GOES as gs 
import base as b 

b.config_labels(fontsize = 25)

pathfile = r"F:/SABER_ALL_DATA/SABER_PROCESS_EP_DAILY_2024/Trabalho_Luiz/Plots/"  




lon_min = -80
lon_max = -40
lat_min = -50
lat_max = 20






def plot_seasonal(df, ds, title):

    fig, ax = plt.subplots(
          dpi = 300, 
          figsize = (12, 8)
          )
        
    sdf = gaussian_filter(df, sigma = 1)

    ax.plot(
        df.index,
        sdf, 
        lw = 3, 
        color = 'blue'
        )

    ax.set(
        ylim = [0, 100], 
        ylabel = r'Convective activity (%)',
        xlabel = 'Years'
        )
    
    
    ax1 = ax.twinx()
    sds = gaussian_filter(ds, sigma = 1)
    
    ax1.plot(ds.index, sds, lw = 3, color = 'red')
    
    io_2 = f': Lat = {lat_min}/{lat_max}\n'
    io_1 = f'Lon = {lon_min}/{lon_max}'
    
    ax1.set(
        title = title.title() + io_1 + io_2,
        ylabel = 'GW potential energy (J/Kg)', 
        xlabel = 'Years'
        )
    
    con_ds = pd.concat([ds, df], axis = 1).dropna()

    x, y = con_ds.iloc[:, 0].values, con_ds.iloc[:, 1].values
    correlation = np.corrcoef(x, y)[0, 1]
    corr_text = f'Correlation: {correlation:.3f}'
    
    ax.text(
         0.95, 0.05, 
         corr_text, 
         transform=ax.transAxes, 
         fontsize=35, 
         verticalalignment='bottom', 
         horizontalalignment='right'
     )
    return fig

def save_figures(fig, output_path):
     
     plt.tight_layout()
     plt.savefig(output_path)
     plt.close(fig)
     
     return None 

def get_couples(col, sample = 'M'):
    
    out_1 = []
    out_2 = []
    
    for year in range(2013, 2023, 1):
        out_1.append(gs.load_nucleos(year))
        out_2.append(gs.potential_energy(year)[col])
        
    
    return pd.concat(out_1), pd.concat(out_2)



cols = ['mean_20_30', 'mean_30_40', 
        'mean_40_50', 'mean_50_60', 
        'mean_60_70', 'mean_70_80', 
        'mean_80_90', 'mean_90_100', 
        'mean_100_110']

save = False 

cols = ['mean_20_60', 'mean_60_90', 'mean_90_110']

def plot_figures_by_col(cols):
    
    for i, col in enumerate(cols):
        df, ds = get_couples(col)
        fig = plot_seasonal(df, ds, title = col)
        
        if save:
            output_path = os.path.join(pathfile, f"fig_{i}.png")
            save_figures(fig, output_path)

col = 'mean_90_110'
# col = 'mean_60_90'
# df, ds = get_couples(col)
# # fig = plot_seasonal(df, ds, title = col)

# df 

year = 2019
ds = gs.load_nucleos(year)

ds