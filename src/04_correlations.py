#correlations script
from pathlib import Path
import itertools
import math
import numpy as np
import pandas as pd


INTERIM_DIR = Path("data/interim")
RESULTS_DIR = Path("results/tables")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def fisher_ci(r: float, n: int, alpha: float = 0.05):
    if pd.isna(r) or n < 4 or abs(r) >= 1:
        return np.nan, np.nan
    z = 0.5 * math.log((1 + r) / (1 - r))
    se = 1 / math.sqrt(n - 3)
    z_crit = 1.96
    lo = z - z_crit * se
    hi = z + z_crit * se
    r_lo = (math.exp(2 * lo) - 1) / (math.exp(2 * lo) + 1)
    r_hi = (math.exp(2 * hi) - 1) / (math.exp(2 * hi) + 1)
    return r_lo, r_hi


def correlation_table(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["chu_id", "year"]]

    rows = []
    for var1, var2 in itertools.combinations(numeric_cols, 2):
        sub = df[[var1, var2]].dropna()
        n = len(sub)
        if n < 3:
            continue
        r = sub[var1].corr(sub[var2], method="pearson")
        ci_low, ci_high = fisher_ci(r, n)
        rows.append(
            {
                "var1": var1,
                "var2": var2,
                "n": n,
                "pearson_r": r,
                "ci_low_95": ci_low,
                "ci_high_95": ci_high,
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    panel_path = INTERIM_DIR / "chu_proxy_panel.csv"
    df = pd.read_csv(panel_path)

    overall = correlation_table(df)
    overall.to_csv(RESULTS_DIR / "proxy_correlations_overall.csv", index=False)

    yearly_tables = []
    for year in sorted(df["year"].dropna().unique()):
        ydf = df[df["year"] == year].copy()
        corr_y = correlation_table(ydf)
        corr_y["year"] = year
        yearly_tables.append(corr_y)

    if yearly_tables:
        yearly = pd.concat(yearly_tables, ignore_index=True)
        yearly.to_csv(RESULTS_DIR / "proxy_correlations_by_year.csv", index=False)

    print("Saved correlation tables.")
    print(overall.head())
