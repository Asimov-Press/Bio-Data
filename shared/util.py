import pandas as pd
import numpy as np
import re
import os


def load_bionumbers_data(
    filepath: str = "shared/bionumbers/samples/raw_full_BioNumbers.xls"
):
    """Load the Bionumbers data from file (supports Excel and HTML formats)"""
    try:
        # First try reading as Excel
        print(f"Loading Bionumbers data from {os.path.join(os.getcwd(), filepath)}")
        return pd.read_excel(
            os.path.join(
                os.getcwd(),
                filepath
            )
        )
    except Exception as e:
        print(f"Warning: Could not read as Excel file ({e})")
        print("Attempting to read as HTML...")
        # Try reading as HTML table and set the first row as headers
        df = pd.read_html(filepath)[0]
        # Set the first row as column headers
        df.columns = df.iloc[0]
        # Remove the first row since it's now the header
        df = df.iloc[1:].reset_index(drop=True)
        return df


def extract_numeric_value(value_str):
    """Extract numeric values from string, handling ranges and single values"""
    if pd.isna(value_str):
        return None
        
    # Convert to string and clean up
    value_str = str(value_str)
    
    # Remove URLs if present (anything starting with 'http' or containing '.pdf', etc)
    value_str = re.sub(r'https?://\S+|www\.\S+|\S+\.pdf', '', value_str)
    
    # Look for common range patterns
    range_patterns = [
        # Handle "X - Y" or "X-Y" format
        r'(\d*\.?\d+)\s*-\s*(\d*\.?\d+)',
        # Handle "X to Y" format
        r'(\d*\.?\d+)\s*to\s*(\d*\.?\d+)'
    ]
    
    for pattern in range_patterns:
        match = re.search(pattern, value_str)
        if match:
            try:
                num1 = float(match.group(1))
                num2 = float(match.group(2))
                return (min(num1, num2), max(num1, num2))
            except (ValueError, AttributeError):
                continue
    
    # If no range found, look for single numbers
    # Avoid capturing numbers that might be years or other irrelevant numbers
    numbers = re.findall(r'(?<!\d)(\d*\.?\d+)(?!\d)', value_str)
    if numbers:
        try:
            # If single number or multiple numbers but not a range, take the first clear number
            return float(numbers[0])
        except ValueError:
            return None
            
    return None


def normalize_unit(unit_str):
    """Normalize unit string to handle different micro symbols and other variations"""
    if pd.isna(unit_str):
        return unit_str

    # First replace micro symbols while preserving case
    unit = unit_str.replace('μ', 'µ')     # Standard micro
    unit = unit.replace('Î¼', 'µ')        # Corrupted micro
    
    # Now convert to lowercase and strip whitespace
    unit = unit.lower().strip()
    
    # Replace 'u' with 'µ' only at the start of unit or after a separator
    unit = re.sub(r'(^|[\s/])u([m|g|l])', r'\1µ\2', unit)
    
    # Remove any spaces before units
    unit = re.sub(r'\s+([²³]|sec|min|hr|/)', r'\1', unit)
    
    # Standardize superscripts
    unit = unit.replace('^2', '²')
    unit = unit.replace('^3', '³')
    
    # Debug output
    if unit_str != unit:
        print(f"Normalized unit: '{unit_str}' -> '{unit}'")
        
    return unit


def standardize_units(value, unit):
    """Convert measurements to standard units (meters or cubic meters)"""
    if pd.isna(value) or pd.isna(unit):
        return None

    unit = normalize_unit(unit)

    # Expanded unit conversion factors
    conversion = {
        # Length units
        'µm': 1e-6,
        'nm': 1e-9,
        'mm': 1e-3,
        'cm': 1e-2,
        'm': 1.0,
        # Volume units
        'µm³': 1e-18,
        'nm³': 1e-27,
        'mm³': 1e-9,
        'cm³': 1e-6,
        'm³': 1.0,
        'µl': 1e-9,    # 1 µL = 1 mm³ = 1e-9 m³
        'ml': 1e-6,    # 1 mL = 1 cm³ = 1e-6 m³
        'l': 1e-3,     # 1 L = 1e-3 m³
        # Area units
        'µm²': 1e-12,
        'nm²': 1e-18,
        'mm²': 1e-6,
        'cm²': 1e-4,
        'm²': 1.0,
        # Mass units (if needed)
        'fg': 1e-15,
        'pg': 1e-12,
        'ng': 1e-9,
        'µg': 1e-6,
        'mg': 1e-3,
        'g': 1.0
    }

    if unit in conversion:
        return value * conversion[unit]
    return value
