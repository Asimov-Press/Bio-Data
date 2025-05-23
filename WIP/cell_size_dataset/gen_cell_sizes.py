from shared.util import (
    load_bionumbers_data
)
from shared.bionumbers.parse import (
    clean_size_data
)
from shared.bionumbers.qa_output import (
    debug_categorization,
    analyze_property_types,
    analyze_property_details
)
from datetime import date



CELL_SIZE_EXCLUDE_KEYWORDS = [
    'rate', 'constant', 'time', 'energy', 'force',
    'concentration', 'abundance', 'number', 'strength',
    'half-life', 'buffering capacity', 'thickness',
    'density', 'weight', 'mass',
    'ratio', 'fraction', 'percentage',
    'selection coefficient', 'flux through',
    'net pressure', 'maximum level',
    'various kinds', 'rapidly degrading', 'free level',
    'ph of', 'physical parameters', 'variation in',
    'probability of', 'power', 'population', 'turnover of',
    'activity of', 'translational diffusion', 'halflives of',
    'affinity of', 'processivity of', 'speed of',
    'diffusion coefficient', 'elemental composition',
    'kinetic parameters', 'cytoplasmic ph', 'periplasmic ph',
    'lacz mrna per', 'percent of heat shock', 'half-lives of',
    'No. of ribosomes', 'comparison of channel counts', 'peak level of',
    'reads per kilobase', 'review course', 'cutoff value', 'half life of',
    'wavelength for', 'distance on', 'residual bulk', 'halflife of',
    'contribution of', 'twenty most', 'internal ph', 'different temperatures',
    'precursor requirements', 'cell dry yield', 'most abundant', 'protein copies',
    'increase in', 'decrease in', 'co-segregation', 'cosegregation', 'replication speed',
    'cellular location', 'resting potential', 'donnan potential', 'odor thresholds', 'halflife',
    'peak in', 'oscillations', 'in the following organisms', 'atp demand', 'mechanoelectrical sensitivity',
    'pool turnover', 'per unit', 'on tryptophan', 'of ocean water', 'volume usage', 'volume variation',
    'volume, growth, and yield'
]

def main():
    # Load data
    df = load_bionumbers_data()

    # Process and clean the data
    size_data = clean_size_data(
        df, 
        general_size_only=True,
        exclude_keywords=CELL_SIZE_EXCLUDE_KEYWORDS
    )

    # Debug categorization
    debug_categorization(size_data)
    
    # Analyze property types
    analyze_property_types(size_data)
    
    # Analyze specific property type
    analyze_property_details(size_data, "Diameter")
    
    # Sort by Organism and save processed data with today's date
    size_data_sorted = size_data.sort_values(['Organism', 'standardized_min'])
    today = date.today().strftime("%Y_%m_%d")
    output_path = f"./cell_size_dataset/output/processed_size_data_{today}.csv"
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
