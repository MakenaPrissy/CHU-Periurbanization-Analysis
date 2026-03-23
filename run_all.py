from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

scripts = [
    "01_build_panel.py",
    "02_descriptive_tables.py",
    "03_change_metrics.py",
    "04_correlations.py",
    "05_clustering_consensus.py",
    "06_make_figures.py",
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run([sys.executable, str(SRC / script)], check=True)

print("All steps completed.")
