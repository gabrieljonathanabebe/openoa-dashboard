import os
import pandas as pd
from utils.transform_lt import transform_energy_wind_data

RAW_DIR = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/raw"
OUT_DIR = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/processed/longterm"
os.makedirs(OUT_DIR, exist_ok=True)

# Mapping von CSV-Dateien zu neuen Namen
datasets = {
    "mc_era5.csv": "era5",
    "mc_merra2.csv": "merra2",
    "mc_combined.csv": "combined",
    "mc_era5_true.csv": "era5_filtered",
    "mc_merra2_true.csv": "merra2_filtered"
}

for filename, label in datasets.items():
    raw_path = os.path.join(RAW_DIR, filename)
    df = pd.read_csv(raw_path)

    df_transformed = transform_energy_wind_data(df, dataset_name=label)

    out_path = os.path.join(OUT_DIR, f"mc_{label}_lt.csv")
    df_transformed.to_csv(out_path, index=False)

    print(f"Gespeichert: {out_path}")