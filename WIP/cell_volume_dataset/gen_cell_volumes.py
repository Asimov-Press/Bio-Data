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


CELL_VOLUME_EXCLUDE_KEYWORDS = [
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
    'volume, growth, and yield', 'range of', 'results of', 'variability in', 'volume of blood',
    'volumes for milk secreted', 'water accessible volumes', 'slope of log carbon',
    'resolvable volumes', 'interspecies comparison', 'in different stages',
    'water-accessible volumes', 'volumes inaccessible to', 
]


def filter_ecoli_volumes(df):
    """Filter for E. coli and Generic volume data"""
    # Filter for E. coli and Generic data
    mask = (df['Organism'].isin(['Bacteria Escherichia coli', 'Generic']))
    filtered_data = df[mask].copy()
    
    # Apply volume filters
    mask = (
        # E. coli specific filters
        (
            (filtered_data['Organism'] == 'Bacteria Escherichia coli') &
            (
                filtered_data['property_type'].str.startswith('Volume occupied by', na=False) |
                (filtered_data['property_type'] == '"Rule of thumb"') |
                (
                    (filtered_data['property_type'] == 'Volume') & 
                    (filtered_data['property_of'] == 'cell')
                )
            )
        ) |
        # Generic organism filters
        (
            (filtered_data['Organism'] == 'Generic') &
            (filtered_data['property_type'] == 'Volume')
        )
    )
    return filtered_data[mask].sort_values(
        by=['Organism', 'property_type', 'standardized_value', 'standardized_min'],
        na_position='last'
    )


def filter_cell_volumes(df):
    """Filter for cell volume measurements"""
    # Filter for entries where Properties is "Cell volume" (case insensitive)
    filtered_data = df[df['Properties'].str.lower() == 'cell volume'].copy()
    
    return filtered_data.sort_values(
        by=['Organism', 'property_type', 'standardized_value', 'standardized_min'],
        na_position='last'
    )


def main():
    # Load data
    df = load_bionumbers_data()

    # Process and clean the data
    size_data = clean_size_data(
        df, 
        cell_volume_only=True, 
        general_size_only=False,
        exclude_keywords=CELL_VOLUME_EXCLUDE_KEYWORDS
    )

    # Debug categorization
    debug_categorization(size_data)
    
    # Analyze property types
    analyze_property_types(size_data)
    
    # Analyze specific property type
    analyze_property_details(size_data, "Diameter")
    
    # Get today's date for filenames
    today = date.today().strftime("%Y_%m_%d")
    
    # Save full dataset
    size_data_sorted = size_data.sort_values(['property_type', 'standardized_value', 'standardized_min'])
    output_path = f"./cell_volume_dataset/output/processed_cell_volume_data_{today}.csv"
    size_data_sorted.to_csv(output_path, index=False)
    
    # Save E. coli volumes subset
    ecoli_volumes = filter_ecoli_volumes(size_data)
    ecoli_volumes.to_csv(f"./cell_volume_dataset/output/ecoli_component_volume_subset_{today}.csv", index=False)
    
    # Save cell volumes subset
    cell_volumes = filter_cell_volumes(size_data)
    cell_volumes.to_csv(f"./cell_volume_dataset/output/cell_volume_organisms_subset_{today}.csv", index=False)

    # Print summary
    print("\nData Summary:")
    print(f"Total entries: {len(size_data)}")
    print(f"E. coli volume entries: {len(ecoli_volumes)}")
    print(f"Cell volume entries: {len(cell_volumes)}")
    
    print("\nEntries by category:")
    print(size_data['category'].value_counts())
    
    print("\nEntries by Organism:")
    organism_counts = size_data['Organism'].value_counts()
    print(organism_counts[organism_counts > 0].head(10))  # Show top 10 organisms

if __name__ == "__main__":
    main()
