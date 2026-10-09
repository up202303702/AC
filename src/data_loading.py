"""Load the hockey CSVs into pandas, and optionally into a SQLite database.

Usage from a notebook in notebooks/:

    import sys; sys.path.append("..")
    from src.data_loading import load_all, build_sqlite, overview

    tables = load_all()            # dict: table name -> DataFrame
    overview(tables)               # rows / columns / years / leagues per table
    con = build_sqlite(tables)     # creates hockey.db, then e.g.:
    # pd.read_sql("SELECT year, tmID, rank FROM Teams WHERE lgID='NHL'", con)
"""
from pathlib import Path
import sqlite3

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "hockey_development_data"
DB_PATH = REPO_ROOT / "hockey.db"


def load_all(raw_dir: Path = RAW_DIR) -> dict[str, pd.DataFrame]:
    """Read every CSV in the raw data folder. Keys are file names without .csv."""
    files = sorted(Path(raw_dir).glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSVs found in {raw_dir}")
    return {f.stem: pd.read_csv(f, low_memory=False) for f in files}


def overview(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per table: size, year range, leagues and overall % of missing cells."""
    rows = []
    for name, df in tables.items():
        rows.append({
            "table": name,
            "rows": len(df),
            "cols": df.shape[1],
            "first_year": df["year"].min() if "year" in df else None,
            "last_year": df["year"].max() if "year" in df else None,
            "leagues": ", ".join(sorted(df["lgID"].dropna().unique())) if "lgID" in df else "",
            "missing_%": round(df.isna().mean().mean() * 100, 1),
        })
    return pd.DataFrame(rows).set_index("table")


def build_sqlite(tables: dict[str, pd.DataFrame], db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Write every table into a SQLite file (overwrites existing tables) and return a connection."""
    con = sqlite3.connect(db_path)
    for name, df in tables.items():
        df.to_sql(name, con, if_exists="replace", index=False)
    return con


if __name__ == "__main__":
    t = load_all()
    print(overview(t).to_string())
    build_sqlite(t)
    print(f"\nSQLite database written to {DB_PATH}")
