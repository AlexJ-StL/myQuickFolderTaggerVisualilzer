import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_sunburst(df, output_image="sunburst_directory.png"):
    # Split paths using os safe separated paths
    def split_path(path):
        parts = str(path).split(os.sep)
        root = parts[0] if len(parts) > 0 else "Unknown"
        sub = parts[1] if len(parts) > 1 else "Main"
        return root, sub

    # Use Clean_Path instead of original absolute hardcoded PATH
    df[["Root_Lvl", "Sub_Lvl"]] = df["Clean_Path"].apply(lambda x: pd.Series(split_path(x)))

    # Analyze the top 12 roots for optimal visual resolution
    top_roots = df["Root_Lvl"].value_counts().nlargest(12).index
    df_filtered = df[df["Root_Lvl"].isin(top_roots)]

    root_data = df_filtered.groupby("Root_Lvl").size().sort_values(ascending=False)
    sub_data = df_filtered.groupby(["Root_Lvl", "Sub_Lvl"]).size()

    # Visualization setup
    fig, ax = plt.subplots(figsize=(12, 12))
    size = 0.3
    cmap = plt.cm.get_cmap("tab20c")
    root_colors = cmap(np.linspace(0, 1, len(root_data)))

    # Inner Ring: Root Folders
    ax.pie(
        root_data.values,
        radius=1 - size,
        labels=root_data.index,
        labeldistance=0.7,
        rotatelabels=True,
        colors=root_colors,
        wedgeprops=dict(width=size, edgecolor="w"),
    )

    # Outer Ring: Subfolders (shaded variants of the root color)
    sub_colors = []
    for i, root in enumerate(root_data.index):
        root_subs = sub_data[root]
        for j in range(len(root_subs)):
            base_color = root_colors[i]
            alpha = max(0.4, 1.0 - (j * 0.1))  # Shade variations
            sub_colors.append((*base_color[:3], alpha))

    ax.pie(
        sub_data.reindex(root_data.index, level=0).values,
        radius=1,
        wedgeprops=dict(width=size, edgecolor="w"),
        colors=sub_colors,
    )

    ax.set_title("Sunburst Directory Diagram: Repository Hierarchy", fontsize=18, pad=20)
    plt.tight_layout()
    plt.savefig(output_image)
    print(f"Sunburst saved to {output_image}")
