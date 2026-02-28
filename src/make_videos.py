import os
import matplotlib.pyplot as plt
import GOES as gs 
import datetime as dt 
from tqdm import tqdm 
import base as b 


def save_maps(ref_day, B = 'D'):
    
    in_date = ref_day.strftime('%Y\\%m')
    infile = f'{B}:\\database\\goes\\{in_date}\\'
    
    path = f'{B}:\\database\\{ref_day.month}\\'
    
    b.make_dir(path)
    files = os.listdir(infile)
       
    for fname in tqdm(files, 'Make Imagens'):
        
        plt.ioff()
        
        dn  = gs.fname2date(fname)
        
        if dn < ref_day:
            try:
                fig = gs.test_plot(infile + fname, temp = -60)
                
                FigureName = fname.split('_')[1][:-3]
                
                fig.savefig(path + FigureName, dpi = 100)
            except:
                 continue
            
            plt.clf()   
            plt.close()
            
    movie_name = ref_day.strftime('%Y%m%d')
    
    b.images_to_movie(
            path, 
            path_out = 'movies/',
            movie_name = movie_name,
            fps = 5, 
            ext = 'png'
            )



 