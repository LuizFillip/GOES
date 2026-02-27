import GOES  as gs 

import datetime as dt 
import matplotlib.pyplot as plt 
import numpy as np 



def plot_view_nucleos(
        lon, lat, 
        temp, dn,
        threshold=-40,
        dot_size = None
        ):
 
    nl = gs.find_nucleos(       
        lon,
        lat,
        temp,
        dn=None,
        temp_threshold=threshold,
    )
    
    
    fig, ax = gs.plot_cloud_top_temperature(
        lon, lat, temp, 
        dn = dn,  
        lat_max = 12, 
        lon_max = -30, 
        lat_min = -55, 
        lon_min = -100
        ) 
    if dot_size is not None:
        
        for _, row in nl.iterrows():
            x0, x1 = row["lon_min"], row["lon_max"]
            y0, y1 = row["lat_min"], row["lat_max"]
            
            gs.add_ellipse_from_bbox(
                ax,
                x0, x1,
                y0, y1
                )
          
           
    return fig, ax 


# --------- example usage ---------
def example_usage():
    dn = dt.datetime(2013, 2, 1)
 
    fn = gs.get_path_by_dn(dn)
    
    lon, lat, temp = gs.read_gzbin(fn)
    
    threshold = -40
    
    fig, ax = plot_view_nucleos(
        lon, lat, temp, dn,
        threshold=threshold, 
        dot_size = 5
        )
    
    
    plt.show()
 

example_usage()