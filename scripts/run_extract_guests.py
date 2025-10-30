import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.guests_extraction import assign_guest_names

df = pd.read_csv("data/raw/DIARY_all_pod.csv")
df = assign_guest_names(df)