from openoa.analysis.aep import MonteCarloAEP
import project_ENGIE
import pandas as pd
import os

# Projekt laden
project = project_ENGIE.prepare('./data/la_haute_borne', use_cleansed=False)

# Analyseobjekt für ERA5 erzeugen
pa_era5 = MonteCarloAEP(project, reanalysis_products=["era5"], outlier_detection=False)
pa_era5.run(num_sim=50, reanalysis_products=["era5"])

# Zeitreihe extrahieren (aus _reanalysis_aggregate)
df_era5 = pa_era5._reanalysis_aggregate.reset_index().rename(columns={"index": "Date"})

# Export als CSV
outdir = "/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/raw"
os.makedirs(outdir, exist_ok=True)
df_era5.to_csv(os.path.join(outdir, "era5_timeseries.csv"), index=False)
print("✅ ERA5-Zeitreihe gespeichert.")

# Optional auch für MERRA2:
pa_merra2 = MonteCarloAEP(project, reanalysis_products=["merra2"], outlier_detection=False)
pa_merra2.run(num_sim=50, reanalysis_products=["merra2"])
df_merra2 = pa_merra2._reanalysis_aggregate.reset_index().rename(columns={"index": "Date"})
df_merra2.to_csv(os.path.join(outdir, "merra2_timeseries.csv"), index=False)
print("✅ MERRA2-Zeitreihe gespeichert.")

