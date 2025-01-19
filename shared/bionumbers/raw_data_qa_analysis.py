import pandas as pd

def detect_file_format(filepath):
    """Detect the actual file format by reading the first few bytes"""
    with open(filepath, 'rb') as f:
        header = f.read(8)
        
    # Check for common file signatures
    if header.startswith(b'PK\x03\x04'):  # XLSX file
        return 'xlsx'
    elif header.startswith(b'\xD0\xCF\x11\xE0'):  # XLS file
        return 'xls'
    elif header.startswith(b'\r\n') or header.startswith(b'<'):  # Likely HTML/Text
        return 'html'
    return 'unknown'


def save_unique_properties(df):
    """Save unique Properties values to a text file, sorted alphabetically"""
    unique_props = df['Properties'].unique()
    
    output_path = "bionumbers/qa/properties_list.txt"
    with open(output_path, 'w') as f:
        for prop in unique_props:
            if pd.notna(prop):  # Skip NaN values
                f.write(f"{prop}\n")
    
    print(f"\n=== Unique Properties ===")
    print(f"Saved {len(unique_props)} unique properties to {output_path}")


def analyze_raw_data():
    """Perform basic quality analysis on the raw BioNumbers dataset"""
    print("Loading raw BioNumbers data...")
    filepath = "bionumbers/samples/raw_full_BioNumbers.xls"
    
    file_format = detect_file_format(filepath)
    print(f"Detected file format: {file_format}")
    
    if file_format == 'html':
        # Try reading as HTML table
        df = pd.read_html(filepath)[0]
        # Set the first row as column headers
        df.columns = df.iloc[0]
        # Remove the first row since it's now the header
        df = df.iloc[1:].reset_index(drop=True)
    else:
        try:
            # Try reading as Excel
            df = pd.read_excel(filepath)
        except Exception as e:
            print(f"Error reading as Excel: {e}")
            print("Attempting to read as HTML...")
            df = pd.read_html(filepath)[0]
            # Set the first row as column headers
            df.columns = df.iloc[0]
            # Remove the first row since it's now the header
            df = df.iloc[1:].reset_index(drop=True)
    
    save_unique_properties(df)
    
    print("\n=== Basic Dataset Information ===")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print("\n=== Columns ===")
    for col in df.columns:
        non_null = df[col].count()
        pct_filled = (non_null / len(df)) * 100
        print(f"{col}: {pct_filled:.1f}% filled ({non_null} non-null values)")

    print("\n=== Sample Data (First 5 Rows) ===")
    print(df.head())

    print("\n=== Data Types ===")
    print(df.dtypes)

    print("\n=== Basic Statistics for Numeric Columns ===")
    print(df.describe())

    print("\n=== Value Counts for Selected Categorical Columns ===")
    categorical_columns = ['Organism', 'Units']
    for col in categorical_columns:
        if col in df.columns:
            print(f"\nTop 10 most common {col}:")
            print(df[col].value_counts().head(10))

def main():
    analyze_raw_data()

if __name__ == "__main__":
    main()
