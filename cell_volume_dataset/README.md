## Overview

This script extracts information from the raw Bionumbers dataset for use in various datasets for our project.

The raw dataset is [available here](https://bionumbers.hms.harvard.edu/resources.aspx).

### Biological Sizes

Plot showing various sizes of biological molecules, all the way up through cells or collections of cells. The “sizes” of various things in biology, plotted in a single chart (perhaps as volumes).

### Script Overview

- `raw_data_qa.py`: Basic QA on the raw data. The file was XLS but we had to read it as HTML.
- `gen_biological_sizes.py`: Generates a cleaned dataset of biological sizes for use in our first data brief.

Here's how we cleaned the data:
- We filtered for properties that were likely to be sizes (with both inclusion and exclusion lists).
- We extracted numeric values and standardized units.
    - Note that some rows had a value, and/or a range. We pull both out where available into the `value` and `min_value` / `max_value` columns.
- We saved the cleaned data to a CSV file within the `output/`.