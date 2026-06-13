import pandas as pd

df = pd.read_csv("data/raw/hl_qol.csv")

print("shape")
print(df.shape)

print("\ncolumns")
print(df.columns)

print("\nhead")
print(df.head())

print("\nmissing values")
print(df.isna().sum())

print("\nhealth literacy")
print(df["hltcatnew"].value_counts(dropna=False))

print("\npcs summary")
print(df["pcs"].describe())

print("\nmcs summary")
print(df["mcs"].describe())
