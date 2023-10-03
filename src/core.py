# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:59:32 2023

@author: Luiz
"""

import xarray as xr
import numpy as np
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib import ticker, cm
import time 
import cartopy.io.img_tiles as cimgt



# Carregue seus dados binários aqui (depende do formato)
def read_gzbin(f_name, threshold):
    # import necessary libraries
    import numpy as np
    import gzip
    from datetime import datetime
    
    # extract date and time from file name
    date_str = f_name[-15:-3]
    date_obj = datetime.strptime(date_str, '%Y%m%d%H%M')#%S
    
    # read binary data from gzip-compressed file
    with gzip.open(f_name, 'rb') as f:
        uncompressed_data = f.read()
        dados_binarios = np.frombuffer(uncompressed_data, dtype=np.int16)

        
        # reshape binary data into a 2D numpy array
        imageSize = [1800,1800]
        dados_binarios = dados_binarios.reshape(imageSize)
        
        # Define x and y positions
        dlon=np.arange(dados_binarios.shape[1]) * 0.04 - 100
        dlat=np.arange(dados_binarios.shape[0]) * 0.04 - 50
        
        
        # return the 2D numpy array, dlon, dlat, and date_obj
        return dados_binarios, dlon, dlat, date_obj


caminho = 'C:/2023/Beckup_note/ANDERSON/PCI_D_inpe_2023\
/mapas_temp_nuvem_python/03-06-2005-goes12_ch4/'                              

# f_name='gcr.050602.0200_0200g.ch4'
nome = 'S10216956_200506020330.gz'

f_name = caminho+nome

saida = caminho 

#Deletes values higher than -65 celcius degress
threshold = 0. 
data, dlon, dlat, date_obj = read_gzbin(f_name, threshold)
###====================================================================