# src/kpi_calculations.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from rapidfuzz import process, fuzz
from datetime import datetime, timezone
import os

# =============================
# 1. Utility Helpers
# =============================

def add_days_since_published(df: pd.DataFrame) -> pd.DataFrame:
    """Add a column with days since publication."""
    if "video_published_at" not in df.columns:
        raise KeyError("'video_published_at' column missing in dataset")

    df["video_published_at"] = pd.to_datetime(df["video_published_at"], utc=True, errors="coerce")
    today = datetime.now(timezone.utc)
    df["days_since_published"] = (today - df["video_published_at"]).dt.days
    return df


def standardize_guest_names(guest_lists, threshold=90):
    """Standardize guest names using fuzzy matching to fix typos."""
    all_names = sorted({g for lst in guest_lists for g in lst if isinstance(g, str)})
    name_map = {}
    for name in all_names:
        if name_map:
            result = process.extractOne(name, name_map.keys(), scorer=fuzz.token_sort_ratio)
            if result:
                match, score, _ = result
                if score >= threshold:
                    name_map[name] = match
                    continue
        name_map[name] = name
    return name_map


def normalize_columns(df, cols):
    """MinMax normalize selected columns."""
    scaler = MinMaxScaler()
    for col in cols:
        df[f"{col}_norm"] = scaler.fit_transform(df[[col]])
    return df


# =============================
# 2. KPI Calculation Functions
# =============================

def compute_topic_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute topic-level averages and weighted engagement scores."""
    topic_df = (
        df.drop_duplicates(subset="video_id")
          .loc[:, ["video_id", "topic_category", "view_count", "video_like_count", "comment_count", "video_title"]]
    )

    topic_stats = (
        topic_df.groupby("topic_category", as_index=False)
                .agg({
                    "view_count": "mean",
                    "video_like_count": "mean",
                    "comment_count": "mean",
                    "video_id": "count"
                })
                .rename(columns={"video_id": "n_videos"})
    )

    topic_stats = normalize_columns(topic_stats, ["view_count", "video_like_count", "comment_count"])

    topic_stats["weighted_score"] = (
        0.5 * topic_stats["comment_count_norm"] +
        0.3 * topic_stats["video_like_count_norm"] +
        0.2 * topic_stats["view_count_norm"]
    ).round(2)

    topic_stats["rank"] = topic_stats["weighted_score"].rank(ascending=False).astype(int)
    return topic_stats.sort_values("weighted_score", ascending=False)


def compute_guest_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute guest-level weighted KPIs with name cleaning."""
    # ✅ Clean up guest names
    mapping = standardize_guest_names(df["guest_list"])
    df["guest_list"] = df["guest_list"].apply(lambda lst: [mapping[g] for g in lst])

    # ✅ Add "days_since_published" if missing
    if "days_since_published" not in df.columns and "video_published_at" in df.columns:
        df = add_days_since_published(df)

    # ✅ Base video-level aggregation
    video_df = (
        df.drop_duplicates(subset="video_id")
          .loc[:, [
              "days_since_published",
              "video_id",
              "video_title",
              "guest_list",
              "topic_category",
              "view_count",
              "video_like_count",
              "comment_count"
          ]]
    )

    video_df["n_guests"] = video_df["guest_list"].apply(lambda x: len(x) if isinstance(x, list) and len(x) > 0 else 1)
    video_df["views_per_guest"] = (video_df["view_count"] / video_df["n_guests"]).round(2)
    video_df["likes_per_guest"] = (video_df["video_like_count"] / video_df["n_guests"]).round(2)
    video_df["comments_per_guest"] = (video_df["comment_count"] / video_df["n_guests"]).round(2)

    # ✅ Explode guests (1 row per guest per episode)
    guest_df = video_df.explode("guest_list").rename(columns={"guest_list": "guest"})

    # ✅ Guest-level aggregation
    guest_stats = (
        guest_df.groupby("guest", as_index=False)
                 .agg({
                     "views_per_guest": "mean",
                     "likes_per_guest": "mean",
                     "comments_per_guest": "mean",
                     "video_id": "count"
                 })
                 .rename(columns={"video_id": "appearances"})
    )

    # ✅ Normalize metrics
    guest_stats = normalize_columns(guest_stats, ["views_per_guest", "likes_per_guest", "comments_per_guest"])

    # ✅ Weighted score logic (same as your notebook)
    guest_stats["weighted_score"] = (
        0.5 * guest_stats["comments_per_guest_norm"] +
        0.3 * guest_stats["likes_per_guest_norm"] +
        0.2 * guest_stats["views_per_guest_norm"]
    ).round(2)

    guest_stats["rank"] = guest_stats["weighted_score"].rank(ascending=False).astype(int)
    return guest_stats.sort_values("weighted_score", ascending=False)


# =============================
# 3. Master Runner
# =============================

def compute_all_kpis(input_path="data/processed/top_funnel_ready.parquet", output_dir="data/processed/kpis"):
    """Run all KPI computations and save results."""
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_parquet(input_path)

    # ✅ Ensure 'days_since_published' exists
    if "days_since_published" not in df.columns and "video_published_at" in df.columns:
        df = add_days_since_published(df)

    print("⚙️ Computing topic KPIs...")
    topic_stats = compute_topic_kpis(df)
    topic_stats.to_parquet(os.path.join(output_dir, "topic_stats.parquet"), index=False)
    print("✅ Topics saved.")

    print("⚙️ Computing guest KPIs...")
    guest_stats = compute_guest_kpis(df)
    guest_stats.to_parquet(os.path.join(output_dir, "guest_stats.parquet"), index=False)
    print("✅ Guests saved.")

    print(f"🎯 All KPI results saved to {output_dir}/")
    return topic_stats, guest_stats
