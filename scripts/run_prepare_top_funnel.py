import pandas as pd
import os

def prepare_top_funnel(
    guests_path="data/interim/guests_processed.parquet",
    topics_path="data/interim/topics_processed.parquet",
    output_path="data/processed/top_funnel_ready.parquet",
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    guests = pd.read_parquet(guests_path)
    topics = pd.read_parquet(topics_path)

    # merge on video_id (keep all columns)
    df = pd.merge(
        guests.drop_duplicates("video_id"),
        topics[["video_id", "topic_category"]],
        on="video_id",
        how="left"
    )

    df.to_parquet(output_path, index=False)
    print(f"✅ Combined dataset saved to {output_path} — {len(df)} rows")

if __name__ == "__main__":
    prepare_top_funnel()
