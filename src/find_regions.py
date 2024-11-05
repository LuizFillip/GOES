import numpy as np
import matplotlib.pyplot as plt
import GOES as gs 


def plot_data_foo(fname):
    ds = gs.CloudyTemperature(fname)
    data = ds.data[::-1]
    lons = ds.lon 
    lats = ds.lat
    
    ptc = gs.plotTopCloud(data, lons, lats)
    
    ptc.add_map()
    ptc.colorbar()
    
    fig, ax = ptc.figure_axes 
    
    data = np.where(data > -60, np.nan, data)
    
    gs.find_nucleos(
            data, 
            lons, 
            lats[::-1],
            ax,
            area_treshold = 60,
            step = 0.5
            )
    
    ax.set(title = gs.fname2date(fname))
    return fig 
    

def save_maps():
    path = 'E:\\database\\nucleos\\'
    
    ref_day = dt.datetime(2013, 1, 5)
    files = load_files(ref_day)
    
    for fname in tqdm(files, 'saving'):
        
        plt.ioff()
    
        dn = fname2date(fname)
        
        fig = plot_data_foo(fname)
        
        FigureName = dn.strftime('%Y%m%d%H%M')
        
        fig.savefig(path + FigureName, dpi = 100)
        
        plt.clf()   
        plt.close()
