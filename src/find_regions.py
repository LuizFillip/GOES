import os
import matplotlib.pyplot as plt
import GOES as gs 
import datetime as dt 
from tqdm import tqdm 
import base as b 


def save_maps(ref_day):
    path = 'E:\\database\\nucleos\\'
    
    infile = 'E:\\database\\goes\\2019\\04\\'
   
    files = os.listdir(infile)
       
    for fname in tqdm(files, 'saving'):
        
        plt.ioff()
            
        fig = gs.test_plot(infile + fname, temp = -40)
        
        FigureName = fname.split('_')[1][:-3]
        
        fig.savefig(path + FigureName, dpi = 100)
        
        plt.clf()   
        plt.close()
        

    
    b.images_to_movie(
            path, 
            path_out = '',
            movie_name = 'goes',
            fps = 5, 
            ext = 'png'
            )



# ref_day = dt.datetime(2019, 4, 1)

# save_maps(ref_day)