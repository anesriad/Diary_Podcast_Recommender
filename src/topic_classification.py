# src/topic_classification.py
import os, pandas as pd, ollama
from tqdm import tqdm

def get_topic_category(title: str) -> str:
    """Use Ollama (Llama 3.2 3B) to classify YouTube titles into one broad topic."""
    if not isinstance(title, str) or not title.strip():
        return "other"

    prompt = f"""
    Categorize the following podcast title into ONE broad topic:
    - health
    - mental health / psychology
    - productivity / personal development
    - finance
    - relationships
    - entrepreneurship / business
    - religion / spirituality
    - technology
    - education
    - lifestyle
    - entertainment
    - other

    Title: "{title}"
    Return only the category name.
    """

    try:
        response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"].strip().lower()
    except Exception as e:
        print(f"⚠️ Topic classification error: {e}")
        return "other"

def assign_topic_categories(df: pd.DataFrame, cache_path: str = "data/interim/topics_processed.parquet") -> pd.DataFrame:
    """Run topic classification once per video and cache results."""
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    if os.path.exists(cache_path):
        print(f"✅ Loading cached topics from {cache_path}")
        return pd.read_parquet(cache_path)

    tqdm.pandas()
    meta = df[["video_id", "video_title"]].drop_duplicates().copy()
    meta["topic_category"] = meta["video_title"].progress_apply(get_topic_category)
    out = df.merge(meta[["video_id", "topic_category"]], on="video_id", how="left")
    out.to_parquet(cache_path, index=False)
    print(f"💾 Topics saved to {cache_path}")
    return out
