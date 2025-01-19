# Bio-Data Datasets & Data Pipelines

This may still be a little janky but we're starting small and evolving over time. This repository contains datasets used in various bio-data related briefs and projects from Asimov Press.

Each folder is grouped by dataset, and shared code / scripts go into the [shared](./shared) folder.

Datasets are either purely automated, part curated, or fully curated. Each one should be self-contained and have a README.md with more information about what it is, how the data was generated, etc. so others can reproduce it.

## Sources

### Cell Volume and Size

Our first data brief is based on volumetric measurements of cells and components of cells. We use the [Bionumbers](https://book.bionumbers.org/) dataset to get the information we need.

So [cell volume](./cell_volume_dataset) and [cell size](./cell_size_dataset) are both based on the same source, which you can find within the [shared](./shared) folder.