import os
import copy
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import clear_output

from openoa.analysis.aep import MonteCarloAEP
from openoa.utils import plot

import project_ENGIE


def run_monte_carlo(project, products, outlier_detection, name, outdir="/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/raw"):
    print(f"\nRunning {name} with products={products} and outlier={outlier_detection}")

    pa = MonteCarloAEP(
        project,
        reanalysis_products=products,
        outlier_detection=outlier_detection
    )
    pa.run(num_sim=2000, reanalysis_products=products)

    df = pd.concat([
        pa.results,
        pd.DataFrame(data={
            'slope': pa._mc_slope.ravel(),
            'intercept': pa._mc_intercept,
            'num_points': pa._mc_num_points,
            'metered_energy_fraction': pa.mc_inputs.metered_energy_fraction,
            'loss_fraction': pa.mc_inputs.loss_fraction,
            'num_years_windiness': pa.mc_inputs.num_years_windiness,
            'loss_threshold': pa.mc_inputs.loss_threshold,
            'reanalysis_product': pa.mc_inputs.reanalysis_product,
            'outlier_threshold': pa.mc_inputs.outlier_threshold
        })
    ], axis=1)

    df["i"] = np.arange(len(df))

    outpath = os.path.join(outdir, f"mc_{name}.csv")
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(outpath, index=False)
    print(f"✅ Saved results to {outpath}")
    return df

# Projekt vorbereiten
project = project_ENGIE.prepare('./data/la_haute_borne', use_cleansed=False)

# Konfigurationen definieren
analysis_configs = {
    "combined": {'products': ['era5', 'merra2'], 'outlier_detection': False},
    "era5": {'products': ['era5'], 'outlier_detection': False},
    "merra2": {'products': ['merra2'], 'outlier_detection': False},
    "era5_true": {'products': ['era5'], 'outlier_detection': True},
    "merra2_true": {"products": ["merra2"], "outlier_detection": True},
}

# Ergebnisse hier speichern (z. B. für spätere Analyse)
results_dict = {}

# Ausgewählte Analysen durchlaufen
for name, params in analysis_configs.items():
    df = run_monte_carlo(
        project=project,
        products=params['products'],
        outlier_detection=params['outlier_detection'],
        name=name  # für den Dateinamen: mc_*.csv
    )
    results_dict[name] = df
    

    
    
    
    
    