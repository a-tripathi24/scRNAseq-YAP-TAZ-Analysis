import pandas as pd
import os

base_path = "results/all_excel_files"

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

results = []
for cell_type, files in file_mappings.items():
    full_file_paths = {key: os.path.join(base_path, fname) for key, fname in files.items()}

    if not all(os.path.exists(fpath) for fpath in full_file_paths.values()):
        continue

    try:
        dp_df = pd.read_excel(full_file_paths['DP'])
        dp_avg_expr = (dp_df['YAP1_expr'] + dp_df['TAZ_expr']) / 2
        
        yap_df = pd.read_excel(full_file_paths['YAP'])
        taz_df = pd.read_excel(full_file_paths['TAZ'])
        
        results.append({
            'Cell Type': cell_type,
            'Mean_DP': dp_avg_expr.mean(), 'Std_DP': dp_avg_expr.std(),
            'Mean_YAP': yap_df['YAP1_expr'].mean(), 'Std_YAP': yap_df['YAP1_expr'].std(),
            'Mean_TAZ': taz_df['TAZ_expr'].mean(), 'Std_TAZ': taz_df['TAZ_expr'].std()
        })
    except Exception as e:
        print(f"Error on {cell_type}: {e}")

results_df = pd.DataFrame(results)
output_filename = "results/mean_std_expression.csv"
os.makedirs("results", exist_ok=True)
results_df.to_csv(output_filename, index=False)