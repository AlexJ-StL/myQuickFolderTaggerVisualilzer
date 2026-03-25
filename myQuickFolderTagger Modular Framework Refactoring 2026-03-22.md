# Modular Framework Refactoring

1. The Core Infrastructure (Root Directory)
Before touching the visualizers, these two files must be finalized. They act as the substrate (wei~mi) for everything else.
[ ] **config.py:** Define **DATA_SOURCE, PATH_MARKERS** (e.g., "Repos", "Coding"), and a **STOP_WORDS** set for the 3D plots.
[ ] **utils.py:** Implement the load_codebase_data() function we discussed. It should handle the header-less CSV, clean the paths, and return a single, standardized DataFrame.

2. The Visualizer Refactor (Inside /visualizer)
Fo
## Refactoring Checklistr each of the six scripts, you need to perform the following "surgery":
[ ] Remove import pandas as pd and pd.read_csv() from inside the functions.
[ ] Remove any hardcoded file paths or execution calls (like my_function("codebase_tags.csv")) at the bottom of the files.
[ ] Change the function signature to accept df as the primary argument (e.g., def generate_sunburst(df):).
[ ] Update logic to use the cleaned columns provided by utils.py (specifically df['Root'] and df['Clean_Path']).
[ ] **Cross-Platform Fix:** In sunburst-directory.py, replace the manual \ splitting with os.path.normpath and os.sep to support Linux/Mac users.

3. The Orchestration (main.py)
This is the final piece that connects the substrate to the visual output.
[ ] Import utils.
[ ] Import every function from your visualizer sub-package.
[ ] **Sequence:** Call utils.load_codebase_data() once, then pass that df into each visualizer function in sequence.

4. GitHub Readiness (The "Polish" Layer)
[ ] **.gitignore:** Add __pycache__/, .venv/, *.png, and your specific codebase_tags.csv (to keep your personal data off the public repo).
[ ] **requirements.txt:** List the dependencies: pandas, matplotlib, seaborn, scikit-learn, and networkx.
[ ] **README.md:** Briefly explain how to run main.py and what the **PATH_MARKERS** in config.py do.


## Refactoring Plan 
### 1. Decouple Logic from Execution
Currently, your scripts (like multi-tech-stats.py and word-frequency-table.py) have hardcoded filenames and execution calls at the bottom.
* **Suggestion:** Ensure every script uses the load\_codebase\_data() from utils.py exclusively.
* **Value:** This allows a user to change the CSV name in config.py once, and all six visualizations will update automatically.

### 2. Standardization of the "3D Galaxy"
In unsupervised-3D.py, you are using PCA for dimensionality reduction.
* **Suggestion:** Consider adding StandardScaler from sklearn.preprocessing before the PCA.
* **Why:** PCA is sensitive to the scale of the data. Since TF-IDF values are generally normalized, it might not seem necessary, but if you later add metadata (like file size or commit counts) to the X,Y,Z axes, scaling becomes mandatory to prevent one feature from dominating the "spatial" relationship.

### 3. Enhancing the Sunburst (Hierarchy Resolution)
In sunburst-directory.py, you are splitting paths by \.
* **Suggestion:** Use os.path.normpath() and os.sep instead of hardcoded backslashes.
* **Value:** This makes the script "Cross-Platform" by default. If a Linux user runs your tool, the hardcoded \ would fail to split their paths correctly.

### 4. Robustness in structured-3D.py
You have a hardcoded stop_words set.
* **Suggestion:** Move the stop_words list to config.py.
* **Value:** Different users might have different "noise" words in their tags (e.g., some might want to filter out "repo" or "test"). Centralizing this makes the tool more customizable without the user needing to edit the logic.

### 5. Unified "Runner" Script
Rather than asking a user to run six different Python files, you can add a main.py that acts as an orchestrator.
```Python
# main.py
from multi_tech_stats import generate_multi_tech_stats
from physical_structure import map_physical_structure
# ... import others


def main():
   print("🚀 Generating Codebase Visualizations...")
   # Call each function
   print("✅ Done! Check your folder for .png files.")


if __name__ == "__main__":
   main()
```

### 6. Visual Refinement (The "Dark Mode" Aesthetic)
Since this is for GitHub, aesthetic "wow-factor" helps adoption.
* **Suggestion:** Add plt.style.use('dark_background') or use a specific Seaborn theme (like sns.set_theme(style="whitegrid")) inside a shared plotting_utils.py.
* **Value:** It gives the entire suite a professional, unified "product" feel.

### 7. Missing wei~mi: Error Handling
If the CSV is empty or the TAG column is missing, the scripts currently crash with a KeyError.
* **Suggestion:** Add a simple try-except block in utils.load_codebase_data that gives a "human-friendly" error message (e.g., "Hey, I couldn't find the 'TAG' column. Check your CSV format.")

### 8. Current Directory Tree:
myQuickFolderTaggerVisualizer/
```directory_tree
├── __pycache__/
│   ├── config.cpython-314.pyc
│   └── utils.cpython-314.pyc
├── codebase_tags.csv
├── config.py
├── main.py
├── pyproject.toml
├── README.md
├── utils.py
├── uv.lock
└── visualizers/
   ├── multi-tech-stats.py
   ├── physical-structure.py
   ├── structured-3D.py
   ├── sunburst-directory.py
   ├── unsupervised-3D.py
   └── word-frequency-table.py
```

