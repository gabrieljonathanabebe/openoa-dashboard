import os
import pandas as pd
import pickle
from utils.transform_por import transform_reg_data_combined

RAW_DIR = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/raw"
OUT_DIR_SCATTER = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/processed/scatter"
OUT_DIR_FULL = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/processed/por"
os.makedirs(OUT_DIR_SCATTER, exist_ok=True)
os.makedirs(OUT_DIR_FULL, exist_ok=True)

datasets = {
    "mc_era5": ("ERA5", "era5"),
    "mc_merra2": ("MERRA2", "merra2"),
    "mc_era5_true": ("ERA5 gefiltert", "era5"),
    "mc_merra2_true": ("MERRA2 gefiltert", "merra2")
}

for base_name, (label, wind_column) in datasets.items():
    print(f"\n🔄 Starte Transformation für {label} ...")

    # Lade Grunddaten
    csv_path = os.path.join(RAW_DIR, f"{base_name}.csv")
    aggregate_path = os.path.join(RAW_DIR, f"{base_name}_aggregate.csv")
    bootstrap_path = os.path.join(RAW_DIR, f"{base_name}_bootstrap.pkl")
    non_bootstrap_path = os.path.join(RAW_DIR, f"{base_name}_non_bootstrap.pkl")

    df = pd.read_csv(csv_path)
    aggregate_df = pd.read_csv(aggregate_path, parse_dates=["time"])

    with open(bootstrap_path, "rb") as f:
        bootstrap_data = pickle.load(f)
    with open(non_bootstrap_path, "rb") as f:
        non_bootstrap_data = pickle.load(f)

    # Scatter-Daten (bootstrap / non-bootstrap)
    df_scatter = transform_reg_data_combined(
        df, aggregate_df, wind_column,
        bootstrap_list=bootstrap_data,
        non_bootstrap_list=non_bootstrap_data,
        dataset_name=label,
        mode="scatter"
    )

    out_scatter = os.path.join(OUT_DIR_SCATTER, f"mc_{label.lower().replace(' ', '_')}_scatter.csv")
    df_scatter.to_csv(out_scatter, index=False)
    print(f"✅ Scatterdaten gespeichert: {out_scatter}")

    # Vollständige Zeitreihe (modellierte Energie)
    df_full = transform_reg_data_combined(
        df, aggregate_df, wind_column,
        dataset_name=label,
        mode="full"
    )

    out_full = os.path.join(OUT_DIR_FULL, f"mc_{label.lower().replace(' ', '_')}_por.csv")
    df_full.to_csv(out_full, index=False)
    print(f"✅ Zeitreihendaten gespeichert: {out_full}")
    
    
    
    