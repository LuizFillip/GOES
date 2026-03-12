import pandas as pd 


def filter_space(
    df: pd.DataFrame,
    lon_min: float = -50,
    lon_max: float = -40,
    lat_min: float = -10,
    lat_max: float = 10,
) -> pd.DataFrame:
    """Filtra o DataFrame por limites espaciais."""
    mask = (
        df["lon"].between(lon_min, lon_max, inclusive="neither")
        & df["lat"].between(lat_min, lat_max, inclusive="neither")
    )
    return df.loc[mask].copy()
