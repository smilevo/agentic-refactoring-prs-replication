import pandas as pd
import os

# Path to your humans file
script_dir = os.path.dirname(os.path.abspath(__file__))
hum_path = os.path.join(script_dir, "AIDev_pop_refactor_reviewers_bots.csv")
if not os.path.exists(hum_path):
    hum_path = os.path.abspath(os.path.join(script_dir, "../../study_design/rq2/data_extraction/AIDev_pop_refactor_reviewers_bots.csv"))

# Load and normalize usernames
hum = pd.read_csv(hum_path)
hum['user'] = hum['user'].astype(str).str.strip().str.lower()

# Get unique reviewers
unique_humans = hum['user'].dropna().drop_duplicates().sort_values()

print(f"Total unique bots reviewers: {len(unique_humans):,}\n")
print(unique_humans.head(50).to_list())  # show first 50

# Optional: save to a text file
out_path = os.path.join(script_dir, "unique_bots_reviewers.txt")
unique_humans.to_csv(out_path, index=False, header=['user'])
print(f"\n✅ Saved all unique bots reviewers to: {out_path}")
