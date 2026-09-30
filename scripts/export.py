import pandas as pd
import os
import sys
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import kruskal

base_path = "results/all_excel_files"
os.makedirs("results", exist_ok=True)
output_filename = "results/statistical_results.txt"

file_mappings = {
    'All Cells': {'DP': 'Cells_Double_Positive_all_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_all_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_all_normal.xlsx'},
    'B Cells': {'DP': 'Cells_Double_Positive_bcells_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_bcells_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_bcells_normal.xlsx'},
    'Epithelial': {'DP': 'Cells_Double_Positive_epithelial_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_epithelial_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_epithelial_normal.xlsx'},
    'Fibroblast': {'DP': 'Cells_Double_Positive_fibroblast_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_fibroblast_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_fibroblast_normal.xlsx'},
    'Lymphatic': {'DP': 'Cells_Double_Positive_lymphatic_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_lymphatic_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_lymphatic_normal.xlsx'},
    'Myeloid': {'DP': 'Cells_Double_myeloid_all_normal.xlsx', 'YAP': 'Cells_YAP1_myeloid_all_normal.xlsx', 'TAZ': 'Cells_WWTR1_myeloid_all_normal.xlsx'},
    'Perivascular': {'DP': 'Cells_Double_Positive_perivascular_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_perivascular_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_perivascular_normal.xlsx'},
    'T Cells': {'DP': 'Cells_Double_Positive_t_cells_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_t_cells_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_t_cells_normal.xlsx'},
    'Vascular': {'DP': 'Cells_Double_Positive_vascular_normal.xlsx', 'YAP': 'Cells_YAP1_Expression_vascular_normal.xlsx', 'TAZ': 'Cells_WWTR1_Expression_vascular_normal.xlsx'}
}

def build_condition_df(condition_name, expression_col):
    frames = []
    for cell_type, files in file_mappings.items():
        path = os.path.join(base_path, files[condition_name])
        if os.path.exists(path):
            df = pd.read_excel(path)
            if condition_name == 'DP':
                 df['Expression_Level'] = (df['YAP1_expr'] + df['TAZ_expr']) / 2
            else:
                df = df.rename(columns={expression_col: 'Expression_Level'})
            df['Cell_Type'] = cell_type
            frames.append(df[['Expression_Level', 'Cell_Type']])
    return pd.concat(frames, ignore_index=True)

dp_df = build_condition_df('DP', None)
yap_df = build_condition_df('YAP', 'YAP1_expr')
taz_df = build_condition_df('TAZ', 'TAZ_expr')

def run_and_save_tests(df, condition_title, file_handle):
    file_handle.write(f"--- Statistical Tests for {condition_title} ---\n\n")
    
    file_handle.write("--- One-Way ANOVA ---\n")
    model = ols('Expression_Level ~ C(Cell_Type)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    file_handle.write(str(anova_table) + "\n\n")
    
    file_handle.write("--- Kruskal-Wallis ---\n")
    grouped_data = [group['Expression_Level'].values for name, group in df.groupby('Cell_Type')]
    h_statistic, p_value = kruskal(*grouped_data)
    file_handle.write(f"H-statistic: {h_statistic}\n")
    file_handle.write(f"p-value: {p_value}\n")
    file_handle.write("-" * 50 + "\n\n")

with open(output_filename, 'w') as f:
    run_and_save_tests(dp_df, "Double Positive Expression", f)
    run_and_save_tests(yap_df, "YAP-Only Expression", f)
    run_and_save_tests(taz_df, "TAZ-Only Expression", f)

print(f"Stats saved to {output_filename}")