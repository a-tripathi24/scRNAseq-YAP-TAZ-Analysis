import h5py

file = "data/normal/h5ad/batches/batch_1.h5ad"
with h5py.File(file, "r") as f:
    print("Available layers in the file:")
    print(list(f["obs"].keys()))