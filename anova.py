import pandas as pd
import os
import statsmodels.api as sm
from statsmodels.formula.api import ols

base_path = "results/all_excel_files"

file_mappings = {
    "YAP1": {
        "B Cells": "Cells_YAP1_Expression_bcells_normal.xlsx",
        "Epithelial": "Cells_YAP1_Expression_epithelial_normal.xlsx",
        "Fibroblast": "Cells_YAP1_Expression_fibroblast_normal.xlsx",
        "Lymphatic": "Cells_YAP1_Expression_lymphatic_normal.xlsx",
        "Myeloid": "Cells_YAP1_Expression_myeloid_all_normal.xlsx",
        "Perivascular": "Cells_YAP1_Expression_perivascular_normal.xlsx",
        "T Cells": "Cells_YAP1_Expression_t_cells_normal.xlsx",
        "Vascular": "Cells_YAP1_Expression_vascular_normal.xlsx",
        "All Cells": "Cells_YAP1_Expression_all_normal.xlsx"
    },
    "WWTR1": {
        "B Cells": "Cells_WWTR1_Expression_bcells_normal.xlsx",
        "Epithelial": "Cells_WWTR1_Expression_epithelial_normal.xlsx",
        "Fibroblast": "Cells_WWTR1_Expression_fibroblast_normal.xlsx",
        "Lymphatic": "Cells_WWTR1_Expression_lymphatic_normal.xlsx",
        "Myeloid": "Cells_WWTR1_Expression_myeloid_all_normal.xlsx",
        "Perivascular": "Cells_WWTR1_Expression_perivascular_normal.xlsx",
        "T Cells": "Cells_WWTR1_Expression_t_cells_normal.xlsx",
        "Vascular": "Cells_WWTR1_Expression_vascular_normal.xlsx",
        "All Cells": "Cells_WWTR1_Expression_all_normal.xlsx"
    },
    "Double": {
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

def build_marker_df(marker_name, mapping):
    frames = []
    for cell_type, filename in mapping.items():
        path = os.path.join(base_path, filename)
        if os.path.exists(path):
            df = pd.read_excel(path)

            if marker_name == "YAP1":
                df = df.rename(columns={'YAP1_expr': 'Expression_Level'})
            elif marker_name == "WWTR1":
                df = df.rename(columns={'TAZ_expr': 'Expression_Level'})
            elif marker_name == "Double":
                df['Expression_Level'] = (df['YAP1_expr'] + df['TAZ_expr']) / 2

            df['Cell_Type'] = cell_type
            frames.append(df[['Expression_Level', 'Cell_Type']])

    marker_df = pd.concat(frames, ignore_index=True)
    marker_df['Marker'] = marker_name
    return marker_df

yap_df = build_marker_df("YAP1", file_mappings["YAP1"])
taz_df = build_marker_df("WWTR1", file_mappings["WWTR1"])
double_df = build_marker_df("Double", file_mappings["Double"])

def run_anova(df, marker_name):
    print(f"\n--- ANOVA for {marker_name} ---")
    model = ols('Expression_Level ~ C(Cell_Type)', data=df).fit()
    table = sm.stats.anova_lm(model, typ=2)
    print(table)
    return table

run_anova(yap_df, "YAP1")
run_anova(taz_df, "WWTR1")
run_anova(double_df, "Double Positive")