import pandas as pd
from scipy.stats import sem, t, ttest_ind

DATA_PATH = "data/raw/hl_qol.csv"
GENDER_ORDER = ["Male", "Female"]


def print_section(title):
    print(f"\n--- {title} ---")


def mean_ci(series):
    n = series.count()
    mean = series.mean()
    se = sem(series, nan_policy="omit")
    ci = t.ppf(0.975, n - 1) * se
    return mean, mean - ci, mean + ci


def make_table3_gender(df):
    rows = []

    for gender in GENDER_ORDER:
        group = df[df["Gender"] == gender]

        pcs_mean, pcs_low, pcs_high = mean_ci(group["pcs"])
        mcs_mean, mcs_low, mcs_high = mean_ci(group["mcs"])

        rows.append({
            "Gender": gender,
            "pcs_mean": round(pcs_mean, 1),
            "pcs_95_ci": f"{round(pcs_low, 1)}-{round(pcs_high, 1)}",
            "mcs_mean": round(mcs_mean, 1),
            "mcs_95_ci": f"{round(mcs_low, 1)}-{round(mcs_high, 1)}",
        })

    result = pd.DataFrame(rows)

    male = df[df["Gender"] == "Male"]
    female = df[df["Gender"] == "Female"]

    pcs_p_value = ttest_ind(
        male["pcs"],
        female["pcs"],
        equal_var=True,
        nan_policy="omit",
    ).pvalue

    mcs_p_value = ttest_ind(
        male["mcs"],
        female["mcs"],
        equal_var=True,
        nan_policy="omit",
    ).pvalue

    result["pcs_p_value"] = ""
    result["mcs_p_value"] = ""
    result.loc[0, "pcs_p_value"] = f"{pcs_p_value:.3f}"
    result.loc[0, "mcs_p_value"] = f"{mcs_p_value:.3f}"

    return result


df = pd.read_csv(DATA_PATH)
result = make_table3_gender(df)

print_section("gender result")
print(result)
