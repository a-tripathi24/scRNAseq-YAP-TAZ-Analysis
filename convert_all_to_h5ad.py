import scanpy as sc
import os

input_dir = "data/normal"
output_dir = "data/normal/h5ad"
os.makedirs(output_dir, exist_ok=True)

converted = 0
for filename in os.listdir(input_dir):
    if filename.endswith(".h5"):
        try:
            file_path = os.path.join(input_dir, filename)
            # extract sample ID from string
            sample_id = filename.split("_")[0]
            print(f"Converting {filename}...")

            adata = sc.read_10x_h5(file_path)
            adata.obs['sample'] = sample_id
            adata.var_names_make_unique()
            
            output_path = os.path.join(output_dir, f"{sample_id}.h5ad")
            adata.write(output_path)
            converted += 1
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")

print(f"Done. Converted {converted} files to .h5ad")