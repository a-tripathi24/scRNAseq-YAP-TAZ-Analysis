import os
import pandas as pd
import numpy as np

folder_path = "results/all_excel_files"
marker_columns = {"YAP1": "YAP1_expr", "TAZ": "TAZ_expr", "Double": ["YAP1_expr", "TAZ_expr"]}
records = []

for file_name in os.listdir(folder_path):
    if not file_name.endswith(".xlsx"):
        continue

    file_path = os.path.join(folder_path, file_name)
    parts = file_name.replace(".xlsx", "").split("_")

    if "Double" in file_name:
        marker = "Double"
    elif "WWTR1" in file_name or "TAZ" in file_name:
        marker = "TAZ"
    elif "YAP1" in file_name:
        marker = "YAP1"
    else:
        continue

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        continue

    if marker == "Double":
        required_cols = marker_columns["Double"]
        if all(col in df.columns for col in required_cols):
            expr = df[required_cols].mean(axis=1)
        else:
            continue
    else:
        col = marker_columns[marker]
        if col not in df.columns:
            continue
        expr = pd.to_numeric(df[col], errors="coerce")

    expr = expr.dropna()
    if len(expr) == 0:
        continue

    if parts[-2] in ["normal", "tumour", "all"]:
        cell_type = parts[-3]
        condition = parts[-2]
    else:
        cell_type = parts[-2]
        condition = parts[-1]

    if cell_type == "t" and condition == "cells":
        cell_type = "t_cells"
        condition = "normal"

    records.append({
        "Cell_Type": cell_type, "Condition": condition, "Marker": marker,
        "Mean_Expression": np.mean(expr), "Std_Expression": np.std(expr)
    })

summary_df = pd.DataFrame(records)
output_csv_path = os.path.join(folder_path, "marker_mean_std_expression.csv")
summary_df.to_csv(output_csv_path, index=False)