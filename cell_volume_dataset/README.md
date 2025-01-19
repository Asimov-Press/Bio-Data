## Cell Volume Dataset

This script takes the raw Bionumbers dataset and pulls out two sets of volume information:
- Volume of things within a cell, in this case with a focus on E. coli.
- Volume of different cells themselves across different organisms.

The main [script](./gen_cell_volumes.py) is used to generate the data for our first data brief.

We also used a script to analyze [E. Coli volume data](./analyze_ecoli_volumes.py) and cross-organism [Cell Volume data](./analyze_cell_volumes.py) to get a sense of what we had available.

### Steps

- Filter for keywords related to volume.
- Use an exclusion list to remove any false positives.
- Clean the data / units:
    - Pull out the primary value, or the range if available.
    - Convert to a standard unit.
- Save the cleaned data to a CSV file within the `output/` folder.

### Output

The output is a timestamped CSV file within the `output/` folder.
