import scanpy as sc
import pandas as pd
import os
from scipy.sparse import issparse

# set paths
file_path = "data/annotated/vascular.h5ad"
output_folder = "results/"
output_file = "vascular.xlsx"
cell_type = "vascular_cells"

os.makedirs(output_folder, exist_ok=True)

print(f"Loading {file_path}...")
adata = sc.read_h5ad(file_path)
adata.obs_names_make_unique()

# disable .raw to use .X directly
adata.raw = None

# ensembl IDs for YAP1 and WWTR1 (TAZ)
yap1_id = "ENSG00000137693"
taz_id = "ENSG00000174684"

if yap1_id not in adata.var_names or taz_id not in adata.var_names:
    print("Error: YAP1 or WWTR1 (TAZ) Ensembl IDs not found.")
    exit()

# extract expression 
yap_data = adata[:, yap1_id].X
taz_data = adata[:, taz_id].X

if issparse(yap_data):
    yap_data = yap_data.toarray().flatten()
else:
    yap_data = yap_data.flatten()

if issparse(taz_data):
    taz_data = taz_data.toarray().flatten()
else:
    taz_data = taz_data.flatten()

# add to obs
adata.obs['YAP1_expr'] = yap_data
adata.obs['TAZ_expr'] = taz_data
adata.obs['YAP1_pos'] = adata.obs['YAP1_expr'] > 0
adata.obs['TAZ_pos'] = adata.obs['TAZ_expr'] > 0
adata.obs['Double_pos'] = adata.obs['YAP1_pos'] & adata.obs['TAZ_pos']

# generate summary
total = adata.n_obs
summary = {
    "Cell Type": cell_type,
    "Total Cells": total,
    "% YAP1+": (adata.obs['YAP1_pos'].sum() / total) * 100,
    "% TAZ+": (adata.obs['TAZ_pos'].sum() / total) * 100,
    "% Double+": (adata.obs['Double_pos'].sum() / total) * 100,
    "Mean YAP1 Expr": adata.obs['YAP1_expr'].mean(),
    "Mean TAZ Expr": adata.obs['TAZ_expr'].mean()
}

df = pd.DataFrame([summary])
df.to_excel(os.path.join(output_folder, output_file), index=False)

print(f"Summary saved to {output_file}")