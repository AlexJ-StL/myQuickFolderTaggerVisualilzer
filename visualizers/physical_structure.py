import matplotlib.pyplot as plt
import seaborn as sns

def map_physical_structure(df, output_image="physical_structure_map.png"):
    # Using the 'Root' column cleanly extracted in utils.py
    root_counts = df["Root"].value_counts()

    # Plotting
    plt.figure(figsize=(12, 8))
    sns.barplot(x=root_counts.values, y=root_counts.index, palette="viridis")
    plt.title("Physical Structure Map: Repository Distribution by Root Folder", fontsize=15)
    plt.xlabel("Number of Repositories", fontsize=12)
    plt.ylabel("Root Directory", fontsize=12)
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    plt.savefig(output_image)
    print(f"✅ Physical structure map saved to {output_image}")
    return root_counts
