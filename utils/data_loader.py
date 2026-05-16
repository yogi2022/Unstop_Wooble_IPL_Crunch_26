"""
utils/data_loader.py
Load and preprocess ball-by-ball IPL CSV data.
"""

import io
import pandas as pd
import numpy as np


def load_and_preprocess(file_bytes) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load raw CSV, clean columns, derive features, and return:
        df      — ball-level DataFrame (one row = one delivery)
        matches — match-level DataFrame (one row = one match)
    """
    raw = pd.read_csv(io.BytesIO(file_bytes.read()) if hasattr(file_bytes, "read") else io.StringIO(file_bytes))

    df = raw.copy()

    # ── Normalise column names ─────────────────────────────────────────────────
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # ── Ensure required columns exist ─────────────────────────────────────────
    required = [
        "match_id", "season", "innings", "over", "ball",
        "batter", "bowler", "runs_batter", "runs_total",
        "toss_winner", "toss_decision", "winner", "team1", "team2",
    ]
    for col in required:
        if col not in df.columns:
            df[col] = np.nan

    # ── Types ─────────────────────────────────────────────────────────────────
    df["season"]       = df["season"].astype(str).str.extract(r"(\d{4})")[0]
    df["season"]       = pd.to_numeric(df["season"], errors="coerce").fillna(0).astype(int)
    df["over"]         = pd.to_numeric(df["over"], errors="coerce").fillna(0).astype(int)
    df["runs_batter"]  = pd.to_numeric(df["runs_batter"], errors="coerce").fillna(0)
    df["runs_total"]   = pd.to_numeric(df["runs_total"], errors="coerce").fillna(0)
    df["innings"]      = pd.to_numeric(df["innings"], errors="coerce").fillna(1).astype(int)

    # ── Wicket flag ───────────────────────────────────────────────────────────
    if "wicket_player_out" in df.columns:
        df["is_wicket"] = df["wicket_player_out"].notna() & (df["wicket_player_out"].astype(str).str.strip() != "")
    else:
        df["is_wicket"] = False

    # ── Dot ball ──────────────────────────────────────────────────────────────
    df["is_dot"] = (df["runs_total"] == 0)

    # ── Boundary flag ─────────────────────────────────────────────────────────
    df["is_boundary"] = df["runs_batter"].isin([4, 6])
    df["is_six"]      = (df["runs_batter"] == 6)
    df["is_four"]     = (df["runs_batter"] == 4)

    # ── Phase label ───────────────────────────────────────────────────────────
    df["phase"] = pd.cut(
        df["over"],
        bins=[-1, 5, 14, 25],
        labels=["powerplay", "middle", "death"],
    )

    # ── Match-level table ──────────────────────────────────────────────────────
    match_cols = [
        "match_id", "season", "date", "venue", "city",
        "team1", "team2", "toss_winner", "toss_decision",
        "winner", "win_by_runs", "win_by_wickets", "player_of_match",
    ]
    avail = [c for c in match_cols if c in df.columns]
    matches = (
        df[avail]
        .drop_duplicates(subset=["match_id"])
        .copy()
        .reset_index(drop=True)
    )

    # Toss won match?
    matches["toss_won_match"] = (
        matches["toss_winner"] == matches["winner"]
    )

    # Batting team per delivery
    if "batting_team" not in df.columns:
        df["batting_team"] = df["team1"]  # fallback

    return df, matches
