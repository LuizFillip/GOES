import matplotlib.pyplot as plt
import GOES as gs
import base as b
import numpy as np 

def plot_correlation_ep_number_cells(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)

    fit = b.linear_fit(x, y)
    corr = np.corrcoef(x, y)[1, 0]

    ax.plot(
        x, y,
        linestyle="none",
        marker="o",
        markersize=5,
        markeredgecolor="black",
        markeredgewidth=1,
        alpha=0.8,
        label="Data",
    )

    ax.plot(
        x, fit.y_pred,
        color="red",
        lw=2,
        label="Linear fit",
    )

    ax.text(
        0.68, 0.88,
        f"r = {corr:.2f}",
        transform=ax.transAxes,
    )

    ax.legend()
    ax.set_xlabel("Number of nuclei")
    ax.set_ylabel("EP")

    return fig


def all_nucleos_for_one_height(
    year=2013,
    alt=100,
    area=30,
    ep_vls="Ep_mean",
    rolling_window=7,
    lon_min=-70,
    lon_max=-50,
    lat_min=-10,
    lat_max=0,
):
    fig, ax = plt.subplots(figsize=(12, 4), dpi=300)
    ax1 = ax.twinx()

    ep = gs.wave_avg_heights(
        year=year,
        freq="1D",
        values=ep_vls,
        lon_min=lon_min,
        lon_max=lon_max,
        lat_min=lat_min,
        lat_max=lat_max,
    )


    ep_series = ep[alt].dropna()
    ep_mean = ep_series.rolling(window=rolling_window, center=True).mean()

    ax1.scatter(
        ep_series.index, 
        ep_series.values, 
        color="b", 
        alpha=0.3, s=12
        )
    ax1.plot(ep_mean.index, ep_mean.values, lw=2, color="b")
    ax1.set_ylabel(f"{ep_vls} (J/kg)")

    b.change_axes_color(
        ax1,
        color="b",
        axis="y",
        position="right",
    )

    nuc = gs.nucleos_by_time(
        year=year,
        freq="1D",
        area=area,
        lon_min=lon_min,
        lon_max=lon_max,
        lat_min=lat_min,
        lat_max=lat_max,
    )["nucleos"]

    nuc_mean = nuc.rolling(window=rolling_window, center=True).mean()

    ax.scatter(nuc.index, nuc.values, alpha=0.3, s=12, color="k")
    ax.plot(nuc_mean.index, nuc_mean.values, lw=2, color="k")

    b.format_month_axes(ax, month_locator=1)

    ax.set(
        ylabel="Number of nuclei",
        title=f"Nuclei (area > {area}) and {ep_vls} at {alt} km",
        xlabel=f"Months ({year})",
    )

    return fig