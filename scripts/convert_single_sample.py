import scanpy as sc
import os

os.makedirs("data/normal", exist_ok=True)
adata = sc.read_10x_h5("data/normal/GSM7500359_hbca_c50_filtered_feature_bc_matrix.h5")
adata.obs['sample'] = 'GSM7500359_c50'
adata.write("data/normal/hbca_c50.h5ad")
print("Saved as hbca_c50.h5ad")