import pandas as pd

DATA_PATH = "data/raw/hl_qol.csv"


def print_section(title):
    print(f"\n--- {title} ---")


df = pd.read_csv(DATA_PATH)

print_section("shape")
print(df.shape)

print_section("columns")
print(df.columns)

print_section("head")
print(df.head())

print_section("missing values")
print(df.isna().sum())

print_section("health literacy")
print(df["hltcatnew"].value_counts(dropna=False))

print_section("pcs summary")
print(df["pcs"].describe())

print_section("mcs summary")
print(df["mcs"].describe())
