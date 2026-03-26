import pandas as pd
import os
import config
import matplotlib.pyplot as plt
import seaborn as sns


def set_viz_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.dpi"] = 150
    plt.rcParams["font.family"] = "sans-serif"


def load_codebase_data():
    try:
        if not os.path.exists(config.DATA_SOURCE):
            raise FileNotFoundError(
                f"Missing {config.DATA_SOURCE}. Please place your CSV in the script folder."
            )

        # 1. Ingest data (handling missing headers and empty first rows)
        df_preview = pd.read_csv(config.DATA_SOURCE, nrows=2, header=None)
        
        # Safely get the first row as string to check for potential headers
        if not df_preview.empty:
            first_row_str = "".join(df_preview.iloc[0].dropna().astype(str).values).upper()
        else:
            first_row_str = ""

        if "PATH" in first_row_str or "TAG" in first_row_str:
            df = pd.read_csv(config.DATA_SOURCE)
        else:
            # Standard fallback for the 3-column output from your app
            df = pd.read_csv(
                config.DATA_SOURCE, header=None, names=["PATH", "TAG", "TECH"]
            )

        # Drop entirely empty rows that may have snuck in 
        df = df.dropna(how="all")

        # 2. Clean Column Names
        df.columns = [str(c).strip() for c in df.columns]

        # 3. Defensive Column Selection
        path_col = next((c for c in df.columns if "PATH" in str(c).upper()), "PATH")
        tag_col = next((c for c in df.columns if "TAG" in str(c).upper()), "TAG")
        tech_col = next((c for c in df.columns if "TECH" in str(c).upper()), "TECH")

        if path_col not in df.columns or tag_col not in df.columns or tech_col not in df.columns:
            raise ValueError("CSV is missing one of the required columns: PATH, TAG, or TECH.")

        # 4. Path Normalization (Privacy & Portability)
        valid_paths = [str(p) for p in df[path_col] if pd.notna(p)]
        if valid_paths:
            split_paths = [p.replace("/", os.sep).replace("\\", os.sep).split(os.sep) for p in valid_paths]
            common_parts = []
            min_len = min(len(p) for p in split_paths)
            for i in range(min_len):
                if all(p[i] == split_paths[0][i] for p in split_paths):
                    common_parts.append(split_paths[0][i])
                else:
                    break
            
            # If the remaining length of the shortest path is 1, 
            # we are stripping all the way down to the leaf node (the repo itself).
            # To preserve container context, we step back one directory.
            if len(common_parts) > 0:
                min_remaining = min(len(p) - len(common_parts) for p in split_paths)
                if min_remaining <= 1 and len(common_parts) > 1:
                    common_parts.pop()
        else:
            common_parts = []

        def clean_path(p):
            p = str(p).replace("/", os.sep).replace("\\", os.sep)
            parts = p.split(os.sep)
            idx = len(common_parts)
            if idx >= len(parts):
                return parts[-1] if parts else p
            return os.sep.join(parts[idx:])

        def extract_root(p):
            p = str(p).replace("/", os.sep).replace("\\", os.sep)
            parts = p.split(os.sep)
            idx = len(common_parts)
            if idx < len(parts):
                return parts[idx]
            return parts[-1] if parts else "Unknown"

        df["Clean_Path"] = df[path_col].apply(clean_path)
        df["Root"] = df[path_col].apply(extract_root)

        # Standardize column names for the rest of the scripts
        df = df.rename(columns={tag_col: "TAG", tech_col: "TECH"})

        return df

    except FileNotFoundError:
        raise
    except pd.errors.EmptyDataError:
        raise ValueError("The provided CSV file is empty.")
    except Exception as e:
        raise ValueError(f"Error loading data: {e}. Please ensure your CSV is formatted correctly with paths and tags.")
