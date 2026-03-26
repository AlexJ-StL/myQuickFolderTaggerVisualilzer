import utils
from visualizers.multi_tech_stats import generate_multi_tech_stats
from visualizers.physical_structure import map_physical_structure
from visualizers.structured_3d import generate_3d_node_topology
from visualizers.sunburst_directory import generate_sunburst
from visualizers.unsupervised_3d import generate_3d_semantic_plot
from visualizers.word_frequency_table import get_word_frequency_table

def main():
    try:
        print("Starting Codebase Visualization Suite...")
        
        # 1. Setup global aesthetics
        utils.set_viz_style()

        # 2. Defensively load data
        print("Loading codebase data...")
        df = utils.load_codebase_data()

        print("Generating visualizations...")
        
        # 3. Pass clean dataframe to all visualizers sequentially
        generate_multi_tech_stats(df)
        map_physical_structure(df)
        generate_3d_node_topology(df)
        generate_sunburst(df)
        generate_3d_semantic_plot(df)
        word_freq = get_word_frequency_table(df)
        
        print("\n--- Top 10 Words by Frequency ---")
        for word, count in word_freq[:10]:
            print(f"{word}: {count}")

        print("\nAll visualizations generated successfully. Check your directory for the output PNGs.")

    except Exception as e:
        print(f"\nExecution Failed: {e}")

if __name__ == "__main__":
    main()
