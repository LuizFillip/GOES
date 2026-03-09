import datetime as dt
from functools import lru_cache

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Ellipse
import cartopy.crs as ccrs

import GOES as gs
import GEO as gg


# -----------------------
# Colormap (cache)
# -----------------------
@lru_cache(maxsize=8)
def goes_cmap(path="GOES/src/plots/colorbar.cpt"):
    cpt = gs.loadCPT(path)
    return cm.colors.LinearSegmentedColormap("goes_cpt", cpt)


# -----------------------
# Base map plot
# -----------------------
def plot_cloud_top_temperature(
    lon,
    lat,
    temp,
    ax=None,
    cmap_path="GOES/src/plots/colorbar.cpt",
    vmin=-100,
    vmax=100,
    lat_min=-50,
    lat_max=10,
    lat_step=10,
    lon_min=-100,
    lon_max=-30,
    lon_step=10,
    add_colorbar=True,
    cbar_label=u"Temperature (°C)",
    cbar_ticks=None,
):
    """
    Plota temperatura de topo de nuvem (pcolormesh) em Cartopy PlateCarree.
    Retorna (fig, ax, mappable, cbar).
    """
    created_fig = False
    if ax is None:
        created_fig = True
        fig, ax = plt.subplots(
            dpi=300,
            figsize=(10, 10),
            subplot_kw={"projection": ccrs.PlateCarree()},
        )
    else:
        fig = ax.figure

    lat_lims = dict(min=lat_min, max=lat_max, stp=lat_step)
    lon_lims = dict(min=lon_min, max=lon_max, stp=lon_step)

    m = ax.pcolormesh(
        lon,
        lat,
        temp,
        vmin=vmin,
        vmax=vmax,
        cmap=goes_cmap(cmap_path),
        transform=ccrs.PlateCarree(),
        shading="auto",
        zorder=1,
    )

    gg.map_attrs(
        ax,
        year=None,
        lat_lims=lat_lims,
        lon_lims=lon_lims,
        grid=False,
        degress=None,
    )

    cbar = None
    if add_colorbar:
        if cbar_ticks is None:
            step = 20
            cbar_ticks = np.arange(vmin, vmax + step, step)

        cbar = fig.colorbar(
            m,
            ax=ax,
            orientation="vertical",
            fraction=0.046,
            pad=0.02,
            ticks=cbar_ticks,
        )
        cbar.set_label(cbar_label)

    return fig, ax, m, cbar

def plot_elipses_from_catalog(ax, nl):
    for _, row in nl.iterrows():
        x0, x1 = row["lon_min"], row["lon_max"]
        y0, y1 = row["lat_min"], row["lat_max"]
        
        gs.add_ellipse_from_bbox(
            ax,
            x0, x1,
            y0, y1
            )
        
        my = (x0 + x1) / 2
        mx = (y0 + y1) / 2
        
        ax.scatter(mx, my, color = 'red')
        


def map_defout(
    figsize = (16, 12),
    ncols = 2, 
    grid = False, 
    lat_min=-50,
    lat_max=10,
    lat_step=10,
    lon_min=-100,
    lon_max=-30,
    lon_step=10,
    wspace = 0.2
     ):
    
    fig, axs = plt.subplots(
        dpi = 300, 
        ncols = ncols,
        sharex = True, 
        figsize = figsize,
        subplot_kw = {"projection": ccrs.PlateCarree()},
    )
    
    
    lats = dict(min = lat_min, max = lat_max, stp = lat_step)
    lons = dict(min = lon_min, max= lon_max, stp = lon_step)
    
    xlocs = np.arange(lons['min'], lons['max'], 4)
    ylocs = np.arange(lats['min'], lats['max'], 4)
   
    if ncols > 1:
        plt.subplots_adjust(wspace = wspace)
        for i, ax in enumerate(axs):
            gg.map_attrs(
                ax, None, 
                lat_lims = lats, 
                lon_lims = lons, 
                grid = False, 
                degress = None
                )
            if grid:
                ax.gridlines(
                    xlocs = xlocs,
                    ylocs = ylocs,
                    linewidth=1,
                    color='k',
                    linestyle='--'
                )
            
            if i !=0:
                ax.set( 
                  
                    yticklabels = [], 
                    ylabel = ''
                    )
    else:
        gg.map_attrs(
            axs, None, 
            lat_lims = lats, 
            lon_lims = lons, 
            grid = False, 
            degress = None
            )
     
    
    return fig, axs


