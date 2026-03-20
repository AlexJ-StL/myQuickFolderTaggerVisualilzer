import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_sunburst(file_path, output_image="sunburst_directory.png"):
    # Load and clean path data
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]
    path_col = "PATH: C:\\Users\\AlexJ\\Documents\\Coding\\Repos\\"

    # Split paths into Root and Subfolder levels
    def split_path(path):
        parts = str(path).split("\\")
        root = parts[0] if len(parts) > 0 else "Unknown"
        sub = parts[1] if len(parts) > 1 else "Main"
        return root, sub

    df[["Root", "Sub"]] = df[path_col].apply(lambda x: pd.Series(split_path(x)))

    # Analyze the top 12 roots for optimal visual resolution
    top_roots = df["Root"].value_counts().nlargest(12).index
    df_filtered = df[df["Root"].isin(top_roots)]

    root_data = df_filtered.groupby("Root").size().sort_values(ascending=False)
    sub_data = df_filtered.groupby(["Root", "Sub"]).size()

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


# Run with your CSV path
generate_sunburst("codebase_tags.xlsx")
