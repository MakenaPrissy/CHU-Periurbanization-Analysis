from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
INTERIM_DIR = Path("data/interim")
INTERIM_DIR.mkdir(parents=True, exist_ok=True)


def melt_wide_years(df: pd.DataFrame, value_name: str, id_col: str = "CHU") -> pd.DataFrame:
    year_cols = [c for c in df.columns if str(c).isdigit()]
    out = df.melt(
        id_vars=[id_col],
        value_vars=year_cols,
        var_name="year",
        value_name=value_name,
    )
    out = out.rename(columns={id_col: "chu_name"})
    out["year"] = out["year"].astype(int)
    return out


def load_night_lights() -> pd.DataFrame:
    path = RAW_DIR / "CHU_night_lights.csv"
    df = pd.read_csv(path)
    return melt_wide_years(df, value_name="ntl")


def load_sentinel_built() -> pd.DataFrame:
    path = RAW_DIR / "kilifi_CHU_Sentinel_2017-2024.csv"
    df = pd.read_csv(path)
    return melt_wide_years(df, value_name="s2_built")


def load_worldpop_built() -> pd.DataFrame:
    path = RAW_DIR / "CHU_Built-up.csv"
    df = pd.read_csv(path)
    return melt_wide_years(df, value_name="wp_built")


def load_worldpop_density() -> pd.DataFrame:
    path = RAW_DIR / "worldpop_chu_density_wide.csv"
    df = pd.read_csv(path)
    return melt_wide_years(df, value_name="wp_density")


def load_degurba_urban_pct() -> pd.DataFrame:
    path = RAW_DIR / "CHU_Urbanisation_Percentages.xlsx"
    df = pd.read_excel(path)

    urban_cols = [c for c in df.columns if str(c).startswith("urban_pct_")]
    keep_cols = ["CHU"] + urban_cols
    df = df[keep_cols].copy()

    rename_map = {c: c.replace("urban_pct_", "") for c in urban_cols}
    df = df.rename(columns=rename_map)

    return melt_wide_years(df, value_name="degurba")


def build_panel() -> pd.DataFrame:
    ntl = load_night_lights()
    s2 = load_sentinel_built()
    wp_built = load_worldpop_built()
    wp_density = load_worldpop_density()
    degurba = load_degurba_urban_pct()

    panel = ntl.merge(s2, on=["chu_name", "year"], how="outer")
    panel = panel.merge(wp_built, on=["chu_name", "year"], how="outer")
    panel = panel.merge(wp_density, on=["chu_name", "year"], how="outer")
    panel = panel.merge(degurba, on=["chu_name", "year"], how="outer")

    panel = panel.sort_values(["chu_name", "year"]).reset_index(drop=True)

    # create a simple numeric id from CHU name
    chu_lookup = (
        panel[["chu_name"]]
        .drop_duplicates()
        .sort_values("chu_name")
        .reset_index(drop=True)
    )
    chu_lookup["chu_id"] = range(1, len(chu_lookup) + 1)

    panel = panel.merge(chu_lookup, on="chu_name", how="left")
    panel = panel[["chu_id", "chu_name", "year", "ntl", "s2_built", "wp_built", "wp_density", "degurba"]]

    return panel


if __name__ == "__main__":
    panel_df = build_panel()
    out_path = INTERIM_DIR / "chu_proxy_panel.csv"
    panel_df.to_csv(out_path, index=False)

    print(f"Saved panel to: {out_path}")
    print(panel_df.head())
