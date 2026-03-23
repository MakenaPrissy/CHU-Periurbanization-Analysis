
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


INTERIM_DIR = Path("data/interim")
RESULTS_DIR = Path("results/tables")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def cluster_one_year(df_year: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    work = df_year.copy()

    numeric_cols = work.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["chu_id", "year"]]

    x = work[numeric_cols].copy()
    x = x.dropna()

    meta = work.loc[x.index, ["chu_id", "chu_name", "year"]].copy()

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    labels = km.fit_predict(x_scaled)

    meta["cluster"] = labels
    return meta


def label_cluster_order(df_clusters: pd.DataFrame, original_df: pd.DataFrame) -> pd.DataFrame:
    merged = df_clusters.merge(
        original_df,
        on=["chu_id", "chu_name", "year"],
        how="left",
    )

    numeric_cols = merged.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ["chu_id", "year", "cluster"]]

    cluster_scores = (
        merged.groupby("cluster")[numeric_cols]
        .mean()
        .mean(axis=1)
        .sort_values()
        .reset_index(name="score")
    )

    cluster_scores["trajectory_group"] = [
        "lower_urban",
        "intermediate_urban",
        "higher_urban",
    ][: len(cluster_scores)]

    out = df_clusters.merge(
        cluster_scores[["cluster", "trajectory_group"]],
        on="cluster",
        how="left",
    )
    return out


if __name__ == "__main__":
    panel_path = INTERIM_DIR / "chu_proxy_panel.csv"
    df = pd.read_csv(panel_path)

    all_years = []
    for year in sorted(df["year"].dropna().unique()):
        df_year = df[df["year"] == year].copy()
        if len(df_year) < 3:
            continue

        clustered = cluster_one_year(df_year, n_clusters=3)
        labeled = label_cluster_order(clustered, df_year)
        all_years.append(labeled)

    if not all_years:
        raise ValueError("No cluster results were generated.")

    clusters = pd.concat(all_years, ignore_index=True)
    clusters.to_csv(RESULTS_DIR / "chu_clusters_by_year.csv", index=False)

    vote_summary = (
        clusters.groupby(["chu_id", "chu_name", "trajectory_group"])
        .size()
        .reset_index(name="n_years")
        .sort_values(["chu_id", "n_years"], ascending=[True, False])
    )

    dominant = vote_summary.drop_duplicates(subset=["chu_id", "chu_name"]).copy()
    dominant = dominant.rename(columns={"trajectory_group": "dominant_group"})
    dominant.to_csv(RESULTS_DIR / "chu_dominant_trajectory_group.csv", index=False)

    print("Saved clustering outputs.")
    print(dominant.head())
