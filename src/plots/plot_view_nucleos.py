import GOES  as gs 

import datetime as dt 
import matplotlib.pyplot as plt 
import numpy as np 



def plot_view_nucleos(
        fn,
        threshold=-40 
        ):
    
    lon, lat, temp = gs.read_gzbin(fn)
    
    threshold = -40
    
    dn = gs.fn2dn(fn)
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
        
    for _, row in nl.iterrows():
        x0, x1 = row["lon_min"], row["lon_max"]
        y0, y1 = row["lat_min"], row["lat_max"]
        
        gs.add_ellipse_from_bbox(
            ax,
            x0, x1,
            y0, y1
            )
    
        
    return fig 


 