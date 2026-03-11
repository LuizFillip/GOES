# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:29:46 2026

@author: Luiz
"""

def plot_semi_axis(ax, e):
    xc_e, yc_e = e.center
    w_e = e.width
    h_e = e.height
    ang_e = e.angle
    
    theta = np.deg2rad(ang_e)
    
    a = h_e / 2
    b = w_e / 2
    
    # eixo maior
    x_major = [xc_e - a*np.sin(theta),
               xc_e + a*np.sin(theta)]
    y_major = [yc_e + a*np.cos(theta),
               yc_e - a*np.cos(theta)]
    
    # eixo menor
    x_minor = [xc_e - b*np.cos(theta), 
               xc_e + b*np.cos(theta)]
    y_minor = [yc_e - b*np.sin(theta), 
               yc_e + b*np.sin(theta)]
    
    ax.plot(x_major, y_major, 'k-', transform=ccrs.PlateCarree())
    ax.plot(x_minor, y_minor, 'k-', transform=ccrs.PlateCarree())

def angle_from_rectangle(lon_min, lon_max, lat_min, lat_max, descending=True):
    rect_width = lon_max - lon_min
    rect_height = lat_max - lat_min

    ang = np.degrees(np.arctan2(rect_height, rect_width))
    return -ang if descending else ang