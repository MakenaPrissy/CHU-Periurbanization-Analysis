#descriptive tables script
from pathlib import Path
import pandas as pd


INTERIM_DIR = Path("data/interim")
RESULTS_DIR = Path("results/tables")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def summarize_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    d = df[df["year"] == year].copy()
    numeric_cols = d.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["chu_id", "year"]]

    rows = []
    for col in numeric_cols:
        s = d[col].dropna()
        if len(s) == 0:
            continue
        rows.append(
            {
                "variable": col,
                "year": year,
                "n": int(s.count()),
                "mean": float(s.mean()),
                "sd": float(s.std()),
                "median": float(s.median()),
                "min": float(s.min()),
                "max": float(s.max()),
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    panel_path = INTERIM_DIR / "chu_proxy_panel.csv"
    df = pd.read_csv(panel_path)

    years = sorted(df["year"].dropna().unique().tolist())
    if not years:
        raise ValueError("No years found in panel data.")

    baseline = years[0]
    endline = years[-1]

    baseline_tbl = summarize_year(df, baseline)
    endline_tbl = summarize_year(df, endline)
    combined = pd.concat([baseline_tbl, endline_tbl], ignore_index=True)

    baseline_tbl.to_csv(RESULTS_DIR / f"table_baseline_{baseline}.csv", index=False)
    endline_tbl.to_csv(RESULTS_DIR / f"table_endline_{endline}.csv", index=False)
    combined.to_csv(RESULTS_DIR / "table_baseline_endline_summary.csv", index=False)

    print("Saved descriptive summary tables.")
    print(combined.head())
