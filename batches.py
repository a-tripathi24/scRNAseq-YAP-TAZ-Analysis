import scanpy as sc
import anndata as ad
import os
import math

input_folder = "data/normal/h5ad"
output_folder = os.path.join(input_folder, "batches")
os.makedirs(output_folder, exist_ok=True)

# 10 files per batch to manage RAM
files_per_batch = 10

all_files = os.listdir(input_folder)
h5ad_files = sorted([f for f in all_files if f.endswith(".h5ad")])

total_batches = math.ceil(len(h5ad_files) / files_per_batch)
print(f"Found {len(h5ad_files)} files. Processing in {total_batches} batches.\n")

for batch_number in range(total_batches):
    start = batch_number * files_per_batch
    end = start + files_per_batch
    batch_files = h5ad_files[start:end]

    print(f"Processing Batch {batch_number + 1}...")
    batch_data = []

    for i, filename in enumerate(batch_files):
        file_path = os.path.join(input_folder, filename)
        try:
            adata = sc.read_h5ad(file_path)
            adata.obs['sample'] = filename.replace(".h5ad", "")
            batch_data.append(adata)
        except Exception as e:
            print(f"Could not read {filename}: {e}")

    if batch_data:
        try:
            merged_data = ad.concat(batch_data, label="sample", keys=[adata.obs['sample'][0] for adata in batch_data])
            output_filename = f"batch_{batch_number + 1}.h5ad"
            output_path = os.path.join(output_folder, output_filename)
            merged_data.write(output_path)
            print(f"Saved {output_filename}")
        except Exception as e:
            print(f"Error merging batch: {e}")
    else:
        print("No files loaded for this batch.")

print("All batches processed.")