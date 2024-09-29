import base as b 

df =  b.load('GOES/data/OLR_avg')


df = df.resample('15D').mean()

df.plot(figsize = (12, 6), subplots = True)
