import pandas as pd
import json
from collections import Counter

# ---- CONFIG ----
INPUT_PATH = "../data/patents_with_domains.csv"
TARGET_DOMAINS = ["AI/ML", "Computing/Software"]  # fastest-rising, highest-volume domains
TOP_N_KEYWORDS = 20

# ---- LOAD ----
print("Loading dataset...")
df = pd.read_csv(INPUT_PATH)
print(f"Loaded {len(df):,} rows")

# ---- FILTER TO TARGET DOMAINS ----
df_target = df[df["domain"].isin(TARGET_DOMAINS)].copy()
print(f"Filtered to {len(df_target):,} rows in target domains")


def parse_keywords(kw_raw):
    """Keywords field is a JSON-style string list, e.g.
    '["sensing electrodes", "biometric recognition"]'.
    Parse it into an actual Python list, or return an empty list on failure."""
    try:
        kws = json.loads(kw_raw)
        if isinstance(kws, list):
            return kws
    except (json.JSONDecodeError, TypeError):
        pass
    return []


# ---- ANALYZE EACH DOMAIN, BY YEAR ----
for domain in TARGET_DOMAINS:
    print(f"\n{'='*60}")
    print(f"DOMAIN: {domain}")
    print(f"{'='*60}")

    domain_df = df_target[df_target["domain"] == domain]

    for year in sorted(domain_df["Year"].unique()):
        year_df = domain_df[domain_df["Year"] == year]

        # Flatten all keyword lists for this domain-year into one big list
        all_keywords = []
        for kw_raw in year_df["Keywords"]:
            all_keywords.extend(parse_keywords(kw_raw))

        # Count frequency of each keyword phrase
        counts = Counter(all_keywords)
        top_keywords = counts.most_common(TOP_N_KEYWORDS)

        print(f"\n--- {domain} | {int(year)} ({len(year_df):,} patents) ---")
        for phrase, count in top_keywords[:10]:  # print top 10 to keep it readable
            print(f"  {count:>5}  {phrase}")


# ---- SAVE FULL RESULTS TO CSV ----
print("\n\nSaving full keyword breakdown to CSV...")

results = []
for domain in TARGET_DOMAINS:
    domain_df = df_target[df_target["domain"] == domain]
    for year in sorted(domain_df["Year"].unique()):
        year_df = domain_df[domain_df["Year"] == year]
        all_keywords = []
        for kw_raw in year_df["Keywords"]:
            all_keywords.extend(parse_keywords(kw_raw))
        counts = Counter(all_keywords)
        for phrase, count in counts.most_common(TOP_N_KEYWORDS):
            results.append({
                "domain": domain,
                "year": int(year),
                "keyword": phrase,
                "count": count
            })

results_df = pd.DataFrame(results)
results_df.to_csv("../output/top_keywords_by_domain_year.csv", index=False)
print("Saved to ../output/top_keywords_by_domain_year.csv")