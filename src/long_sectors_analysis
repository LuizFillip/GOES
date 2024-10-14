import base as b 
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import PlasmaBubbles as pb 
import core as c

df =  b.load('olr')


# df 


# fig, ax = plt.subplots(
#     nrows = 4,
#     figsize = (18, 12),
#     sharey = True,
#     sharex = True,
#     dpi = 300)

# df.plot(ax = ax, subplots = True, 
#         ylabel = 'OLR', 
#         xlabel = 'Years')

# ds = df.resample('1M').mean()


# ds.plot(ax = ax, subplots = True, 
#                 ylabel = 'OLR', 
#                 xlabel = 'Years')

def set_avg(ds):
    count_epb = ds.groupby(ds.index.to_period('M')).agg('mean')
     
    ys = df.index[0].year
    ye = df.index[-1].year
    
    new_index = pd.date_range(
        f"{ys}-01-01", 
        f"{ye}-12-31", 
        freq = "1M")
    
    ds = count_epb.reindex(
        pd.PeriodIndex(
            new_index, 
            freq = "M"
            )
        ).replace(float('nan'), 0)
    
    ds.index = ds.index.to_timestamp()
    
    ds.columns = pd.to_numeric(ds.columns)
    return ds 

df2 = set_avg(df)

def set_epbs(col = -70):
    df = b.load('events_class2')
    
    
    df = pb.sel_typing(
              df, 
              typing = 'midnight', 
              indexes = True, 
              year = 2022
              )
    
    # df = df.loc[df['dst'] > -30]

    return c.seasonal_yearly_occurrence(
            df, 
            col = col
            )
col = -80
df = set_epbs(col )
ds = pd.concat([df[col], df2[col]], axis = 1)

plt.scatter(
    ds.iloc[:, 0],
    ds.iloc[:, 1]
    )

plt.title(col)