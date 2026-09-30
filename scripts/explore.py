import scanpy as sc

adata = sc.read_h5ad("data/normal/hbca_c50.h5ad")
print(adata)
print("Metadata columns (obs):")
print(adata.obs.columns.tolist())
print("First 10 genes:")
print(adata.var_names[:10].tolist())
print("YAP1 present:", 'YAP1' in adata.var_names)
print("WWTR1 present:", 'WWTR1' in adata.var_names)