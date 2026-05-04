import base as b 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import GOES as gs
import GEO as gg 





#%%%%
import datetime as dt 
df = b.load('GOES/data/nucleos_40/2013')

nl = df.loc[df.index.date == dt.date(2013, 1, 1)]

def plot_track_paths(nl):
    fig, ax = plt.subplots(
            dpi=300,
            figsize=(10, 10),
            subplot_kw={"projection": ccrs.PlateCarree()},
        )
     
     
    
    lat_lims = dict(min=-60, max=20, stp=10)
    lon_lims = dict(min=-90, max=-30, stp=10)
    
    
    gg.map_attrs(
         ax,
         year=None,
         lat_lims=lat_lims,
         lon_lims=lon_lims,
         grid=False,
         degress=None,
     )
    
    for _, row in nl.iterrows():
       
        gs.plot_rectangle(
            ax,
            row["lon_min"], row["lon_max"],
            row["lat_min"], row["lat_max"],
            color="k",
        )
    
    return fig

nl = nl.loc[nl['area'] >  200]
fig = plot_track_paths(nl)

nl['area']