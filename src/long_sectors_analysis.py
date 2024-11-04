import base as b 
import numpy as np 
import pandas as pd
import GEO as gg
import datetime as dt


df = b.load('nucleos')

df['start'] = pd.to_datetime(df['start'])

df = df.loc[
    (df['start'].dt.time < dt.time(6, 0)) |
    (df['start'].dt.time > dt.time(21, 0)) |
    (df['area'] > 20)
            ]

df['month'] = df.index.month


ds = df.groupby(
    ['month', 'sector']
    ).size().reset_index(name='occs')

ds = pd.pivot_table(
    ds, 
    columns = 'sector', 
    index = 'month', 
    values = 'occs'
    )


ds.plot(kind = 'bar', figsize = (12, 8))


df 