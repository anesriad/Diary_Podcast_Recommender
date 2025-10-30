import pandas as pd
from src.topic_classification import assign_topic_categories

df = pd.read_parquet("data/interim/guests_processed.parquet")
df = assign_topic_categories(df)