### 9. The "Import Resolution" Hurdle
Since your scripts are now in a subfolder (visualizers/), they will have trouble finding utils.py and config.py in the parent directory if run individually.
* **Suggestion:** Use main.py as the sole orchestrator. The scripts in the subfolder should contain the functions, and main.py will import them and provide the data.

### 10. Standardization of the utils Integration
Looking at your current scripts (like multi-tech-stats.py), tataFrame as an argument instead of a file_path.
hey still contain pd.read_csv(file_path) inside the functions. This bypasses the defensive loading and path cleaning we built into utils.py.
* **Suggestion:** Update the functions to accept a D


### 11. Updated "Modular" Template
Here is how I recommend refactoring each of those scripts in your visualizers/ folder to be truly modular and "GitHub Ready":
* **Example:** Refactored visualizers/physical-structure.py

```Python
import matplotlib.pyplot as plt
import seaborn as sn
def map_physical_structure(df, output_image="physical_structure_map.png"):
   # We no longer load the CSV here. 
   # We use the 'Root' column created by our defensive utils.p
   root_counts = df['Root'].value_counts()

   plt.figure(figsize=(12, 8))
   sns.barplot(x=root_counts.values, y=root_counts.index, palette="viridis")
   plt.title("Physical Structure Map: Repository Distribution by Root Folder", fontsize=15)
   plt.xlabel("Number of Repositories", fontsize=12)
   plt.ylabel("Root Directory", fontsize=12)
   plt.grid(axis="x", linestyle="--", alpha=0.7)
   plt.tight_layout()


   plt.savefig(output_image)
   print(f"✅ Physical structure map saved to {output_image}")
```

### 12. The Orchestrator: main.py
This becomes your "Command Center." It loads the data once and passes it to every visualizer. This is highly efficient for large codebases.
```Python
# main.py
import utils
from vizualizers.multi_tech_stats import generate_multi_tech_stats
from vizualizers.physical_structure import map_physical_structure
from vizualizers.structured_3d import generate_3d_node_topology
# ... import other visualizers

def main():
    try:
        print("🔍 Loading codebase data...")
        df = utils.load_codebase_data()
        
        print("🎨 Generating visualizations...")
        
        # Pass the pre-cleaned dataframe to each function
        map_physical_structure(df)
        generate_multi_tech_stats(df)
        generate_3d_node_topology(df)
        
        print("\n✨ All visualizations generated successfully!")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
```

### 13. Aesthetic Synergy (The rek~mi of Style)
Since these are for GitHub, a unified look is vital.
* **Suggestion:** Add a small function to your utils.py called set_viz_style().
* **Action:** Call it at the start of main.py.

```Python
# Add to utils.py
import matplotlib.pyplot as plt
import seaborn as sns

def set_viz_style():
   sns.set_theme(style="whitegrid")
   plt.rcParams['figure.dpi'] = 150
   plt.rcParams['font.family'] = 'sans-serif'
```

### 14. The "Privacy" Check
In structured-3D.py and unsupervised-3D.py, ensure you are using df['Clean_Path'] instead of the original PATH column in your labels. This ensures that your local Windows username (AlexJ) doesn't accidentally end up in a screenshot on your GitHub repo.

#### Summary of Next Steps
* **Standardize Functions:** Change your visualizer functions to accept df instead of file_path.
* **Harmonize Folder Names:** Your tree uses visualizers. Ensure your imports in main.py match that exactly.
* **Update pyproject.toml:** If you're using uv, make sure networkx, scikit-learn, seaborn, and matplotlib are added as dependencies.


## Refactoring Recommendations

### 1. The "Modular" Template
Every file in your /visualizer folder should follow a standard pattern. This makes the codebase predictable and easy to maintain.
**Current Pattern (Problematic for GitHub):**
```Python
def my_viz(file
   df = pd.read_csv(file_path) # Crashes if path is absolute/wrong
   # ... logic ...
my_viz("codebase_tags.csv") # Hardcoded execution
```
**Recommended Pattern (Modular):**
```Python
def generate_viz(df, output_name="viz.png"):
   # Logic only. Assumes df is already cleaned by utils.py
   # ... logic ...
   plt.savefig(output_image)
```


## 2. Specific Logic Fixes
* **physical-structure.py & sunburst-directory.py:** These currently rely on a hardcoded string PATH: C:\Users\AlexJ.... By using the utils.load_codebase_data() we built, these scripts can instead use the df['Root'] column, making them work on any computer instantly.
* **structured-3D.py:** I noticed your stop_words are defined inside the function. For an open-source tool, it’s better to move these to config.py so a user can easily add their own "noise" words without touching the code.


## Proposed main.py Orchestrator
With your new directory tree, main.py should be the only file the user ever has to run. It acts as the "substrate" (wei~mi) that connects the data to the art.
```Python
import utils
from visualizer.multi_tech\_stats import generate_multi_tech_stats
from visualizer.physical_structure import map_physical_structure
# ... import the others

def main():
   print("🚀 Starting Codebase Visualization Suite...")

   # 1. Load the data once (defensively)
   df = utils.load_codebase_data()

   # 2. Run the visualizers
   map_physical_structure(df)
   generate_multi_tech_stats(df)
   # ... call the others

   print("✨ Process Complete. Check your folder for images.")

if __name__ == "__main__":
   main()
```

## Final Polish for GitHub
Before you push, I recommend adding two small "quality of life" files to your root:
1. **.gitignore:** To ensure your .venv, __pycache__, and the generated .png files don't clutter the repo.
2. **pyproject.toml:** So users can simply run 'uv pip install -r pyproject.toml'.