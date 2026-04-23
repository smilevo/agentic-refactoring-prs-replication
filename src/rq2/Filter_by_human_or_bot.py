# File: Filter_REF_by_human_or_bot_all_rows.py
import os
import pandas as pd
import csv

# ---------- paths ----------
here = os.path.dirname(os.path.abspath(__file__))
# Check if data exists in src/rq2, otherwise look in study_design
all_rows_path = os.path.join(here, "AIDev_all_refactor_PR_reviews.csv")
if not os.path.exists(all_rows_path):
    all_rows_path = os.path.abspath(os.path.join(here, "../../study_design/rq2/data_extraction/AIDev_all_refactor_PR_reviews.csv"))

hum_out = os.path.join(here, "AIDev_pop_refactor_reviewers_humans.csv")
bot_out = os.path.join(here, "AIDev_pop_refactor_reviewers_bots.csv")

# ---------- load ----------
df = pd.read_csv(all_rows_path)

if "user" not in df.columns:
    raise KeyError(f"'user' column not found in {all_rows_path}. Columns: {list(df.columns)}")

# keep an original-case copy in case you want to inspect later
df["user_orig"] = df["user"].astype(str)

# normalize for reliable matching
df["user_norm"] = df["user"].astype(str).str.strip().str.lower()

# ---------- bot classifier (same logic as before; high precision) ----------
KNOWN_BOT_LOGINS = {
    # Paper Fig.7 + common CI/automation
    "copilot", "copilot-pull-request-reviewer[bot]", "copilot-swe-agent[bot]",
    "cursor[bot]", "gemini-code-assist[bot]", "coderabbitai[bot]",
    "ellipsis-dev[bot]", "greptile-apps[bot]", "entelligence-ai-pr-reviews[bot]",
    "github-advanced-security[bot]",
    "github-actions[bot]", "dependabot[bot]", "dependabot[security]",
    "renovate[bot]", "mergify[bot]", "semantic-release-bot", "snyk-bot",
    "codecov[bot]", "vercel[bot]", "netlify[bot]", "circleci[bot]",
    "travis-ci", "azure-pipelines[bot]", "actions-user", "release-please[bot]",
    "automation-bot",
}
SAFE_BOT_SUFFIXES = ("-bot", "_bot")

def is_bot_user(u: str) -> bool:
    if not isinstance(u, str) or u == "" or u == "nan":
        return False
    ul = u.strip().lower()
    if "[bot]" in ul:
        return True
    if ul in KNOWN_BOT_LOGINS:
        return True
    if ul.endswith(SAFE_BOT_SUFFIXES):
        return True
    return False

df["is_bot"] = df["user_norm"].apply(is_bot_user)

# ---------- split WITHOUT de-dup ----------
humans = df[df["is_bot"] == False].copy()
bots   = df[df["is_bot"] == True].copy()

# choose columns to export (keep whatever exists)
preferred_cols = ["pr_id","user","state","submitted_at","full_name","stars","body"]
cols = [c for c in preferred_cols if c in df.columns]
if not cols:
    cols = df.columns.tolist()  # fall back to everything if preferred not present

# ---------- save ----------
humans[cols].to_csv(hum_out, index=False, encoding="utf-8-sig",
                    lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
bots[cols].to_csv(bot_out, index=False, encoding="utf-8-sig",
                  lineterminator="\n", quoting=csv.QUOTE_MINIMAL)

# ---------- summary ----------
print("\n📊 Refactor PRs — ALL review rows (no de-dup)")
print(f"🤖 bot rows:   {len(bots):,}")
print(f"👩‍💻 human rows: {len(humans):,}")
print(f"✅ saved humans -> {hum_out}")
print(f"✅ saved bots   -> {bot_out}")
