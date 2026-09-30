import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

input_filename = "results/mean_std_expression.csv"

if not os.path.exists(input_filename):
    print(f"File {input_filename} not found.")
else:
    results_df = pd.read_csv(input_filename)
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(16, 9)) 

    cell_types = results_df['Cell Type']
    x = np.arange(len(cell_types))
    width = 0.25

    # asymmetric error bars to stop at zero
    yerr_dp = [results_df['Mean_DP'], results_df['Std_DP']]
    yerr_yap = [results_df['Mean_YAP'], results_df['Std_YAP']]
    yerr_taz = [results_df['Mean_TAZ'], results_df['Std_TAZ']]

    ax.bar(x - width, results_df['Mean_DP'], width, label='Double Positive',
           yerr=yerr_dp, capsize=5, color='royalblue')
    ax.bar(x, results_df['Mean_YAP'], width, label='YAP',
           yerr=yerr_yap, capsize=5, color='darkorange')
    ax.bar(x + width, results_df['Mean_TAZ'], width, label='TAZ',
           yerr=yerr_taz, capsize=5, color='forestgreen')

    ax.set_ylabel('Mean Expression Level', fontsize=14)
    ax.set_title('Mean Gene Expression by Cell Type and Condition', fontsize=18, fontweight='bold')
    ax.set_xticks(x) 
    ax.set_xticklabels(cell_types, rotation=45, ha='right', fontsize=12)
    ax.legend(fontsize=12)
    
    ax.set_ylim(bottom=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()

    plot_filename = "results/expression_plot_with_error_bars_corrected.png"
    plt.savefig(plot_filename, dpi=300)
    print(f"Plot saved as {plot_filename}")