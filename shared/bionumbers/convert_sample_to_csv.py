import pandas as pd
import os

def convert_sample_to_csv():
    """Convert the sample Excel file to CSV format"""
    input_path = "shared/bionumbers/samples/raw_full_BioNumbers.xls"
    output_path = "shared/bionumbers/samples/raw_full_BioNumbers.csv"
    
    print(f"Reading Excel file from: {input_path}")
    
    # Read the Excel file
    try:
        df = pd.read_excel(input_path)
        print(f"Successfully read {len(df)} rows")
        
        # Basic data validation
        print("\nDataframe Info:")
        print(df.info())
        
        print("\nSample of first few rows:")
        print(df.head())
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"\nSaved CSV file to: {output_path}")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        
        # Try reading as HTML if Excel fails
        print("\nAttempting to read as HTML...")
        df = pd.read_html(input_path)[0]
        print(f"Successfully read {len(df)} rows from HTML")
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"Saved CSV file to: {output_path}")

if __name__ == "__main__":
    convert_sample_to_csv() 