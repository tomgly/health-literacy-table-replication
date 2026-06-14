import pandas as pd
from statsmodels.stats.proportion import proportion_confint
from scipy.stats import chi2_contingency
from pathlib import Path

DATA_PATH = "data/raw/hl_qol.csv"
OUTPUT_PATH = "outputs/table2_preview.csv"

TABLE2_BLOCKS = [
    ("Gender", ["Male", "Female"]),
    ("agegroup3", ["38 to 69 years", "70 to 79 years", "80 years above"]),
    ("ms2g", ["married", "unmarried"]),
    ("RA06ur", ["Urban Area", "Rural Australia"]),
    ("Stateno", ["SA practice", "QLD practice"]),
    ("educatn4g", [
        "post grad/bachelor",
        "advdipl/dipl/certif/trade",
        "seniorsec/secondary",
        "no schooling/primary",
    ]),
    ("workst3g", ["employed", "retired", "pensioner"]),
    ("econ3g", ["very high to higher", "the same", "lower to very low"]),
    ("irsd_quint", ["highest", "high", "middle", "low"]),
    ("ischprocedure", ["no", "yes"]),
    ("yearsIHD3g", ["0-5 years", "6-10 years", ">10 years"]),
    ("CVDcomorb3g", ["none", "just 1", "2 or more"]),
    ("CVDriskf3g", ["0-1 risk factors", "2 risk factors", "3 or more"]),
]


def print_section(title):
    print(f"\n--- {title} ---")


def prepare_table2_data(df):
    # Table 2ではhealth literacyが欠損している行を除外する
    df_table2 = df.dropna(subset=["hltcatnew"]).copy()
    df_table2["inadequate_hl"] = df_table2["hltcatnew"].eq("inadequate")
    return df_table2


def make_table2_block(df, df_table2, variable_name, category_order):
    variable_n = df[variable_name].value_counts().reindex(category_order)
    variable_percent = variable_n / len(df) * 100

    variable_hl = (
        df_table2
        .groupby(variable_name)["inadequate_hl"]
        .agg(["count", "sum", "mean"])
        .reindex(category_order)
    )

    variable_cross = pd.crosstab(
        df_table2[variable_name],
        df_table2["inadequate_hl"],
    ).reindex(category_order)

    _, p_value, _, _ = chi2_contingency(variable_cross.to_numpy())

    result = pd.DataFrame({
        "N": variable_n,
        "%": variable_percent,
        "inadequate_n": variable_hl["sum"],
        "prevalence_percent": variable_hl["mean"] * 100,
    })

    result["p_value"] = p_value

    ci_low, ci_high = proportion_confint(
        count=variable_hl["sum"],
        nobs=variable_hl["count"],
        alpha=0.05,
        method="wilson",
    )

    result["ci_low"] = ci_low * 100
    result["ci_high"] = ci_high * 100

    return result.round({
        "%": 1,
        "prevalence_percent": 1,
        "ci_low": 1,
        "ci_high": 1,
        "p_value": 3,
    })


def format_table2_block(variable_name, block):
    formatted = block.copy()
    formatted.insert(0, "variable", variable_name)
    formatted.insert(1, "category", formatted.index)
    formatted["95% CI"] = (
        formatted["ci_low"].astype(str)
        + "-"
        + formatted["ci_high"].astype(str)
    )
    formatted["p_value"] = formatted["p_value"].astype(str)
    formatted.loc[formatted.index[1:], "p_value"] = ""

    return formatted[[
        "variable",
        "category",
        "N",
        "%",
        "prevalence_percent",
        "95% CI",
        "p_value",
    ]]


df = pd.read_csv(DATA_PATH)
df_table2 = prepare_table2_data(df)

print_section("Overall Inadequate Health Literacy")
print(df_table2["inadequate_hl"].value_counts())
print(round(df_table2["inadequate_hl"].mean() * 100, 1))

formatted_blocks = []

for variable_name, category_order in TABLE2_BLOCKS:
    print_section(f"{variable_name} result")
    block = make_table2_block(df, df_table2, variable_name, category_order)
    formatted_block = format_table2_block(variable_name, block)
    formatted_blocks.append(formatted_block)
    print(formatted_block.to_string(index=False))

table2_preview = pd.concat(formatted_blocks, ignore_index=True)
Path("outputs").mkdir(exist_ok=True)
table2_preview.to_csv(OUTPUT_PATH, index=False)

print_section("note")
print("Table 2 may not fully match the published values when recalculated from this dataset.")
print(f"Saved preview to {OUTPUT_PATH}")
