#!/usr/bin/env python3

import subprocess
import json
import pandas as pd
from datetime import date
import argparse
import logging
from pathlib import Path
import sys
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', f'genome_data_{date.today().strftime("%Y_%m_%d")}.log')),
        logging.StreamHandler(sys.stdout)
    ]
)


#
# Note (Ashish): This is used to map taxon names to NCBI taxon IDs.
# The script ignores this if --taxon-id is provided by the user.
#
TAXON_ID_MAP = {
    'bacteria': 2,
    'archaea': 2157,
    'metazoa': 33208,          # multicellular animals
    'viridiplantae': 33090,    # plants
    'fungi': 4751,
    'viruses': 10239
}


def setup_directories():
    """Create necessary directories if they don't exist."""
    for dir_name in ['output', 'logs']:
        Path(dir_name).mkdir(exist_ok=True)


def check_datasets_installation():
    """Verify that the NCBI datasets tool is installed."""
    try:
        result = subprocess.run(['datasets', '--version'], 
                              capture_output=True, 
                              text=True)
        logging.info(f"NCBI datasets version: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        logging.error("NCBI datasets tool not found. Please install it first.")
        return False


def query_genome_data(taxon_id):
    """Query NCBI datasets for genome data."""
    cmd = [
        'datasets', 'summary', 'genome', 
        'taxon', str(taxon_id),
        '--assembly-level', 'chromosome,complete',
        '--as-json-lines'
    ]
    
    logging.info(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Error querying NCBI: {result.stderr}")
            return None
            
        # Parse JSON lines output
        data = []
        for line in result.stdout.splitlines():
            if line.strip():
                try:
                    entry = json.loads(line)
                    # Only process entries that have assembly info
                    if 'assembly_info' in entry:
                        data.append(entry)
                except json.JSONDecodeError as e:
                    logging.warning(f"Failed to parse JSON line: {e}")
                    continue
        
        logging.info(f"Retrieved {len(data)} genome entries")
        return data
    except Exception as e:
        logging.error(f"Error processing NCBI data: {e}")
        return None


def process_genome_data(raw_data):
    """Process and clean the genome data."""
    if not raw_data:
        return pd.DataFrame()
        
    # Extract relevant fields
    processed_data = []
    for entry in raw_data:
        try:
            # Get assembly info
            assembly_info = entry.get('assembly_info', {})
            assembly_stats = entry.get('assembly_stats', {})
            organism_info = entry.get('organism', {})
            checkm_info = entry.get('checkm_info', {})
            
            processed_entry = {
                'assembly_accession': entry.get('accession'),
                'assembly_name': assembly_info.get('assembly_name'),
                'organism_name': organism_info.get('organism_name'),
                'organism_taxonomic_id': organism_info.get('tax_id'),
                'assembly_release_date': assembly_info.get('release_date'),
                'assembly_release_year': assembly_info.get('release_date').split('-')[0],
                'checkm_completeness': checkm_info.get('completeness'),
                'checkm_completeness_percentile': checkm_info.get('completeness_percentile'),
                'checkm_contamination': checkm_info.get('contamination'),
                'checkm_version': checkm_info.get('checkm_version'),
                'checkm_marker_count': checkm_info.get('marker_count')
            }
            processed_data.append(processed_entry)
        except Exception as e:
            logging.warning(f"Error processing entry: {e}")
            continue
            
    # Convert to DataFrame
    df = pd.DataFrame(processed_data)
    
    # Remove duplicates
    df_dedup = df.drop_duplicates(subset=['organism_taxonomic_id'])
    logging.info(f"Removed {len(df) - len(df_dedup)} duplicate entries")
    
    # Add collection timestamp
    df_dedup['collection_date'] = date.today().strftime("%Y-%m-%d")
    
    return df_dedup


def generate_cumulative_analysis(output_dir: str):
    """Generate cumulative analysis of genome sequencing over time."""
    logging.info(f"Generating cumulative analysis for {output_dir}")
    
    # Get all genome data files in the directory
    genome_files = list(Path(output_dir).glob("genome_data_*.csv"))
    if not genome_files:
        logging.warning(f"No genome data files found in {output_dir}")
        return
        
    # Read and process each file
    data_frames = {}
    for file_path in genome_files:
        # Extract organism name from filename (e.g., genome_data_archaea_2025_01_26.csv -> archaea)
        organism = file_path.stem.split('_')[2]
        df = pd.read_csv(file_path)
        data_frames[organism] = df
    
    # Find the year range
    min_year = float('inf')
    max_year = 0
    for df in data_frames.values():
        if 'assembly_release_year' in df.columns:
            years = pd.to_numeric(df['assembly_release_year'], errors='coerce')
            min_year = min(min_year, years.min())
            max_year = max(max_year, years.max())
    
    # Create year range from 1980 or earliest year to latest year
    start_year = min(min_year, 1980)
    year_range = range(int(start_year), int(max_year) + 1)
    
    # Initialize results DataFrame with years as index
    results = pd.DataFrame(index=year_range)
    
    # Calculate cumulative counts for each organism
    for organism, df in data_frames.items():
        if 'assembly_release_year' in df.columns:
            # Count genomes per year
            yearly_counts = df['assembly_release_year'].value_counts()
            # Convert to cumulative sum
            cumulative = pd.Series(0, index=year_range)
            for year in year_range:
                if year in yearly_counts.index:
                    cumulative[year] = yearly_counts[year]
            results[organism] = cumulative.cumsum()
    
    # Sort index (years) and fill any missing values with previous value (or 0)
    results = results.sort_index().fillna(method='ffill').fillna(0)
    
    # Save results
    results.to_csv(Path(output_dir) / 'results.csv')
    logging.info(f"Saved cumulative analysis to {output_dir}/results.csv")
    
    return results


def fetch_and_save_taxon_data(
    taxon_id: str,
    taxon_name: str,
    output_dir: str
):  
    raw_data = query_genome_data(taxon_id)
    df = process_genome_data(raw_data)
    today = date.today().strftime("%Y_%m_%d")
    
    # Create date-specific output directory
    date_output_dir = Path(output_dir) / today
    date_output_dir.mkdir(exist_ok=True)
    
    output_path = date_output_dir / f"genome_data_{taxon_name}_{today}.csv"
    df.to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser(description='Download and process NCBI genome data')
    parser.add_argument('--taxon-id', type=int, required=False,
                      help='Taxon ID to query (e.g., 10239 for viruses). If missing, all taxons will be queried.')
    parser.add_argument('--taxon-name', type=str, required=False,
                      help='Taxon name to query (e.g., viruses). This is ignored if --taxon-id is missing.')
    parser.add_argument('--output-dir', type=str, default='output',
                      help='Directory for output files')
    parser.add_argument('--cumulative-analysis', action='store_true',
                      help='Generate cumulative analysis of genome sequencing over time')
    
    args = parser.parse_args()

    today = date.today().strftime("%Y_%m_%d")
    date_output_dir = Path(args.output_dir) / today
    date_output_dir.mkdir(exist_ok=True)

    if args.cumulative_analysis:
        generate_cumulative_analysis(date_output_dir)
        return

    # Setup
    setup_directories()
    if not check_datasets_installation():
        return
        
    # Query and process data
    if args.taxon_id:
        logging.info(f"Querying genome data for taxon {args.taxon_id}")
        fetch_and_save_taxon_data(args.taxon_id, TAXON_ID_MAP[args.taxon_name], args.output_dir)
    else:
        logging.info(f"Querying genome data for all taxons")
        for taxon_name, taxon_id in TAXON_ID_MAP.items():
            fetch_and_save_taxon_data(taxon_id, taxon_name, args.output_dir)
    
    # Generate cumulative analysis
    generate_cumulative_analysis(date_output_dir)


if __name__ == "__main__":
    main()
