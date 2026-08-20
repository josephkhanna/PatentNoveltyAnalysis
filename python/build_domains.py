import pandas as pd
import json

# ---- CONFIG ----
INPUT_PATH = "../data/patents_2016_2020_filtered.csv"
OUTPUT_PATH = "../data/patents_with_domains.csv"

# ---- IPC PREFIX -> DOMAIN LOOKUP ----
# Based on IPC classification codes (class + subclass level, e.g. "G06N").
# Matched by checking if the patent's primary IPC code starts with one of these keys.
# Longer/more specific prefixes are checked first so "G06N" doesn't get swallowed by a broader "G06" rule.
IPC_TO_DOMAIN = {
    # --- AI / ML / Data ---
    "G06N": "AI/ML",              # computing based on specific computational models (core AI/ML)
    "G06V": "AI/ML",              # image/video recognition (modern CV classification)
    "G06K9": "AI/ML",             # legacy pattern recognition / biometrics / old CV code
    "G06K7": "AI/ML",             # legacy pattern recognition (readers, scanners)

    # --- General Computing / Software ---
    "G06F": "Computing/Software", # general digital data processing

    # --- Business / Fintech / Data Systems ---
    "G06Q": "Business/Fintech",   # data processing for admin, commerce, finance

    # --- Imaging / Graphics / Optics ---
    "G06T": "Imaging/Graphics",   # image data processing, 3D graphics
    "G02B": "Imaging/Graphics",   # optical elements
    "H04N": "Imaging/Graphics",   # image communication (cameras, video)

    # --- Telecom / Networking ---
    "H04L": "Telecom/Networking", # digital data transmission
    "H04W": "Telecom/Networking", # wireless communication networks
    "H04B": "Telecom/Networking", # general transmission systems
    "H04M": "Telecom/Networking", # telephonic communication

    # --- Semiconductors / Electronics ---
    "H01L": "Semiconductors/Electronics",   # semiconductor devices (core)
    "H10":  "Semiconductors/Electronics",   # newer IPC scheme for semiconductor devices (post-2021 reclassification of H01L)
    "H01Q": "Semiconductors/Electronics",   # antennas
    "H03K": "Semiconductors/Electronics",   # pulse technique / digital circuits
    "H01B": "Semiconductors/Electronics",   # conductors, cables, resistors
    "H01G": "Semiconductors/Electronics",   # capacitors
    "G11C": "Semiconductors/Electronics",   # static/dynamic memory devices (semiconductor memory, very relevant)
    "H03F": "Semiconductors/Electronics",   # amplifiers
    "H03M": "Semiconductors/Electronics",   # code conversion (ADC/DAC circuits)

    # --- Biotech / Medical ---
    "A61B": "Biotech/Medical",    # diagnosis, surgery
    "A61K": "Biotech/Medical",    # medical preparations
    "A61P": "Biotech/Medical",    # therapeutic activity
    "C12N": "Biotech/Medical",    # microorganisms, genetic engineering
    "C12Q": "Biotech/Medical",    # measuring/testing processes for biology
    "C07K": "Biotech/Medical",    # peptides, proteins

    # --- Energy / Power ---
    "H02J": "Energy/Power",   # circuit arrangements for power distribution
    "H02S": "Energy/Power",   # solar power generation
    "H02K": "Energy/Power",   # electric generators/motors
    "H02M": "Energy/Power",   # power conversion (AC/DC, inverters)
    "H02N": "Energy/Power",   # electric machines not covered elsewhere
    "F03D": "Energy/Power",   # wind motors
    "F03B": "Energy/Power",   # hydraulic engines (hydropower)
    "H01M": "Energy/Power",   # batteries, fuel cells
    "C25B": "Energy/Power",   # electrolytic processes (hydrogen production)
    "F24S": "Energy/Power",   # solar heat collectors
    "G21":  "Energy/Power",   # nuclear reactors and related tech

    # --- Mechanical / Transportation ---
    "B60": "Mechanical/Transportation",   # vehicles in general
    "B62D": "Mechanical/Transportation",  # motor vehicles

    # --- Measuring / Sensors ---
    "G01B": "Measuring/Sensors",
    "G01N": "Measuring/Sensors",
    "G01S": "Measuring/Sensors",  # radar, positioning
}

# Fallback bucket if no prefix matches
DEFAULT_DOMAIN = "Other"


def get_primary_ipc(ipc_raw):
    """IPC field is stored as a JSON-style string list. Parse it and return
    the first code, or None if parsing fails or the list is empty."""
    try:
        codes = json.loads(ipc_raw)
        if isinstance(codes, list) and len(codes) > 0:
            return codes[0]
    except (json.JSONDecodeError, TypeError):
        return None
    return None


def map_to_domain(ipc_code):
    """Check the IPC code against our lookup table, longest/most specific
    prefix first, so e.g. 'G06K9' matches before a hypothetical broader 'G06' rule."""
    if pd.isna(ipc_code):
        return DEFAULT_DOMAIN

    # Sort keys by length descending so more specific prefixes are checked first
    for prefix in sorted(IPC_TO_DOMAIN.keys(), key=len, reverse=True):
        if ipc_code.startswith(prefix):
            return IPC_TO_DOMAIN[prefix]

    return DEFAULT_DOMAIN


# ---- LOAD ----
print("Loading filtered dataset...")
df = pd.read_csv(INPUT_PATH)
print(f"Loaded {len(df):,} rows")

# ---- APPLY MAPPING ----
print("Extracting primary IPC code and mapping to domain...")
df["primary_ipc"] = df["IPC"].apply(get_primary_ipc)
df["domain"] = df["primary_ipc"].apply(map_to_domain)



print("\n--- Domain distribution ---")
print(df["domain"].value_counts())

other_pct = (df["domain"] == DEFAULT_DOMAIN).mean() * 100
print(f"\n'Other' bucket: {other_pct:.1f}% of rows")
if other_pct > 30:
    print("WARNING: 'Other' is large — consider adding more IPC prefixes to the lookup table.")

print("\nSample mapped rows:")
print(df[["PN", "primary_ipc", "domain", "Year", "Novelty"]].head(10).to_string())

# ---- EXPORT ----
export_cols = ["PN", "primary_ipc", "domain", "Year", "Novelty", "Keywords"]
df[export_cols].to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved domain-mapped dataset to {OUTPUT_PATH}")