# Classifying Peri-Urban Transition at Community Health Unit Level Using Multiple Geospatial Proxies in Coastal Kenya

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository contains the full reproducible analysis code for:

> Makena P, Oluoch F, Ondiek RI, Gudda F, Keter A, Das J, Bhutta Z, Ngugi A.
> *Classifying peri-urban transition at Community Health Unit level using multiple geospatial proxies in coastal Kenya.*

---

## Study Overview

We conducted a longitudinal ecological analysis across **10 Community Health Units (CHUs)** in Kilifi County, Kenya (Kaloleni-Rabai Health and Demographic Surveillance System, KRHDSS), with annual observations from **2017 to 2024**.

Five publicly available geospatial proxy indicators were summarized within CHU boundaries:
- **VIIRS nighttime lights** – mean annual radiance
- **Sentinel 2 built-up area** – % of CHU area classified as built-up
- **WorldPop built-up area** – % of CHU area classified as built-up
- **WorldPop population density** – mean persons per km²
- **Degree of Urbanisation (GHS-SMOD)** – % of CHU area classified as urban

Key analyses:
1. Baseline and endline summary statistics (2017 vs 2024)
2. Year-to-year and cumulative percent change
3. Pearson correlations between proxy pairs
4. K-means consensus classification (peri-urban vs rural)

---

## Repository Structure

```
.
├── data/
│   ├── raw/
│   └── interim/
├── results/
│   ├── figures/
│   └── tables/
├── src/
│   ├── 01_build_panel.py
│   ├── 02_descriptive_tables.py
│   ├── 03_change_metrics.py
│   ├── 04_correlations.py
│   ├── 05_clustering_consensus.py
│   └── 06_make_figures.py
├── run_all.py
├── requirements.txt
├── environment.yml
└── LICENSE
```

---

## Data

Proxy values were extracted in **QGIS 3.28.3** using zonal statistics on CHU boundary polygons and exported as CSV files. Place these in `data/raw/`:

| File | Source | Description |
|------|--------|-------------|
| `viirs_nighttime_lights.csv` | [VIIRS/NPP](https://www.earthdata.nasa.gov/) | Mean annual radiance per CHU |
| `sentinel2_builtup.csv` | [ESA WorldCover / DLR](https://livingatlas.arcgis.com/landcover/) | % built-up area per CHU |
| `worldpop_builtup.csv` | [WorldPop](https://www.worldpop.org/) | % built-up area per CHU |
| `worldpop_popdens.csv` | [WorldPop](https://www.worldpop.org/) | Mean pop density per CHU |
| `ghssmod_urban_pct.csv` | [GHS-SMOD](https://ghsl.jrc.ec.europa.eu/ghs_smod2023.php) | % urban area per CHU |

Each raw file must have columns: `CHU_name`, `year`, `value`.

See `data/raw/README_data.md` for full data dictionary.

---

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/<your-org>/chu-periurban-classification.git
cd chu-periurban-classification
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add data
Place your raw CSV files in `data/raw/` following the naming conventions above.

### 4. Run the full pipeline
```bash
python scripts/00_data_preparation.py
python scripts/01_descriptive.py
python scripts/02_change_metrics.py
python scripts/03_correlations.py
python scripts/04_clustering.py
python scripts/05_figures.py
```

Or explore interactively in the Jupyter notebook:
```bash
jupyter notebook notebooks/analysis_walkthrough.ipynb
```

---

## Software

- Python 3.10
- QGIS 3.28.3 (for spatial pre-processing, not scripted here)
- See `requirements.txt` for full Python dependencies

---

## Citation and archive

The first archived release of this repository is available on Zenodo:

DOI: https://doi.org/10.5281/zenodo.19200614

If you use this repository, please cite the Zenodo record associated with the release.

## License and data use

The code in this repository is licensed under the MIT License. See the `LICENSE` file for details.

Data files are included only where sharing is permitted. Some data associated with this project may be subject to access controls, institutional permissions, or ethical restrictions. Reuse of data is the responsibility of the user and should comply with the relevant data governance requirements.  

MIT License. See [LICENSE](LICENSE).
