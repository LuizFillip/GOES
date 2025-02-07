import pandas as pd 
import base as b 
import numpy as np
import GEO as gg 
import datetime as dt 
from tqdm import tqdm 



b.config_labels()




    


def coord_diff_on_data(df, threshold = 2):

    df['dx0'] =  df['x0'].diff().abs()
    df['dy0'] =  df['y0'].diff().abs()
    df['dx1'] =  df['x1'].diff().abs()
    df['dy1'] =  df['y1'].diff().abs()
    
    df = df.replace(np.nan, 0)
    
    cols = ['dx0', 'dy0', 'dx1', 'dy1']
    mask = (df[cols] < 1).sum(axis=1) >= 4
    
    df_filt = df[mask].copy()
    
    rt = df_filt.index.to_series(
            ).diff().fillna(
        pd.Timedelta(seconds = 0)
        )
    
    df_filt['dtime'] =  (
        rt.dt.components['hours'] +      
        rt.dt.components['minutes'] / 60       
        )     
                   
    df_filt['group'] = (
        df_filt['dtime'] >= threshold
        ).cumsum()
    
    return df_filt.iloc[:, 4:]

def sequential_blocks(df):
    
    df_filtered = coord_diff_on_data(df)
    intervalo_max = pd.Timedelta(hours=0.5)
    
    bloco_atual = []
    blocos_sequenciais = []
    
    for i, (time, row) in enumerate(df_filtered.iterrows()):
        if i == 0 or row['time_diff'] <= intervalo_max:
            bloco_atual.append(row)
        else:
            # Se não for sequencial, salva o bloco atual e começa um novo
            if bloco_atual:
                blocos_sequenciais.append(pd.DataFrame(bloco_atual))
            bloco_atual = [row]
     

    if bloco_atual:
        blocos_sequenciais.append(pd.DataFrame(bloco_atual))
    
    for bloco in blocos_sequenciais:
        bloco.drop(columns=['time_diff'], inplace = True)
        
    return blocos_sequenciais
    



def filter_region(df, sector, year = 2013):
    '''filter region'''
    corners = gg.set_coords(year)

    xlim, ylim = corners[sector]
    
    return df.loc[
        (df['x0'] > xlim[0]) & 
        (df['x1'] < xlim[1]) & 
        (df['y0'] > ylim[0]) & 
        (df['y1'] < ylim[1])
        ]


def built_area_locator_time(df, sector):
    
    start_time = df.index.min()
    end_time = df.index.max()
    area_sum = df['area'].mean()
    time_sum = df['dtime'].sum()
    
    result = {
        'time': time_sum, 
        'area': area_sum, 
        'start': start_time, 
        'end': end_time, 
        'sector': sector
        }
    
    dn = [start_time.date()]
    
    return pd.DataFrame(result, index = dn)




def group_of_convective_storms(ds):
    
    out = []
    for sector in np.arange(-80, -40, 10):
    
        df1 = coord_diff_on_data(
            filter_region(ds, sector).copy()
            )
               
        valid_intervals = df1[df1['dtime'] < 2].groupby('group')
    
        for group_id, group_df in valid_intervals:
            
            out.append(
                built_area_locator_time(
                    group_df, sector
                    )
                )
            
    return pd.concat(out)


def run_years_convective():
    
    ds = b.load('test_goes2')
    
    ds = ds.loc[~(ds['area'] > 1000)]
    delta = dt.timedelta(days = 1)
    
    times = pd.date_range('2013-01-01', '2017-12-31')
    
    out = []
    for dn in tqdm(times):
        ds1 = ds.loc[(ds.index > dn) & 
                     (ds.index < dn + delta)]
        try:
            out.append(group_of_convective_storms(ds1))
        except:
            continue
        
    return pd.concat(out)
    
    
# df = run_years_convective()

# df.to_csv('nucleos2')

    
# df = load_tunde(infile)
# for index, row in df1.iterrows():
    
# df1['mean_90_110'].max()
# df['mean_60_90'].resample('15D').mean().plot(figsize = (15, 8))


