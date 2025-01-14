import pandas as pd
import numpy as np
import re


def load_bionumbers_data(filepath):
    """Load the Bionumbers data from CSV"""
    return pd.read_csv(filepath, delimiter='\t')


def extract_numeric_value(value_str):
    """Extract numeric values from string, handling ranges and single values"""
    if pd.isna(value_str):
        return None
    # Extract numbers using regex
    numbers = re.findall(r'[-+]?\d*\.?\d+', str(value_str))
    if numbers:
        # If multiple numbers, take the average
        return sum(float(x) for x in numbers) / len(numbers)
    return None



def standardize_units(value, unit):
    """Convert measurements to standard units (meters or cubic meters)"""
    if pd.isna(value) or pd.isna(unit):
        return None
    
    unit = unit.lower().strip()
    
    # Expanded unit conversion factors
    conversion = {
        # Length units
        'µm': 1e-6,
        'μm': 1e-6,
        'nm': 1e-9,
        'mm': 1e-3,
        'cm': 1e-2,
        'm': 1.0,
        # Volume units
        'µm^3': 1e-18,
        'μm^3': 1e-18,
        'nm^3': 1e-27,
        'mm^3': 1e-9,
        'cm^3': 1e-6,
        'm^3': 1.0,
        # Area units
        'µm^2': 1e-12,
        'μm^2': 1e-12,
        'nm^2': 1e-18,
        'mm^2': 1e-6,
        'cm^2': 1e-4,
        'm^2': 1.0,
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