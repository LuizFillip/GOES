import matplotlib.pyplot as plt 
import core as c

def plot_seasonal_Ep(col = 'mean_90_110'):

    fig, ax = plt.subplots( 
        sharex = True,
        sharey = True,
        figsize = (14, 8), 
        dpi = 300
        )
        
    years = [2013, 2019]
    maks = ['s', 'o']
    labl = ['Maximum', 'Minimum']
    
    for i, year in enumerate(years):
        
        df = c.potential_energy(year)
        
        ds = df[col].resample('1M').mean()
        
        ds.index = ds.index.month
        
        ax.plot(ds, lw = 2, 
                label = f'Solar {labl[i]} - {year}',
                markersize = 20, 
                marker = maks[i], 
             
                )
    
    ax.legend(loc = 'upper right')
    ax.set(
           ylabel = 'Ep (J/Kg)', 
           xticks = np.arange(1, 13, 1),
           xlabel = 'Months')
    
    plt.show()
    return fig
