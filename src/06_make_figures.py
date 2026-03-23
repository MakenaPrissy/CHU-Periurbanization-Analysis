from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


INTERIM_DIR = Path("data/interim")
RESULTS_DIR = Path("results/figures")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def plot_mean_trajectories(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["chu_id", "year"]]

    for col in numeric_cols:
        yearly = df.groupby("year", as_index=False)[col].mean()

        plt.figure(figsize=(8, 5))
        plt.plot(yearly["year"], yearly[col], marker="o")
        plt.title(f"Mean trajectory of {col} over time")
        plt.xlabel("Year")
        plt.ylabel(col)
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / f"trajectory_{col}.png", dpi=300)
        plt.close()


if __name__ == "__main__":
    panel_path = INTERIM_DIR / "chu_proxy_panel.csv"
    df = pd.read_csv(panel_path)

    plot_mean_trajectories(df)

    print("Saved trajectory figures.")
