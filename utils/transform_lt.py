import numpy as np
import pandas as pd
import ast  # Für sicheres Parsen von Strings zu Listen

def transform_energy_wind_data(df, dataset_name=None):
    data = []

    for iteration in range(len(df)):
        try:
            # Sicheres Parsen
            energy_raw = df.iloc[iteration]["yearly_gross_energy"]
            wind_raw = df.iloc[iteration]["yearly_wind_speeds"]

            # Konvertiere, wenn nötig, von String zu Liste
            if isinstance(energy_raw, str):
                energy_values = ast.literal_eval(energy_raw)
            else:
                energy_values = energy_raw

            if isinstance(wind_raw, str):
                wind_values = ast.literal_eval(wind_raw)
            else:
                wind_values = wind_raw

            wind_values = np.array(wind_values).flatten()

            slope_value = df.iloc[iteration]["slope"]
            intercept_value = df.iloc[iteration]["intercept"]
            bias_value = df.iloc[iteration]["yearly_bias"]

            num_years = len(energy_values)

            for year_index in range(num_years):
                wind_speed = wind_values[num_years - 1 - year_index]
                if isinstance(wind_speed, (list, np.ndarray)):
                    wind_speed = wind_speed[0]

                data.append({
                    "Iteration": iteration,
                    "year": year_index + 1,
                    "energy": energy_values[num_years - 1 - year_index],
                    "wind": float(wind_speed),
                    "slope": slope_value,
                    "intercept": intercept_value,
                    "yearly_bias": bias_value,
                })

        except Exception as e:
            print(f"⚠️  Fehler bei Iteration {iteration}: {e}")
            continue  # Überspringe diese Zeile bei Fehlern

    transformed_df = pd.DataFrame(data)

    if dataset_name:
        print(f"✅ Transformation für {dataset_name} abgeschlossen. {len(transformed_df)} Zeilen erstellt.")

    return transformed_df