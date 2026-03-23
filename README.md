# CHU-Periurbanization-Analysis
Reproducible code for analyzing periurbanization trajectories of community health units in Kenya using multiple urbanization proxies.

# Classifying peri-urban transition at Community Health Unit level using multiple geospatial proxies in coastal Kenya

This repository provides a reproducible analysis scaffold for the manuscript:

**Classifying peri-urban transition at Community Health Unit level using multiple geospatial proxies in coastal Kenya**

## Overview

The workflow mirrors the manuscript's core steps:

1. Harmonize Community Health Unit (CHU) by year proxy datasets
2. Merge all proxies into a single panel
3. Compute baseline, endline, absolute change, year to year percent change, and cumulative percent change
4. Estimate bootstrap confidence intervals for medians
5. Compute Pearson correlations for raw values and derived change metrics
6. Derive consensus peri-urban classification using proxy specific k means clustering and cross proxy vote scoring
7. Export tables and figures for manuscript reporting

## Repository structure

```text
chu_periurban_github_repo/
├── data/
│   ├── raw/                  # input proxy files and optional boundary files
│   └── derived/              # harmonized panel outputs
├── docs/                     # manuscript support docs
├── notebooks/                # optional exploratory notebooks
├── outputs/
│   ├── figures/              # exported figures
│   └── tables/               # exported tables
├── src/
│   ├── config.py
│   ├── utils.py
│   ├── 01_build_panel.py
│   ├── 02_descriptive_tables.py
│   ├── 03_change_metrics.py
│   ├── 04_correlations.py
│   ├── 05_clustering_consensus.py
│   └── 06_make_figures.py
├── .gitignore
├── environment.yml
├── requirements.txt
└── run_all.py
```

## Expected input data

The scripts assume annual CHU-level summaries already exist for the five proxies described in the manuscript:

- `night_lights.csv`
- `sentinel_built_up.csv`
- `worldpop_built_up.csv`
- `worldpop_density.csv`
- `degree_urbanisation.csv`

Each file should contain at minimum:

- `chu`
- `year`
- one value column for the relevant proxy

Recommended standardized value columns:

- `night_lights`
- `sentinel_built_pct`
- `worldpop_built_pct`
- `worldpop_density`
- `urban_pct`

## Notes on restricted data

The manuscript states that CHU boundary files are available through the KRHDSS data management process rather than being openly posted. For a public GitHub repository, do **not** upload restricted boundary files unless you have explicit permission. Instead:

- keep code public
- keep restricted boundaries out of the repository
- provide a data dictionary and instructions for approved users to place local files into `data/raw/`

## Quick start

```bash
conda env create -f environment.yml
conda activate chu-periurban
python run_all.py
```

## Outputs

The pipeline exports:

- harmonized panel dataset
- baseline and endline summary table
- availability table for percent change metrics
- cumulative change table
- year to year change table
- correlation tables
- consensus clustering table
- figure-ready CSVs and image files

## Citation

If you use this code, cite the manuscript and the original input data sources listed in the paper.
