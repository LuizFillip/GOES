import xarray as xr


def dataset_to_frame(fname):
    
    ds = xr.open_dataset(fname)
    
    data = (ds['Band1'].values / 100) * -1
    
    lat = ds.lat.values
    lon = ds.lon.values
    
    # ax = gs.map_attrs(lon, lat, data)
    
    
    
    nlons, nlats, grid = grid_mean(
        lon, lat, data, 
        grid_size = 100
        )
    
    ns = ['lon', 'lat', 'temp']
    
    df = pd.DataFrame(
        structured_data(nlons, nlats, grid), 
        columns = ns
        )
    
    df['date'] = fname2date(fname)
    
 #   ax = gs.map_attrs(nlons, nlats, grid)

    # find_storms(ax, df)
    return df 

def find_storms(ax, ds):
        
        
    index = ds.index.values
    
    out = []
    
    for i in range(len(ds) - 1):
        
        idx = index[i + 1] - index[i]
        
        if idx > 100:
            
            out.append(index[i + 1])
            
            
            
    vls = ds.loc[ds.index == out[0]]
    
    if vls['lon'].min() == vls['lon'].max():
        
        clon, clat = gg.plot_square_area(
                ax, 
                lat_min = vls['lat'].min(), 
                lon_min = vls['lon'].min(),
                lat_max = None, 
                lon_max = None, 
                radius = 5
                )
    
    # ds = ds.loc[~(ds.index == vls.index[0])]
    
    
    # clon, clat = gg.plot_square_area(
    #         ax, 
    #         lat_min = ds['lat'].min(), 
    #         lon_min = ds['lon'].min(),
    #         lat_max = ds['lat'].max(), 
    #         lon_max = ds['lon'].max(), 
    #         radius = 10
    #         )



def grid_mean(lon, lat, data, grid_size = 100):
    
    num_grids_x = data.shape[0] // grid_size
    num_grids_y = data.shape[1] // grid_size

    grid_means = np.zeros((num_grids_x, num_grids_y))

    new_lats = np.zeros(num_grids_y)
    new_lons = np.zeros(num_grids_x)


    for i in range(num_grids_x):
        
        new_lons[i] = lon[
            i * grid_size:(i + 1) * grid_size
            ].mean()
        new_lats[i] = lat[
            i * grid_size:(i + 1) * grid_size
            ].mean()
        
        for j in range(num_grids_y):
            
            
            grid = data[i * grid_size:(i + 1) * grid_size, 
                        j * grid_size:(j + 1) * grid_size]
            
            grid_mean = np.mean(grid)
            grid_means[i, j] = grid_mean

    return new_lons, new_lats, grid_means


def structured_data(nlons, nlats, grid):
    x, y = np.meshgrid(nlons, nlats)
    
    x = x.reshape(-1)
    y = y.reshape(-1)
    grid_means = grid.reshape(-1)
    
    return np.column_stack((x, y, grid_means))

def recover_dataset(structured_data):
    
    ns = ['lon', 'lat', 'temp']
    df = pd.DataFrame(
        structured_data, 
        columns = ns
        )
    
    return pd.pivot_table(
        df, 
        columns = ns[0], 
        index = ns[1], 
        values = ns[2]
        )
