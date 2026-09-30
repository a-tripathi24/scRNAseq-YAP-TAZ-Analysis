import pandas as pd
import os

def merge_expression_data(directory_path):
    if not os.path.exists(directory_path):
        return None

    all_files = [f for f in os.listdir(directory_path) if f.endswith('.xlsx')]
    if not all_files:
        return None

    data_frames = []
    for filename in all_files:
        file_path = os.path.join(directory_path, filename)
        try:
            df = pd.read_excel(file_path)
        except Exception:
            continue

        df.columns = [col.strip() for col in df.columns]
        clean_filename = filename.replace('.xlsx', '')
        parts = clean_filename.split('_')
        
        if "Double" in clean_filename:
            gene_name = "Double_Positive"
            cell_type = parts[3] if len(parts) > 3 else 'unknown'
        elif "YAP1" in clean_filename:
            gene_name = "YAP1"
            cell_type = parts[3] if len(parts) > 3 else 'unknown'
        elif "WWTR1" in clean_filename:
            gene_name = "WWTR1"
            cell_type = parts[3] if len(parts) > 3 else 'unknown'
        else:
            continue 

        if gene_name == "Double_Positive":
            if 'YAP1_Expression' in df.columns:
                yap_df = df[['YAP1_Expression']].copy()
                yap_df.rename(columns={'YAP1_Expression': 'expression'}, inplace=True)
                yap_df['gene'] = 'YAP1'
                yap_df['cell_type'] = cell_type
                data_frames.append(yap_df)

            if 'WWTR1_Expression' in df.columns:
                wwtr1_df = df[['WWTR1_Expression']].copy()
                wwtr1_df.rename(columns={'WWTR1_Expression': 'expression'}, inplace=True)
                wwtr1_df['gene'] = 'WWTR1'
                wwtr1_df['cell_type'] = cell_type
                data_frames.append(wwtr1_df)
        else:
            df.rename(columns={f'{gene_name}_Expression': 'expression'}, inplace=True)
            df['gene'] = gene_name
            df['cell_type'] = cell_type
            data_frames.append(df)

    if not data_frames:
        return None

    merged_df = pd.concat(data_frames, ignore_index=True)
    merged_df['condition'] = 'Normal'
    merged_df['cell_type'] = merged_df['cell_type'].str.replace('all', 'all_cells')

    return merged_df

if __name__ == "__main__":
    data_directory = 'results'
    final_normal_data = merge_expression_data(data_directory)

    if final_normal_data is not None:
        output_filename = os.path.join(data_directory, 'merged_normal_tissue_expression.csv')
        final_normal_data.to_csv(output_filename, index=False)