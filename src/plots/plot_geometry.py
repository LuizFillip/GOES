import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
import cartopy.crs as ccrs

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
    fontsize = 30
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
            fontsize = fontsize
        )

    return rect

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

def angle_from_rectangle(
        lon_min, lon_max,
        lat_min, lat_max, descending=True
        ):
    rect_width = lon_max - lon_min
    rect_height = lat_max - lat_min

    ang = np.degrees(np.arctan2(rect_height, rect_width))
    return -ang if descending else ang