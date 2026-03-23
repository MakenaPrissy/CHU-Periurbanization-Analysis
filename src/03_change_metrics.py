#change metrics script
from pathlib import Path
import numpy as np
import pandas as pd


INTERIM_DIR = Path("data/interim")
RESULTS_DIR = Path("results/tables")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def compute_changes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["chu_id", "year"]).copy()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["chu_id", "year"]]

    for col in numeric_cols:
        df[f"{col}_lag"] = df.groupby("chu_id")[col].shift(1)
        df[f"{col}_abs_change"] = df[col] - df[f"{col}_lag"]
        df[f"{col}_pct_change"] = np.where(
            df[f"{col}_lag"].notna() & (df[f"{col}_lag"] != 0),
            (df[col] - df[f"{col}_lag"]) / df[f"{col}_lag"] * 100,
            np.nan,
        )

    return df


def cumulative_change_from_baseline(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["chu_id", "year"]).copy()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["chu_id", "year"]]
    first_year = int(df["year"].min())

    baseline = df[df["year"] == first_year][["chu_id"] + numeric_cols].copy()
    baseline = baseline.rename(columns={c: f"{c}_baseline" for c in numeric_cols})

    merged = df.merge(baseline, on="chu_id", how="left")

    for col in numeric_cols:
        merged[f"{col}_cum_abs_change"] = merged[col] - merged[f"{col}_baseline"]
        merged[f"{col}_cum_pct_change"] = np.where(
            merged[f"{col}_baseline"].notna() & (merged[f"{col}_baseline"] != 0),
            (merged[col] - merged[f"{col}_baseline"]) / merged[f"{col}_baseline"] * 100,
            np.nan,
        )

    return merged


if __name__ == "__main__":
    panel_path = INTERIM_DIR / "chu_proxy_panel.csv"
    df = pd.read_csv(panel_path)

    year_to_year = compute_changes(df)
    cumulative = cumulative_change_from_baseline(df)

    year_to_year.to_csv(RESULTS_DIR / "chu_proxy_year_to_year_changes.csv", index=False)
    cumulative.to_csv(RESULTS_DIR / "chu_proxy_cumulative_changes.csv", index=False)

    print("Saved change metric tables.")
    print(year_to_year.head())
