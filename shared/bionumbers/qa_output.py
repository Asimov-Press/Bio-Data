import pandas as pd


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
            if pd.notna(row['property_of']):
                print(f"  Type: {row['property_type']}")
                print(f"  Of: {row['property_of']}")
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


def analyze_property_types(size_data):
    """Print distribution and examples of property types"""
    print("\n=== Property Type Distribution ===")
    
    # Get value counts and calculate percentages
    type_counts = size_data['property_type'].value_counts()
    type_percentages = (type_counts / len(size_data) * 100).round(1)
    
    # Print distribution
    print(f"\nFound {len(type_counts)} unique property types across {len(size_data)} entries")
    print("\nTop 20 most common property types:")
    for prop_type, count in type_counts.head(20).items():
        percentage = type_percentages[prop_type]
        print(f"{prop_type}: {count} ({percentage}%)")
        # Show a sample property for this type
        sample = size_data[size_data['property_type'] == prop_type]['Properties'].iloc[0]
        print(f"  Example: {sample}\n")


def analyze_property_details(size_data, property_type):
    """Analyze the distribution of property_of values for a given property type"""
    print(f"\n=== Analysis of '{property_type}' Properties ===")
    
    # Filter for the property type
    type_data = size_data[size_data['property_type'] == property_type]
    
    # Group by property_of and organism, count occurrences
    grouped = type_data.groupby(['property_of', 'Organism']).size().reset_index()
    grouped.columns = ['property_of', 'Organism', 'count']
    
    # Sort by count and property_of
    grouped = grouped.sort_values(['count', 'property_of'], ascending=[False, True])
    
    # Print summary
    print(f"\nFound {len(type_data)} total '{property_type}' measurements")
    print(f"Across {grouped['property_of'].nunique()} unique descriptions")
    print(f"For {grouped['Organism'].nunique()} different organisms")
    
    print("\nDistribution:")
    for prop_of in grouped['property_of'].unique():
        prop_data = grouped[grouped['property_of'] == prop_of]
        print(f"\n{prop_of}:")
        for _, row in prop_data.iterrows():
            print(f"  {row['Organism']}: {row['count']} measurements")