# -----------------------
# Shapes helpers
# -----------------------
def plot_rectangle(
    ax,
    lon0,
    lon1,
    lat0,
    lat1,
   
    lw=2.5,
    color="k",
    dot_size=50,
    number=None,
    number_offset=1.0,
):
    """
    Desenha retângulo (bbox) e opcionalmente marca o centro.
    """
    x0, x1 = sorted([lon0, lon1])
    y0, y1 = sorted([lat0, lat1])

    rect = plt.Rectangle(
        (x0, y0),
        x1 - x0,
        y1 - y0,
        edgecolor=color,
        facecolor="none",
        linewidth=lw,
        transform=ccrs.PlateCarree(),
        zorder=6,
    )
    ax.add_patch(rect)

    xc = 0.5 * (x0 + x1)
    yc = 0.5 * (y0 + y1)

    if dot_size is not None:
        ax.scatter(
            xc,
            yc,
            s=dot_size,
            color="red",
            transform=ccrs.PlateCarree(),
            zorder=7,
        )

    if number is not None:
        ax.text(
            xc,
            yc + number_offset,
            str(number),
            transform=ccrs.PlateCarree(),
            zorder=8,
        )

    return rect


def add_ellipse_from_bbox(
    ax,
    lon_min,
    lon_max,
    lat_min,
    lat_max,
    angle = 0,
    shrink=1.0,
    edgecolor="k",
    linewidth=2.5,
    facecolor="none",
    zorder=7,
    center_marker=True,
    center_marker_size=20,
):
    """
    Desenha uma elipse inscrita no bbox e (opcionalmente) marca o centro.
    """
    x0, x1 = sorted([lon_min, lon_max])
    y0, y1 = sorted([lat_min, lat_max])

    xc = 0.5 * (x0 + x1)
    yc = 0.5 * (y0 + y1)

    width = (x1 - x0) * shrink
    height = (y1 - y0) * shrink

    e = Ellipse(
        (xc, yc),
        width=width,
        height=height,
        angle=angle,
        edgecolor=edgecolor,
        facecolor=facecolor,
        linewidth=linewidth,
        transform=ccrs.PlateCarree(),
        zorder=zorder,
    )
    ax.add_patch(e)

    if center_marker:
        ax.scatter(
            xc,
            yc,
            s=center_marker_size,
            color="red",
            transform=ccrs.PlateCarree(),
            zorder=zorder + 1,
        )

    return e


# -----------------------
# Full view
# -----------------------
def plot_view_nucleos(
    dn,
    ax=None,
    threshold=-40,
    detect=True,
    ellipse=True,
    cmap_path="GOES/src/plots/colorbar.cpt",
    title = False
):
    """
    Lê GOES do dia dn, plota temperatura e (opcional) desenha nucleos detectados.
    Retorna (fig, ax, nl).
    """
    fn = gs.get_path_by_dn(dn)
    lon, lat, temp = gs.read_gzbin(fn)

    nl = gs.find_nucleos(
        lon,
        lat,
        temp,
        dn=None,
        temp_threshold=threshold,
    )

    fig, ax, m, cbar = plot_cloud_top_temperature(
        lon,
        lat,
        temp,
        ax=ax,
        cmap_path=cmap_path,
        lat_max=12,
        lon_max=-30,
        lat_min=-55,
        lon_min=-100,
        add_colorbar=True,
        cbar_label=u"Temperature (°C)",
    )

    if detect and not nl.empty:
        for _, row in nl.iterrows():
            if ellipse:
                add_ellipse_from_bbox(
                    ax,
                    row["lon_min"], row["lon_max"],
                    row["lat_min"], row["lat_max"],
                    edgecolor="k",
                )
            else:
                plot_rectangle(
                    ax,
                    row["lon_min"], row["lon_max"],
                    row["lat_min"], row["lat_max"],
                    color="k",
                )

    # título opcional
    if title:
        ax.set_title(dn.strftime("%Y-%m-%d %H:%M UTC") 
                     if hasattr(dn, "strftime") else str(dn))

    return fig, ax, nl


def example():
    dn = dt.datetime(2013, 1, 1)
    
    # fig, ax = plt.subplots(
    #     dpi=300,
    #     figsize=(10, 10),
    #     subplot_kw={"projection": ccrs.PlateCarree()},
    # )
    ax = None 
    plot_view_nucleos(dn, ax=ax, threshold=-40)
    plt.show()