import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

base_path = "results/all_excel_files"
os.makedirs("results", exist_ok=True)

file_mappings = {
    "YAP-Only": {
        "B Cells": "Cells_YAP1_Expression_bcells_normal.xlsx",
        "Epithelial": "Cells_YAP1_Expression_epithelial_normal.xlsx",
        "Fibroblast": "Cells_YAP1_Expression_fibroblast_normal.xlsx",
        "Lymphatic": "Cells_YAP1_Expression_lymphatic_normal.xlsx",
        "Myeloid": "Cells_YAP1_myeloid_all_normal.xlsx",
        "Perivascular": "Cells_YAP1_Expression_perivascular_normal.xlsx",
        "T Cells": "Cells_YAP1_Expression_t_cells_normal.xlsx",
        "Vascular": "Cells_YAP1_Expression_vascular_normal.xlsx",
        "All Cells": "Cells_YAP1_Expression_all_normal.xlsx"
    },
    "TAZ-Only": {
        "B Cells": "Cells_WWTR1_Expression_bcells_normal.xlsx",
        "Epithelial": "Cells_WWTR1_Expression_epithelial_normal.xlsx",
        "Fibroblast": "Cells_WWTR1_Expression_fibroblast_normal.xlsx",
        "Lymphatic": "Cells_WWTR1_Expression_lymphatic_normal.xlsx",
        "Myeloid": "Cells_WWTR1_myeloid_all_normal.xlsx",
        "Perivascular": "Cells_WWTR1_Expression_perivascular_normal.xlsx",
        "T Cells": "Cells_WWTR1_Expression_t_cells_normal.xlsx",
        "Vascular": "Cells_WWTR1_Expression_vascular_normal.xlsx",
        "All Cells": "Cells_WWTR1_Expression_all_normal.xlsx"
    },
    "Double Positive": {
        "B Cells": "Cells_Double_Positive_bcells_normal.xlsx",
        "Epithelial": "Cells_Double_Positive_epithelial_normal.xlsx",
        "Fibroblast": "Cells_Double_Positive_fibroblast_normal.xlsx",
        "Lymphatic": "Cells_Double_Positive_lymphatic_normal.xlsx",
        "Myeloid": "Cells_Double_myeloid_all_normal.xlsx",
        "Perivascular": "Cells_Double_Positive_perivascular_normal.xlsx",
        "T Cells": "Cells_Double_Positive_t_cells_normal.xlsx",
        "Vascular": "Cells_Double_Positive_vascular_normal.xlsx",
        "All Cells": "Cells_Double_Positive_all_normal.xlsx"
    }
}

all_frames = []
for marker_name, mapping in file_mappings.items():
    for cell_type, filename in mapping.items():
        path = os.path.join(base_path, filename)
        if os.path.exists(path):
            df = pd.read_excel(path)
            if marker_name == "Double Positive":
                df['Expression_Level'] = (df['YAP1_expr'] + df['TAZ_expr']) / 2
            elif marker_name == "YAP-Only":
                df = df.rename(columns={'YAP1_expr': 'Expression_Level'})
            elif marker_name == "TAZ-Only":
                df = df.rename(columns={'TAZ_expr': 'Expression_Level'})

            df['Cell_Type'] = cell_type
            df['Marker'] = marker_name
            all_frames.append(df[['Expression_Level', 'Cell_Type', 'Marker']])

combined_df = pd.concat(all_frames, ignore_index=True)

plt.figure(figsize=(16, 9))
# showfliers=False to keep the plot clean
sns.boxplot(data=combined_df, x='Cell_Type', y='Expression_Level', hue='Marker', showfliers=False)
plt.title('YAP/TAZ Expression Across Cell Types in Normal Breast Tissue')
plt.ylabel('Expression Level')
plt.xlabel('Cell Type')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/normal_tissue_boxplot.png')
print("Boxplot saved to results folder.")