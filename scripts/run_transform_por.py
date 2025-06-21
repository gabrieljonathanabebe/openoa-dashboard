import os
import pandas as pd
import pickle
from utils.transform_por import transform_reg_data

RAW_DIR = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/raw"
OUT_DIR = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/processed/por"
os.makedirs(OUT_DIR, exist_ok=True)

datasets = {
    "mc_era5": "era5",
    "mc_merra2": "merra2",
    "mc_combined": "combined",
    "mc_era5_true": "era5_filtered",
    "mc_merra2_true": "merra2_filtered"
}

for base_name, label in datasets.items():
    csv_path = os.path.join(RAW_DIR, f"{base_name}.csv")
    bootstrap_path = os.path.join(RAW_DIR, f"{base_name}_bootstrap.pkl")
    non_bootstrap_path = os.path.join(RAW_DIR, f"{base_name}_non_bootstrap.pkl")

    df = pd.read_csv(csv_path)

    with open(bootstrap_path, "rb") as f:
        bootstrap_data = pickle.load(f)
    with open(non_bootstrap_path, "rb") as f:
        non_bootstrap_data = pickle.load(f)

    transformed_df_por = transform_reg_data(df, bootstrap_data, non_bootstrap_data, dataset_name=label)

    out_path = os.path.join(OUT_DIR, f"mc_{label}_por.csv")
    transformed_df_por.to_csv(out_path, index=False)
    print(f"✅ Gespeichert: {out_path}")