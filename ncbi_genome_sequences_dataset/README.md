## NCBI Genome Dataset

This script uses the NCBI Datasets CLI tool to download genome data for different taxa, focusing on high-quality assemblies (chromosome or complete level). The data is used in various bio-data related briefs and projects from Asimov Press.

### Prerequisites

The script requires the NCBI `datasets` command-line tool, [you can find instructions here](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/download-and-install/).

If you are e.g. on a Mac, move the `datasets` executable to `/usr/local/bin/` and make sure it is executable (`chmod +x datasets`).

Verify installation with:
```bash
datasets --version
```

### Data Collection

The script collects genome data with the following filters:
- Specific taxon IDs (e.g., 10239 for viruses)
- Assembly level: Only 'chromosome' or 'complete' assemblies
  - Excludes 'contig' and 'scaffold' level assemblies
- Deduplicates entries by organism taxonomic ID

### Steps

1. Query NCBI Datasets API for genome metadata
2. Filter and clean the data:
   - Remove duplicate entries
   - Standardize fields
   - Add metadata (collection date, processing date)
3. Save processed data to CSV files in the `output/` folder

### Output

The output is a timestamped CSV file within the `output/` folder containing fields like:
- Genome ID
- Organism name
- Assembly level
- Release date
- Genome length
- GC percent

### Usage

For the full data collection and analysis which uses our stored mapping of taxon names to IDs, run
```bash
python gen_genome_data.py
``` 

To pick a specific taxon (by `id` and `name`), run:
```bash
python gen_genome_data.py --taxon-id 10239 --taxon-name viruses
``` 

The data will be stored under `output/` in a subdirectory named after today's date.

The `results.csv` file contains the cumulative analysis of genome sequencing over time, broken down by taxon.

Note that you can also just get the cumulative analysis of the data from today's date by running:
```bash
python gen_genome_data.py --cumulative-analysis
``` 
