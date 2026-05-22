import sqlite3
import pickle
import hashlib
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "cache.db"

def _conn():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS price_cache (
            key TEXT PRIMARY KEY,
            data BLOB,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    return con

def get_cached(key: str) -> pd.DataFrame | None:
    with _conn() as con:
        row = con.execute("SELECT data FROM price_cache WHERE key=?", (key,)).fetchone()
        if row:
            return pickle.loads(row[0])
    return None

def set_cached(key: str, df: pd.DataFrame):
    blob = pickle.dumps(df)
    with _conn() as con:
        con.execute(
            "INSERT OR REPLACE INTO price_cache (key, data) VALUES (?,?)",
            (key, blob)
        )
        con.commit()
