import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "results/marker_mean_expression.csv"
df = pd.read_csv(file_path)
df = df[df["Condition"] == "normal"]

df["Mean_Expression"] = pd.to_numeric(df["Mean_Expression"], errors="coerce")
df["Std_Expression"] = pd.to_numeric(df["Std_Expression"], errors="coerce")

plt.figure(figsize=(16, 6))
sns.set(style="whitegrid")

ax = sns.barplot(
    data=df, x="Cell_Type", y="Mean_Expression", hue="Marker",
    palette=["green", "orange", "blue"], errorbar=None, capsize=0.2
)

for i, bar in enumerate(ax.patches):
    index = i % len(df)
    row = df.iloc[index]
    bar_x = bar.get_x() + bar.get_width() / 2
    bar_height = bar.get_height()
    std = row["Std_Expression"]

    plt.errorbar(
        x=bar_x, y=bar_height, yerr=std, color="black",
        capsize=5, fmt='none', linewidth=1.2
    )

plt.title("Mean Marker Expression Across Cell Types (Normal Tissue)", fontsize=14)
plt.xlabel("Cell Type", fontsize=12)
plt.ylabel("Mean Expression", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.legend(title="Marker")
plt.tight_layout()

plt.savefig("results/marker_expression_plot.png", dpi=300)