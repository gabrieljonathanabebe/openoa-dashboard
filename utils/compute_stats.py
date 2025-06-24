from data.config import TIMESERIES_DATAFRAMES


def compute_normalized_timeseries():
    era5_ts = TIMESERIES_DATAFRAMES["ERA5"].copy()
    merra2_ts = TIMESERIES_DATAFRAMES["MERRA2"].copy()
    
    era5_ts["rolling"] = era5_ts["era5"].rolling(window=12, center=True).mean()
    merra2_ts["rolling"] = merra2_ts["merra2"].rolling(window=12, center=True).mean()
    
    era5_ts["norm"] = era5_ts["rolling"] / era5_ts["rolling"].mean()
    merra2_ts["norm"] = merra2_ts["rolling"] / merra2_ts["rolling"].mean()
    
    return era5_ts, merra2_ts


def get_aep_stats(dataframes):
    stats = {
        "labels": [],
        "mean_aep": [],
        "aep_cv": []
    }
    
    for label, df in dataframes.items():
        stats["labels"].append(label)
        mean = df["aep_final"].mean()
        std = df["aep_final"].std()
        stats["mean_aep"].append(mean)
        stats["aep_cv"].append(std / mean)
    
    return stats


def filter_dataframes_by_labels(dataframes, selected_labels):    
    filtered = {}
    
    for label, df in dataframes.items():
        if label in selected_labels:
            filtered[label]=df
            
    return filtered


def compute_lt_metrics(df, column ="energy"):
    df_grouped = df.groupby("year", as_index=False).agg(mean_value=(column, "mean"))
    df_grouped = df_grouped.sort_values("year")
    
    years = df_grouped["year"]
    non_cum_mean = df_grouped["mean_value"]
    
    cum_mean = df_grouped["mean_value"].expanding().mean()
    cum_std = df_grouped["mean_value"].expanding().std()
    cum_cv = (cum_std / cum_mean) * 100
    
    return years, non_cum_mean, cum_mean, cum_cv


def filter_lt_data(df, selected_years):
    return df[df["year"].isin(selected_years)]



def get_iteration(df, metric, method="max"):  
    if df.empty or metric not in df.columns:
        raise ValueError("Ungültige Dataframes oder Metrik nicht gefunden.")
        
    method = method.lower()
    
    if method == "max":
        target_value = df[metric].max()
    elif method == "min":
        target_value = df[metric].min()
    elif method == "median":
        target_value = df[metric].median()
    elif method == "q1":
        target_value = df[metric].quantile(0.25)
    elif method == "q3":
        target_value = df[metric].quantile(0.75)
    else:
        raise ValueError(f"Unbekannte Methode: {method}")
    
    closest_index = (df[metric] - target_value).abs().idxmin()

    return df.loc[closest_index, "iteration"]
        





















