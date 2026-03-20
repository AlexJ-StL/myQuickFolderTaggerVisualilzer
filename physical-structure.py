import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def map_physical_structure(file_path, output_image='physical_structure_map.png'):
    # Load data
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]
    
    path_col = 'PATH: C:\\Users\\AlexJ\\Documents\\Coding\\Repos\\'
    
    # Extract root directory (first part of the path)
    def get_root(path):
        parts = str(path).split('\\')
        return parts[0] if parts else 'Unknown'
    
    df['Root'] = df[path_col].apply(get_root)
    
    # Count repos per root
    root_counts = df['Root'].value_counts()
    
    # Plotting
    plt.figure(figsize=(12, 8))
    sns.barplot(x=root_counts.values, y=root_counts.index, palette='viridis')
    plt.title('Physical Structure Map: Repository Distribution by Root Folder', fontsize=15)
    plt.xlabel('Number of Repositories', fontsize=12)
    plt.ylabel('Root Directory', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.savefig(output_image)
    return root_counts

# Run
filename = 'codebase_tags.xlsx'
roots = map_physical_structure(filename)
print("Physical Structure Map generated.")
print(roots)