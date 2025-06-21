import pandas as pd


def transform_reg_data(df, bootstrap_list, non_bootstrap_list, dataset_name=None):
    all_data = []

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
            print(f"⚠️ Fehler in Iteration {i}: {e}")
            continue

    if not all_data:
        raise ValueError("⚠️ Keine gültigen Daten zum Zusammenführen gefunden.")

    full_df = pd.concat(all_data, ignore_index=True)

    if dataset_name:
        print(f"✅ Transformation für {dataset_name} abgeschlossen. {len(full_df)} Zeilen erstellt.")

    return full_df