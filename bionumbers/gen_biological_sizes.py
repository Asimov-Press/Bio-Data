import pandas as pd
from util import (
    load_bionumbers_data,
    extract_numeric_value,
    standardize_units
)
from datetime import date


def clean_size_data(df):
    """Extract and clean size-related measurements"""
    # Expanded keywords related to size measurements
    size_keywords = [
        'length', 'diameter', 'volume', 'size', 'radius',
        'width', 'surface area', 'cross section',
        'dimensions', 'axes', 'rule of thumb'
    ]

    specific_terms = [
        'molecular', 'molecule', 'protein', 'dna', 'rna', 
        'organelle', 'cell', 'tissue',
        # Additional specific terms
        'nuclear', 'cytoplasm', 'envelope', 'periplasm',
        'chromatid', 'chromosome', 'mitochondria', 'chloroplast',
        'ribosome', 'vesicle', 'membrane'
    ]
    size_keywords.extend(specific_terms)

    # Properties to exclude (false positives)
    exclude_keywords = [
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
        'peak in', 'oscillations'
    ]

    # Filter for size-related properties
    mask = (
        df['Properties'].str.lower().str.contains('|'.join(size_keywords), na=False) &
        ~df['Properties'].str.lower().str.contains('|'.join(exclude_keywords), na=False)
    )
    size_data = df[mask].copy()

    # Store original values
    size_data['original_value'] = size_data['Value']
    size_data['original_range'] = size_data['Range']

    # Process single values
    size_data['value'] = size_data['Value'].apply(extract_numeric_value)
    size_data['standardized_value'] = size_data.apply(
        lambda row: standardize_units(row['value'], row['Units']),
        axis=1
    )

    # Process ranges (regardless of whether value exists)
    range_values = size_data['Range'].apply(extract_numeric_value)
    
    # Split ranges into min and max
    size_data['min_value'] = range_values.apply(
        lambda x: x[0] if isinstance(x, tuple) else None
    )
    size_data['max_value'] = range_values.apply(
        lambda x: x[1] if isinstance(x, tuple) else None
    )

    # Standardize units for range values
    size_data['standardized_min'] = size_data.apply(
        lambda row: standardize_units(row['min_value'], row['Units']),
        axis=1
    )
    size_data['standardized_max'] = size_data.apply(
        lambda row: standardize_units(row['max_value'], row['Units']),
        axis=1
    )

    # Add category for scale
    size_data['category'] = size_data.apply(categorize_scale, axis=1)

    return size_data[['bion_id', 'Properties', 'Organism', 
                     'value',
                     'min_value', 'max_value',
                     'Units',
                     'standardized_value',
                     'standardized_min', 'standardized_max',
                     'category',
                     'original_value', 'original_range']]


def categorize_scale(row):
    """Categorize biological entities based on their size and properties"""
    prop = row['Properties'].lower()
    org = str(row['Organism']).lower() if pd.notna(row['Organism']) else ''

    # Small molecules and proteins
    if any(x in prop for x in ['molecule', 'protein', 'peptide', 'amino acid']):
        return 'Small molecules & proteins'

    # DNA/RNA structures 
    elif any(x in prop for x in [
        'dna', 'rna', 'nucleotide', 'chromosome', 'chromatid',
        'chromatin', 'nucleosome'
    ]):
        return 'DNA/RNA structures'

    # Nucleus/Nuclear structures
    elif any(x in prop for x in ['nucleus', 'nuclei', 'nuclear']):
        return 'Nuclei'

    # Cell organelles
    elif any(x in prop for x in [
        'organelle', 'mitochondria', 'chloroplast',
        'vesicle', 'ribosome', 'membrane', 'endoplasmic',
        'periplasm', 'cytoplasm', 'envelope',
        'golgi', 'lysosome', 'vacuole'
    ]):
        return 'Cell organelles'

    # Individual cells
    elif ('cell' in prop and not any(x in prop for x in ['tissue', 'organ'])) or \
         any(x in org for x in ['bacteria', 'coli']):
        return 'Cells'

    # Tissues and larger structures
    elif any(x in prop for x in ['tissue', 'organ', 'skin', 'muscle']):
        return 'Tissues & organs'

    return 'Other'


def debug_categorization(size_data):
    """Print sample entries from each category to verify categorization and standardization"""
    print("\n=== DEBUG: Sample Entries by Category ===")
    
    # Sort by standardized value or min value within each category
    size_data_sorted = size_data.sort_values(
        by=['standardized_value', 'standardized_min'],
        na_position='last'
    )
    
    for category in size_data['category'].unique():
        print(f"\n{category}:")
        samples = size_data_sorted[size_data_sorted['category'] == category].head(5)
        for _, row in samples.iterrows():
            print(f"- {row['Properties']} (ID: {row['bion_id']})")
            print(f"  Original Value: {row['original_value']}")
            print(f"  Original Range: {row['original_range']}")
            
            if pd.notna(row['value']):
                print(f"  Value: {row['value']} {row['Units']}")
                print(f"  Standardized: {row['standardized_value']} meters")
            elif pd.notna(row['min_value']):
                print(f"  Range: {row['min_value']} - {row['max_value']} {row['Units']}")
                print(f"  Standardized: {row['standardized_min']} - {row['standardized_max']} meters")
            
            if pd.notna(row['Organism']):
                print(f"  Organism: {row['Organism']}")
            print()


def main():
    # Load data
    filepath = "bionumbers/samples/raw_full_BioNumbers.xls"
    df = load_bionumbers_data(filepath)

    # Process and clean the data
    size_data = clean_size_data(df)

    # Debug categorization
    debug_categorization(size_data)

    # Sort by Organism and save processed data with today's date
    size_data_sorted = size_data.sort_values(['Organism', 'standardized_min'])
    today = date.today().strftime("%Y_%m_%d")
    output_path = f"./bionumbers/output/processed_size_data_{today}.csv"
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
