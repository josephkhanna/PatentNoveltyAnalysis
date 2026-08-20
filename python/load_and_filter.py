import pandas as pd

# ---- CONFIG ----
INPUT_PATH = "../data/DeepPatentAI.csv"
OUTPUT_PATH = "../data/patents_2016_2020_filtered.csv"
YEAR_START = 2016
YEAR_END = 2020

# ---- LOAD ----
# The DeepPatentAI file is large w/ over 2.3M+ rows, so this reads it in chunks to avoid blowing up memory, filtering each chunk as we go.
print("Loading and filtering in chunks...")

chunks = []
chunk_size = 100_000

for i, chunk in enumerate(pd.read_csv(INPUT_PATH, chunksize=chunk_size)):
    # Filter to our year range
    filtered = chunk[(chunk["Year"] >= YEAR_START) & (chunk["Year"] <= YEAR_END)]

    # Drop rows missing the fields we actually need
    filtered = filtered.dropna(subset=["IPC", "Novelty", "Keywords"])

    chunks.append(filtered)

    if i % 5 == 0:
        print(f"  processed chunk {i}, running total: {sum(len(c) for c in chunks):,} rows")

# Combine all filtered chunks into one DataFrame
df = pd.concat(chunks, ignore_index=True)

print(f"Total filtered rows: {len(df):,}")
print(f"\nYear range in filtered data: {df['Year'].min()} to {df['Year'].max()}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nSample rows:")
print(df.head(5).to_string())

print(f"\nNovelty score stats:")
print(df["Novelty"].describe())

print(f"\nRows per year:")
print(df["Year"].value_counts().sort_index())

# ---- SAVE ----
df.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved filtered dataset to {OUTPUT_PATH}")