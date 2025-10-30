# src/guests_extraction.py
import os, json, re, pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

def get_guest_names_openrouter(description: str) -> list:
    """Extract true guest names from YouTube descriptions using GPT-4o-mini."""
    if not isinstance(description, str) or not description.strip():
        return []

    prompt = f"""
    You are a podcast metadata assistant.

    Task:
    - Read the YouTube video description carefully.
    - Identify ONLY the actual guest(s) who appear in the episode.
    - Ignore names mentioned as examples or comparisons.
    - Preserve professional titles (Dr, Prof, etc).
    - Return a JSON list, e.g. ["Andrew Huberman", "Lex Fridman"].
    - Return [] if no clear guest.
    Description:
    \"\"\"{description}\"\"\"
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200,
        )
        content = completion.choices[0].message.content.strip()
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r'\[(.*?)\]', content)
            result = [n.strip().strip('"') for n in match.group(1).split(",")] if match else []
        if isinstance(result, str): result = [result]
        return list({r.strip() for r in result if r.strip()})
    except Exception as e:
        print(f"⚠️ Guest extraction error: {e}")
        return []

def assign_guest_names(df: pd.DataFrame, cache_path: str = "data/interim/guests_processed.parquet") -> pd.DataFrame:
    """Extract guests once per video and cache results."""
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    # reuse cache if it exists
    if os.path.exists(cache_path):
        print(f"✅ Loading cached guests from {cache_path}")
        return pd.read_parquet(cache_path)

    tqdm.pandas()
    meta = df.drop_duplicates(subset="video_id")[["video_id", "video_description"]].copy()
    meta["guest_list"] = meta["video_description"].progress_apply(get_guest_names_openrouter)
    out = df.merge(meta[["video_id", "guest_list"]], on="video_id", how="left")
    out.to_parquet(cache_path, index=False)
    print(f"💾 Guests saved to {cache_path}")
    return out
