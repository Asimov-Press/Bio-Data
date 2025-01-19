from shared.util import (
    load_bionumbers_data
)
from shared.bionumbers.parse import (
    clean_size_data
)
from cell_volume_dataset.analyze_output import (
    debug_categorization,
    analyze_property_types,
    analyze_property_details
)
from datetime import date


def main():
    # Load data
    df = load_bionumbers_data()

    # Process and clean the data
    size_data = clean_size_data(df, cell_volume_only=True, general_size_only=False)

    # Debug categorization
    debug_categorization(size_data)
    
    # Analyze property types
    analyze_property_types(size_data)
    
    # Analyze specific property type
    analyze_property_details(size_data, "Diameter")
    
    # Sort by Organism and save processed data with today's date
    size_data_sorted = size_data.sort_values(['Organism', 'standardized_min'])
    today = date.today().strftime("%Y_%m_%d")
    output_path = f"./cell_volume_dataset/output/processed_cell_volume_data_{today}.csv"
    size_data_sorted.to_csv(output_path, index=False)

    # Print summary
    print("\nData Summary:")
    print(f"Total entries: {len(size_data)}")
    print("\nEntries by category:")
    print(size_data['category'].value_counts())
    
    print("\nEntries by Organism:")
    organism_counts = size_data['Organism'].value_counts()
    print(organism_counts[organism_counts > 0].head(10))  # Show top 10 organisms

if __name__ == "__main__":
    main()
