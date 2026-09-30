import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = "results/all_excel_files/marker_mean_std_expression_cleaned.csv"
df = pd.read_csv(file_path)

# clean up cell type names
df["Cell_Type"] = df["Cell_Type"].astype(str).str.strip().str.replace("_", " ").str.replace(",", " ").str.title()
df["Cell_Type"] = df["Cell_Type"].replace({
    "B Cells": "B Cells", "T Cells": "T Cells", "All": "All",
    "Myeloid": "Myeloid", "Epithelial": "Epithelial", "Fibroblast": "Fibroblast",
    "Perivascular": "Perivascular", "Lymphatic": "Lymphatic", "Vascular": "Vascular"
})

df["Marker"] = df["Marker"].replace({
    "YAP1 (Double+)": "YAP1", "TAZ (Double+)": "TAZ", "Double (Avg)": "Double"
})

df = df.dropna(subset=["Mean_Expression", "Std_Expression"])
df["Mean_Expression"] = pd.to_numeric(df["Mean_Expression"], errors="coerce")
df["Std_Expression"] = pd.to_numeric(df["Std_Expression"], errors="coerce")

cell_order = ['Myeloid', 'B Cells', 'Epithelial', 'Fibroblast', 'Lymphatic',
              'Perivascular', 'T Cells', 'Vascular', 'All']
marker_order = ['YAP1', 'TAZ', 'Double']
df["Cell_Type"] = pd.Categorical(df["Cell_Type"], categories=cell_order, ordered=True)
df["Marker"] = pd.Categorical(df["Marker"], categories=marker_order, ordered=True)
df = df.sort_values(["Cell_Type", "Marker"])

x_labels = df["Cell_Type"].unique()
bar_width = 0.25
x = np.arange(len(x_labels))
offsets = {"YAP1": -bar_width, "TAZ": 0, "Double": bar_width}

plt.figure(figsize=(16, 6))
palette = {"YAP1": "#1f77b4", "TAZ": "#ff7f0e", "Double": "#2ca02c"}

for marker in marker_order:
    subset = df[df["Marker"] == marker]
    xpos = x + offsets[marker]
    plt.bar(xpos, subset["Mean_Expression"], yerr=subset["Std_Expression"],
        width=bar_width, label=marker, color=palette[marker], capsize=5)

plt.xticks(x, x_labels, rotation=45)
plt.xlabel("Cell Type")
plt.ylabel("Mean Expression Level")
plt.title("Mean Expression of YAP1, TAZ, and Double Markers Across Cell Types (Normal Tissue)")
plt.legend(title="Marker")
plt.tight_layout()
plt.grid(True, axis='y', linestyle='--', alpha=0.6)

plt.savefig("results/marker_expression_plot_cleaned_final.png", dpi=300)