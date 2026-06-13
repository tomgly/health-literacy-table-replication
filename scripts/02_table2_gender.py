import pandas as pd
from statsmodels.stats.proportion import proportion_confint
from scipy.stats import chi2_contingency

DATA_PATH = "data/raw/hl_qol.csv"
GENDER_ORDER = ["Male", "Female"]


def print_section(title):
    print(f"\n--- {title} ---")


def prepare_table2_data(df):
    # Table 2ではhealth literacyが欠損している行を除外する
    df_table2 = df.dropna(subset=["hltcatnew"]).copy()
    df_table2["inadequate_hl"] = df_table2["hltcatnew"].eq("inadequate")
    return df_table2


def make_gender_table(df, df_table2):
    gender_n = df["Gender"].value_counts().reindex(GENDER_ORDER)
    gender_percent = gender_n / len(df) * 100

    gender_hl = (
        df_table2
        .groupby("Gender")["inadequate_hl"]
        .agg(["count", "sum", "mean"])
        .reindex(GENDER_ORDER)
    )

    gender_cross = pd.crosstab(
        df_table2["Gender"],
        df_table2["inadequate_hl"],
    ).reindex(GENDER_ORDER)

    _, p_value, _, _ = chi2_contingency(gender_cross.to_numpy())

    result = pd.DataFrame({
        "N": gender_n,
        "%": gender_percent,
        "inadequate_n": gender_hl["sum"],
        "prevalence_percent": gender_hl["mean"] * 100,
    })

    result["p_value"] = p_value

    ci_low, ci_high = proportion_confint(
        count=gender_hl["sum"],
        nobs=gender_hl["count"],
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


df = pd.read_csv(DATA_PATH)
df_table2 = prepare_table2_data(df)

print_section("overall inadequate health literacy")
print(df_table2["inadequate_hl"].value_counts())
print(round(df_table2["inadequate_hl"].mean() * 100, 1))

print_section("gender result")
print(make_gender_table(df, df_table2))

print_section("note")
print("Table 2 may not fully match the published values when recalculated from this dataset.")
