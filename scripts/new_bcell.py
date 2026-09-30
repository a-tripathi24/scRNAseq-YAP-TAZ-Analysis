import scanpy as sc
import pandas as pd
import os
from scipy.sparse import issparse

file_path = "data/annotated/myeloid.h5ad"
output_folder = "results/"
os.makedirs(output_folder, exist_ok=True)

yap1_id = "ENSG00000137693"
taz_id = "ENSG00000174684"

adata = sc.read_h5ad(file_path)
adata.obs_names_make_unique()
adata.raw = None 

if yap1_id not in adata.var_names or taz_id not in adata.var_names:
    print("YAP1 or WWTR1 not found.")
    exit()

yap_data = adata[:, yap1_id].X
taz_data = adata[:, taz_id].X

if issparse(yap_data): yap_data = yap_data.toarray().flatten()
else: yap_data = yap_data.flatten()

if issparse(taz_data): taz_data = taz_data.toarray().flatten()
else: taz_data = taz_data.flatten()

adata.obs['YAP1_expr'] = yap_data
adata.obs['TAZ_expr'] = taz_data
adata.obs['Double_pos'] = (adata.obs['YAP1_expr'] > 0) & (adata.obs['TAZ_expr'] > 0)

df = adata.obs[['YAP1_expr', 'TAZ_expr', 'author_cell_type', 'cell_type']].copy()
df.rename(columns={'author_cell_type': 'Cell Type', 'cell_type': 'Most Abundant Cell Type'}, inplace=True)

df_yap = df[['YAP1_expr', 'Cell Type', 'Most Abundant Cell Type']].copy()
df_yap.index.name = "Cell_ID"
df_yap.reset_index(inplace=True)
df_yap.to_excel(os.path.join(output_folder, "Cells_YAP1_myeloid_all_normal.xlsx"), index=False)

df_taz = df[['TAZ_expr', 'Cell Type', 'Most Abundant Cell Type']].copy()
df_taz.index.name = "Cell_ID"
df_taz.reset_index(inplace=True)
df_taz.to_excel(os.path.join(output_folder, "Cells_WWTR1_myeloid_all_normal.xlsx"), index=False)

df_double = df[(df['YAP1_expr'] > 0) & (df['TAZ_expr'] > 0)].copy()
df_double.index.name = "Cell_ID"
df_double.reset_index(inplace=True)
df_double.to_excel(os.path.join(output_folder, "Cells_Double_myeloid_all_normal.xlsx"), index=False)