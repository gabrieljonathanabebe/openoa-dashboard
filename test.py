git add .
git commit -m "Modularisierung der Plotfunktionen und Aufr�umen der Struktur (utils/plot_utils, Layout-Importe angepasst)"
git push origin main


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lade transformierten Datensatz
df = pd.read_csv("/Users/jonathanabebe/Desktop/Python-Projekte/OpenOA-Dashboard/data/processed/por/mc_era5_por.csv")

# Finde die Iteration mit maximaler Steigung
max_slope_iter = df.loc[df["r2"].idxmax(), "iteration"]

# Filtere Daten dieser Iteration
df_iter = df[df["iteration"] == max_slope_iter]

# Separiere Bootstrap- und Non-Bootstrap-Daten
df_bootstrap = df_iter[df_iter["source"] == "bootstrap"]
df_non_bootstrap = df_iter[df_iter["source"] == "non-bootstrap"]

# Hole Regressionsparameter
slope = df_iter["slope"].iloc[0]
intercept = df_iter["intercept"].iloc[0]

# Regressionslinie vorbereiten
x_line = np.linspace(df_iter["wind_speed"].min(), df_iter["wind_speed"].max(), 100)
y_line = slope * x_line + intercept

# Plot
plt.figure(figsize=(8, 5))

# Streudiagramm
plt.scatter(df_bootstrap["wind_speed"], df_bootstrap["energy"], color="green", alpha=0.6, label="Bootstrap-Daten")
plt.scatter(df_non_bootstrap["wind_speed"], df_non_bootstrap["energy"], color="red", marker="x", alpha=0.8, label="Non-Bootstrap-Daten")

# Regressionslinie
regression_label = f"Regression: y = {slope:.3f}x + {intercept:.2f}"
plt.plot(x_line, y_line, color="blue", linewidth=2, label=regression_label)

# Achsen & Titel
plt.title(f"Regression – höchste Steigung (Iteration {int(max_slope_iter)})")
plt.xlabel("Windgeschwindigkeit (m/s)")
plt.ylabel("Energieertrag (GWh)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()