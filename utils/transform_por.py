import pandas as pd

def transform_reg_data_combined(df, aggregate_df, wind_column,
                                 bootstrap_list=None, non_bootstrap_list=None,
                                 dataset_name=None, mode="scatter"):
    """
    Kombinierte Transformationsfunktion für:
    - scatter: Bootstrap & Non-Bootstrap Punkte je Iteration
    - full: Anwendung des Modells auf komplette Zeitreihe

    Parameters:
        df (pd.DataFrame): Regressionsmetriken mit slope, intercept etc.
        aggregate_df (pd.DataFrame): Zeitreihe mit Winddaten & tatsächlicher Energie
        wind_column (str): Name der Windspalte im aggregate_df (z. B. "era5")
        bootstrap_list (List[pd.DataFrame]): Liste mit Bootstrap-DFs (nur bei mode="scatter")
        non_bootstrap_list (List[pd.DataFrame]): Liste mit Non-Bootstrap-DFs
        dataset_name (str): Für Logging und Rückverfolgung
        mode (str): "scatter" oder "full"

    Returns:
        pd.DataFrame: Transformiertes Langformat-DF
    """
    all_data = []

    if mode not in ["scatter", "full"]:
        raise ValueError("Ungültiger Modus: 'mode' muss 'scatter' oder 'full' sein.")

    if mode == "scatter":
        if not bootstrap_list or not non_bootstrap_list:
            raise ValueError("Für 'scatter' müssen bootstrap_list & non_bootstrap_list übergeben werden.")

        for i in range(len(df)):
            try:
                b_raw = bootstrap_list[i].reset_index()
                nb_raw = non_bootstrap_list[i].reset_index()

                b_raw.columns = ['time', 'wind_speed', 'energy']
                nb_raw.columns = ['time', 'wind_speed', 'energy']

                metrics = {
                    "iteration": i,
                    "slope": df.loc[i, "slope"],
                    "intercept": df.loc[i, "intercept"],
                    "mse": df.loc[i, "mse"],
                    "r2": df.loc[i, "r2"],
                    "yearly_bias": df.loc[i, "yearly_bias"]
                }

                for key, value in metrics.items():
                    b_raw[key] = value
                    nb_raw[key] = value

                b_raw["source"] = "bootstrap"
                nb_raw["source"] = "non-bootstrap"

                all_data.extend([b_raw, nb_raw])
            except Exception as e:
                print(f"Fehler in Iteration {i} (scatter): {e}")
                continue

    elif mode == "full":
        if wind_column not in aggregate_df.columns:
            raise ValueError(f"Spalte '{wind_column}' nicht in aggregate_df gefunden!")

        for i in range(len(df)):
            try:
                slope = df.loc[i, "slope"]
                intercept = df.loc[i, "intercept"]

                metrics = {
                    "iteration": i,
                    "slope": slope,
                    "intercept": intercept,
                    "r2": df.loc[i, "r2"],
                    "mse": df.loc[i, "mse"],
                    "yearly_bias": df.loc[i, "yearly_bias"]
                }

                iter_df = aggregate_df[["time", "gross_energy_gwh", wind_column]].copy()
                iter_df = iter_df.rename(columns={wind_column: "wind_speed"})
                iter_df["pred_energy"] = slope * iter_df["wind_speed"] + intercept

                for key, value in metrics.items():
                    iter_df[key] = value

                all_data.append(iter_df)
            except Exception as e:
                print(f"Fehler in Iteration {i} (full): {e}")
                continue

    if not all_data:
        raise ValueError("Keine gültigen Daten zum Zusammenführen gefunden.")

    full_df = pd.concat(all_data, ignore_index=True)
    full_df["time"] = pd.to_datetime(full_df["time"])
    full_df["dataset"] = dataset_name

    print(f"Transformation ({mode}) für {dataset_name} abgeschlossen. {len(full_df)} Zeilen erstellt.")
    return full_df

