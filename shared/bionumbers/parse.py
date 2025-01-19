import pandas as pd
from shared.util import (
    load_bionumbers_data,
    extract_numeric_value,
    standardize_units
)


def parse_property(prop_str):
    """Parse property string into type and description"""
    if pd.isna(prop_str):
        return None, None
    
    # Handle "Rule of thumb" cases
    if 'rule of thumb' in prop_str.lower():
        # Find the part after "rule of thumb"
        parts = prop_str.lower().split('rule of thumb')
        if len(parts) > 1:
            return '"Rule of thumb"', parts[1].strip(' :for').strip()
    
    # Handle normal "X of Y" cases
    parts = prop_str.split(' of ', 1)  # Split on first occurrence of 'of'
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    
    return prop_str.strip(), None


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


def clean_size_data(
    df,
    cell_volume_only=False,
    general_size_only=True
):
    """Extract and clean size-related measurements"""
    if cell_volume_only and general_size_only:
        raise ValueError("Cannot set both cell_volume_only and general_size_only to True")
    
    # Expanded keywords related to size measurements
    size_keywords = [
        'cell volume', 'volume of'
    ] if cell_volume_only else [
        'length', 'diameter', 'volume', 'size', 'radius',
        'width', 'surface area', 'cross section',
        'dimensions', 'axes', 'rule of thumb'
    ] if general_size_only else []

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
        'peak in', 'oscillations', 'in the following organisms', 'atp demand', 'mechanoelectrical sensitivity',
        'pool turnover'
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
    
    # Parse property strings
    property_parts = size_data['Properties'].apply(parse_property)
    size_data['property_type'] = property_parts.apply(lambda x: x[0])
    size_data['property_of'] = property_parts.apply(lambda x: x[1])

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

    return size_data[[
        'bion_id', 'Properties', 
        'property_type', 'property_of',  # New columns
        'Organism', 
        'value',
        'min_value', 'max_value',
        'Units',
        'standardized_value',
        'standardized_min', 'standardized_max',
        'category',
        'original_value', 'original_range'
    ]]