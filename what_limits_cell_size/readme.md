# What is a Cell Made From?

_We have collected a variety of datasets that break down diffusion rates for various proteins in the E. coli proteome, and also the sizes of cells in the human body. These datasets come from multiple different sources, as described below._

---

## Table of Contents

- [Datasets](#datasets)
  - [Dataset 1: *Experimentally-determined diffusion rates of various proteins*](#bellotto_diffusion.csv)
  - [Dataset 2: *Calculated diffusion rates for the E. coli proteome*](#Diffusion_Rates_with_kDa.csv)
  - [Dataset 3: *Size of Various Human Cells*](#Human Cell Sizes.xlsx)
- [Data Sources](#data-sources)
- [Contact](#contact)

---

## Project Overview

The datasets in this folder were collected for an Asimov Press article entitled: "What Limits a Cell's Size?"

---

## Datasets

This section describes the datasets used in this project.

### Dataset 1: *Experimentally-determined diffusion rates of various proteins*

- **Description:**  
  This dataset includes the measured diffusion rate and size of sfGFP fusion proteins. Diffusion rates were measured, and reported, with both FCS and FRAP.
- **Source:**  
  [Bellotto _et al_ (2022)](https://elifesciences.org/articles/82654)  
- **Format:**  
  CSV
- **License:**  
  Creative Commons Attribution License.

### Dataset 2: *Calculated diffusion rates for the E. coli proteome*

- **Description:**  
  This tidy dataset breaks down the _calculated_ (not experimentally measured) diffusion rates for a subset of proteins in _E. coli_. kDa values are not present in the original dataset. All kDa values were scraped from the UniProt database, using Python, and then appended to the Kalwarczyk dataset.
- **Source:**  
  [Kalwarczyk T _et al_ (2012)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3496334/)  
- **Format:**  
  CSV
- **License:**
  Creative Commons Attribution License

### Dataset 3: *Size of Various Human Cells*

- **Description:**  
  A small dataset showing the volumes of various types of human cells, as pulled from the Bionumbers book.
- **Source:**  
  [BioNumbers](https://book.bionumbers.org/how-big-is-a-human-cell/)  
- **Format:**  
  Excel file

---

## Contact

Please email editors@asimov.com if you have any questions.