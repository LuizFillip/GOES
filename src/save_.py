# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:06:34 2024

@author: Luiz
"""

import os 

out = []

for file in os.listdir(infile):
    out.append(b.load(infile + file))
    
df = pd.concat(out)
