import pandas as pd
from statsmodels.stats.proportion import proportion_confint

DATA_PATH = "data/raw/hl_qol.csv"


def print_section(title):
    print(f"\n--- {title} ---")


def prepare_table2_data(df):
    # Table 2ではhealth literacyが欠損している行を除外する
    df_table2 = df.dropna(subset=["hltcatnew"]).copy()
    df_table2["inadequate_hl"] = df_table2["hltcatnew"].eq("inadequate")
    return df_table2


def make_gender_table(df, df_table2):
    gender_n = df["Gender"].value_counts().sort_index()
    gender_percent = gender_n / len(df) * 100

    gender_hl = (
        df_table2
        .groupby("Gender")["inadequate_hl"]
        .agg(["count", "sum", "mean"])
        .sort_index()
    )

    result = pd.DataFrame({
        "N": gender_n,
        "%": gender_percent,
        "inadequate_n": gender_hl["sum"],
        "prevalence_percent": gender_hl["mean"] * 100,
    })

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
    })


df = pd.read_csv(DATA_PATH)
df_table2 = prepare_table2_data(df)

print_section("overall inadequate health literacy")
print(df_table2["inadequate_hl"].value_counts())
print(round(df_table2["inadequate_hl"].mean() * 100, 1))

print_section("gender result")
print(make_gender_table(df, df_table2))
