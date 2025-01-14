import pandas as pd
import numpy as np
import re
from util import (
    load_bionumbers_data,
    extract_numeric_value,
    standardize_units
)


def clean_size_data(df):
    """Extract and clean size-related measurements"""
    # Expanded keywords related to size measurements
    size_keywords = [
        'length', 'diameter', 'volume', 'size', 'radius',
        'thickness', 'width', 'surface area', 'cross section',
        'dimensions', 'axes'
    ]
    
    # Properties to exclude (false positives)
    exclude_keywords = [
        'rate', 'constant', 'time',I 'energy', 'force',
        'concentration', 'abundance', 'number'
    ]
    
    # Filter for size-related properties
    mask = (
        df['Properties'].str.lower().str.contains('|'.join(size_keywords), na=False) &
        ~df['Properties'].str.lower().str.contains('|'.join(exclude_keywords), na=False)
    )
    size_data = df[mask].copy()
    
    # Process values and ranges
    size_data['numeric_value'] = size_data.apply(
        lambda row: extract_numeric_value(row['Value'] if pd.notna(row['Value']) else row['Range']),
        axis=1
    )
    
    # Standardize units
    size_data['standardized_value'] = size_data.apply(
        lambda row: standardize_units(row['numeric_value'], row['Units']),
        axis=1
    )
    
    # Add category for scale
    size_data['category'] = size_data.apply(categorize_scale, axis=1)
    
    return size_data[['bion_id', 'Properties', 'Organism', 'numeric_value', 
                     'standardized_value', 'Units', 'category']]


def categorize_scale(row):
    """Categorize biological entities based on their size and properties"""
    prop = row['Properties'].lower()
    org = str(row['Organism']).lower() if pd.notna(row['Organism']) else ''
    
    # Small molecules and proteins
    if any(x in prop for x in ['molecule', 'protein', 'peptide', 'amino acid']):
        return 'Small molecules & proteins'
    
    # DNA/RNA structures
    elif any(x in prop for x in ['dna', 'rna', 'nucleotide', 'chromosome']):
        return 'DNA/RNA structures'
    
    # Cell organelles
    elif any(x in prop for x in [
        'organelle', 'mitochondria', 'nucleus', 'chloroplast',
        'vesicle', 'ribosome', 'membrane', 'endoplasmic'
    ]):
        return 'Cell organelles'
    
    # Cells
    elif 'cell' in prop or any(x in org for x in ['bacteria', 'coli']):
        return 'Cells'
    
    # Tissues and larger structures
    elif any(x in prop for x in ['tissue', 'organ', 'skin', 'muscle']):
        return 'Tissues & organs'
    
    return 'Other'


def main():
    # Load data
    filepath = "bionumbers/sample.csv"
    df = load_bionumbers_data(filepath)
    
    # Process and clean the data
    size_data = clean_size_data(df)
    
    # Save processed data
    size_data.to_csv("processed_size_data.csv", index=False)
    
    # Print summary
    print("\nData Summary:")
    print(f"Total entries: {len(size_data)}")
    print("\nEntries by category:")
    print(size_data['category'].value_counts())

if __name__ == "__main__":
    main()
