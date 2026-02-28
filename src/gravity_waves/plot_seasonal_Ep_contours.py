import pandas as pd 
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
import numpy as np 
import GOES as gs
import cartopy.crs as ccrs
pd.options.mode.chained_assignment = None


def size_by_grid(df, step=1, rounding=0):

    df = df.copy()  # evita alterar o original

    # centro do núcleo
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    # bins
    lon_bins = np.arange(df["lon"].min(), df["lon"].max() + step, step)
    lat_bins = np.arange(df["lat"].min(), df["lat"].max() + step, step)

    df["lon_bin"] = pd.cut(
        df["lon"],
        bins=lon_bins,
        labels=lon_bins[:-1],
        include_lowest=True
    )

    df["lat_bin"] = pd.cut(
        df["lat"],
        bins=lat_bins,
        labels=lat_bins[:-1],
        include_lowest=True
    )

    # conversão limpa (sem warning)
    df["lon_bin"] = df["lon_bin"].astype(float).round(rounding)
    df["lat_bin"] = df["lat_bin"].astype(float).round(rounding)

    # groupby mais moderno
    event_count = (
        df.groupby(["lon_bin", "lat_bin"], observed=True)
          .size(numeric_only=True)
          .reset_index()
    )
    
    # df = df.resample(sample).size()

    return event_count




def plot_map(ax, ds):

    lat_lims = dict(min = -40, max = 20, stp = 10)
    lon_lims = dict(min = -90, max = -30, stp = 15) 
    
    gg.map_attrs(
       ax, 
       year = None, 
       lat_lims = lat_lims, 
       lon_lims = lon_lims,
       grid = False,
       degress = None
        )
    
    img = ax.pcolormesh(
        ds.columns, 
        ds.index, 
        ds.values, 
        
        vmin = 0, 
        vmax = 100,
        cmap = 'jet'
        )
    
    return img 
    

 

 

def plot_seasonal_occurrence(
        ax, 
        ds,
        step = 2, 
        values = 'mean_90_110'
        ):
    
   
    seasons = {

        'Jan - Feb': [1, 2], 
        'Mar - Apr': [3, 4], 
        'May - Jun': [5, 6], 
        'Jul - Aug': [7, 8], 
        'Sep - Oct': [9, 10], 
        'Nov - Dec': [11, 12]
    }
    '''
    Verão: Dezembro, Janeiro e Fevereiro
    Outono: Março, Abril e Maio
    Inverno: Junho, Julho e Agosto
    Primavera: Setembro, Outubro e Novembro
    '''
    seasons = {

        'December\nsolstice': [12, 1, 2], 
        'March\nequinox': [3, 4, 5], 
        'June\nsolstice': [6, 7, 8], 
        'September\nequinox': [9, 10, 11], 
    }
    
    axes = ax.flat

    for i, (key, value) in enumerate(seasons.items()):
       
        df = ds.loc[ds.index.month.isin(value)]
        
        plot_map(
            axes[i], 
            set_data(
                df, 
                step = step, 
                values = values
                )
            ) 
                    
        l = b.chars()[i]
        
        axes[i].set_title(
            f'({l}) {key}', 
            fontsize = 30
            )

        if i == 0:
            pass
        else:
            axes[i].set(
                xticklabels = [],
                xlabel = '',
                ylabel = '',
                yticklabels = []
                )
            
    return ax 

       
def plot_seasonal_Ep_contours():
     
    fig, axs = plt.subplots(
          dpi = 300, 
          ncols = 4, 
          nrows = 1, 
          figsize = (14, 12),
          subplot_kw = 
          {'projection': ccrs.PlateCarree()}
          )
    
    plt.subplots_adjust(wspace = 0.1, hspace = 0.05)
    
    ds = b.load('GOES/data/ep_all')
    
    ds = ds.between_time('18:00', '05:00')
    
    ds = gs.filter_space(
            ds, 
            x0 = -90, 
            x1 = -30, 
            y0 = -40, 
            y1 = 25
            )
    
    
    plot_seasonal_occurrence(axs, ds, step = 3)
    
    b.fig_colorbar(
            fig,
            label = 'Ep (J/Kg)',
            fontsize = 35,
            vmin = 9, 
            vmax = 14, 
            step = 1,
            orientation = "vertical", 
            anchor = (.93, 0.39, 0.022, 0.22)
            )
    
    name  = 'Seasonal gravity waves Ep averages 2013 to 2022'
    
    fig.suptitle(name, y = 0.73)
    
    return fig


 

ds = b.load("nucleos_2012_2018")   


df = ds[[ 'lon_min', 'lon_max', 'lat_min', 'lat_max']].copy()  # evita alterar o original

step = 2.5
rounding = 0
# centro do núcleo
df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

# bins
lon_bins = np.arange(df["lon"].min(), df["lon"].max() + step, step)
lat_bins = np.arange(df["lat"].min(), df["lat"].max() + step, step)

df["lon_bin"] = pd.cut(
    df["lon"], bins = lon_bins,
    labels=lon_bins[:-1],
    include_lowest=True
)

df["lat_bin"] = pd.cut(
    df["lat"], bins = lat_bins,
    labels = lat_bins[:-1],
    include_lowest = True
)

# conversão limpa (sem warning)
df["lon_bin"] = df["lon_bin"].astype(float).round(rounding)
df["lat_bin"] = df["lat_bin"].astype(float).round(rounding)


 
df = df.groupby(["lon_bin", "lat_bin"]).size().to_frame('count').reset_index()
      

df['count']  = (df['count']  / df['count'].max()) * 100

ds = pd.pivot_table(
     df, 
     columns = 'lon_bin', 
     index = 'lat_bin', 
     values = 'count'
     ).interpolate()

fig, ax = plt.subplots(
      dpi = 300, 
      # ncols = 4, 
      # nrows = 1, 
      figsize = (10,10),
      subplot_kw = 
      {'projection': ccrs.PlateCarree()}
      )


plot_map(ax, ds)