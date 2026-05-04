import matplotlib.pyplot as plt 
import GOES as gs 
import spectral as sp
import base as b 

lon_min=-70
lon_max=-60

lat_min=-10
lat_max = 0
year = 2017
area = 10


df = gs.nucleos_by_time(
    year=year,
    freq="12H",
    area=area,
    lon_min=lon_min,
    lon_max=lon_max,
    lat_min=lat_min,
    lat_max=lat_max,
)  


 
fig, ax = plt.subplots(
    nrows = 2, 
    sharex = True, 
    figsize = (12, 8),
    dpi = 300
    )

plt.subplots_adjust(hspace = 0.1)
df['doy'] = df.index.day_of_year + df.index.hour / 24

time = df['doy'].values
sst = df['nucleos'].values 

ax[0].plot(time, sst)

sst = b.bandpass_1d(
    sst,
    low_period = 2.2,
    high_period = 30,
    fs=1,
    order=4,
    handle_nan=True
)
 
dt = time[1] - time[0]

result = sp.compute_wavelet_analysis(
    series = sst,
    dt= dt,
    pad=1,
    dj=0.1,
    j1=7 / 0.17,
    lag1 = 0.7, 
)


sp.plot_wavelet_power_spectrum(
        ax[1], result, time
        )


ax[1].set(
    ylim = [1, 16], 
          xlabel = f'Day of Year - {year}', 
          ylabel = 'Periodos (days)')

title = (f'Latitudes: {lat_min}° to {lat_max}° |' +
         f'Longitudes: {lon_min}° to {lon_max}°')
ax[0].set(
    title = title, 
    ylabel = 'Number of Nucleos'
    )