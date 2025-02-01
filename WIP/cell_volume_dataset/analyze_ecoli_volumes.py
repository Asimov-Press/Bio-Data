import pandas as pd
from prettytable import PrettyTable
import glob
import os

def get_latest_output_file():
    """Get the most recent output file from the output directory"""
    output_dir = "./cell_volume_dataset/output/"
    files = glob.glob(os.path.join(output_dir, "processed_cell_volume_data_*.csv"))
    if not files:
        raise FileNotFoundError("No output files found")
    return max(files, key=os.path.getctime)

def analyze_ecoli_data():
    # Load the latest data file
    latest_file = get_latest_output_file()
    df = pd.read_csv(latest_file)
    
    # Filter for E. coli and Generic data
    mask = (df['Organism'].isin(['Bacteria Escherichia coli', 'Generic']))
    filtered_data = df[mask].copy()
    
    # Apply additional filters
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
    filtered_data = filtered_data[mask]
    
    # Sort by organism first, then by property type and values
    filtered_data = filtered_data.sort_values(
        by=['Organism', 'property_type', 'standardized_value', 'standardized_min'],
        na_position='last'
    )
    
    # Create table
    table = PrettyTable()
    table.field_names = [
        "Property Type",
        "Property Of",
        "Value",
        "Min",
        "Max", 
        "Units"
    ]
    
    # Configure table appearance
    table.align = "l"  # Left align text
    table.max_width = 40  # Limit column width
    
    # Add data rows
    for _, row in filtered_data.iterrows():
        table.add_row([
            str(row['property_type'])[:40],
            str(row['property_of'])[:40],
            row['value'] if pd.notna(row['value']) else '',
            row['min_value'] if pd.notna(row['min_value']) else '',
            row['max_value'] if pd.notna(row['max_value']) else '',
            row['Units']
        ])
    
    # Print summary
    print("\nVolume Measurements:")
    print(f"Total entries: {len(filtered_data)}")
    print("\nBreakdown by organism:")
    print(filtered_data['Organism'].value_counts())
    print("\nBreakdown by category:")
    print(filtered_data['category'].value_counts())
    print("\nDetailed measurements:")
    print(table)

if __name__ == "__main__":
    analyze_ecoli_data() 