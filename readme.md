# VoronoiGro — Colony Voronoi analysis

Small toolkit to analyze simulated bacterial colonies with clustering and Voronoi-based scoring/visualization. The repository contains gro simulation configurations and a Python analyzer that reads simulation outputs, computes clusters and centroids, builds Voronoi diagrams, and exports visual results.

## Quick overview
- Project: VoronoiGro
- Purpose: cluster cells from gro simulation outputs, compute centroids per cluster and region scores using Voronoi tessellations, and plot results.
- Main analysis script: `data_analysis.py`

## Repository layout (relevant files)
- `colony.gro` — gro simulation file (static scenario)
- `colony_with_growing.gro` — gro simulation file (growing scenario)
- `data_analysis.py` — main Python analysis routines (clustering, centroid extraction, Voronoi, plotting)
- `clustering_metric.py` — clustering metric utility
- `data/records_voronoi.csv` — example/input CSV used by the analyzer
- `results/` — output images and centroid text files produced by the analyzer
- `verilog.v` – Verilog code of the simplified circuit without Cas9 logic, used to test orthogonalization between components

## Expected CSV schema
The analyzer expects a CSV with one row per cell containing (typical gro export):
- id, x, y, theta, volume, gfp, rfp, yfp, cfp

Only `x, y` and optional fluorescence columns (`gfp`, `rfp`, `yfp`) are required for most analyses; adjust parsing in `data_analysis.py` if your format differs.

## Requirements
- Python 3.8+ recommended
- Core packages: numpy, scipy, scikit-learn, matplotlib, shapely, pandas
- Optional (for tests/metrics): `permetrics`

Install dependencies (Windows PowerShell example):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage
1. Place your simulation/export CSV into `data/` (named `Conteos.csv` or modify `data_analysis.py` to point to your file).
2. Run the analyzer:

```powershell
python data_analysis.py
```

The script will perform clustering (DBSCAN by default), compute centroids per cluster and build Voronoi regions, then save plots and centroid lists under `results/`.

## Configuration notes
- DBSCAN parameters (`eps`, `min_samples`) and plotting options are set inside `data_analysis.py`. Tweak them for your data density and units.
- The code uses Shapely + Matplotlib for geometry and plotting; adjust figure size / DPI if output images need higher resolution.

## Output
Typical outputs written to `results/`:
- centroid lists: `centroids_GFP.txt`, `centroids_RFP.txt`, `centroids_YFP.txt` (one file per channel if used)
- plots: `GFP_in_micrometers.png`, `RFP_in_micrometers.png`, `YFP_in_micrometers.png`, `voronoi_all.png`

## `clustering_metric.py` — clustering metric utility

`clustering_metric.py` is a small utility included to compute clustering quality metrics for a set of data / clustering labels. It uses the `permetrics` package (or scikit-learn metrics when `permetrics` is not available) to compute standard clustering comparisons and prints the results to the console.

Typical uses:
- Validate clustering parameters (e.g. DBSCAN `eps` / `min_samples`) on `data/Conteos.csv` or on synthetic/test data.
- Quick regression check to ensure clustering behaviour remains consistent after code changes.

Dependencies:
- `permetrics` (recommended) or `scikit-learn` (for fallback metrics)

Run example (PowerShell):

```powershell
# Run gro simulation
1- Open file with gro UI
2- Click on play button
3- The result should be in a csv file called "records_voronoi.csv"

# Generate diagram of voronoi to compare the result from gro simulation
1. python data_analysis.py
```

