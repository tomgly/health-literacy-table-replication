import pandas as pd
from scipy.stats import sem, t, ttest_ind, f_oneway
from pathlib import Path

DATA_PATH = "data/raw/hl_qol.csv"
OUTPUT_PATH = "outputs/table3_preview.csv"
EXCEL_OUTPUT_PATH = "outputs/table3_preview.xlsx"

TABLE3_BLOCKS = [
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


def mean_ci(series):
    n = series.count()
    mean = series.mean()
    se = sem(series, nan_policy="omit")
    ci = t.ppf(0.975, n - 1) * se
    return mean, mean - ci, mean + ci


def calculate_p_value(df, variable_name, category_order, score_name):
    groups = [
        df[df[variable_name] == category][score_name].dropna()
        for category in category_order
    ]

    if len(category_order) == 2:
        return ttest_ind(
            groups[0],
            groups[1],
            equal_var=True,
            nan_policy="omit",
        ).pvalue

    return f_oneway(*groups).pvalue


def make_table3_block(df, variable_name, category_order):
    rows = []

    for category in category_order:
        group = df[df[variable_name] == category]

        pcs_mean, pcs_low, pcs_high = mean_ci(group["pcs"])
        mcs_mean, mcs_low, mcs_high = mean_ci(group["mcs"])

        rows.append({
            "variable": variable_name,
            "category": category,
            "pcs_mean": round(pcs_mean, 1),
            "pcs_95_ci": f"{round(pcs_low, 1)}-{round(pcs_high, 1)}",
            "mcs_mean": round(mcs_mean, 1),
            "mcs_95_ci": f"{round(mcs_low, 1)}-{round(mcs_high, 1)}",
        })

    result = pd.DataFrame(rows)

    pcs_p_value = calculate_p_value(df, variable_name, category_order, "pcs")
    mcs_p_value = calculate_p_value(df, variable_name, category_order, "mcs")

    result["pcs_p_value"] = ""
    result["mcs_p_value"] = ""
    result.loc[0, "pcs_p_value"] = f"{pcs_p_value:.3f}"
    result.loc[0, "mcs_p_value"] = f"{mcs_p_value:.3f}"

    return result


df = pd.read_csv(DATA_PATH)

formatted_blocks = []

for variable_name, category_order in TABLE3_BLOCKS:
    result = make_table3_block(df, variable_name, category_order)
    formatted_blocks.append(result)

table3_preview = pd.concat(formatted_blocks, ignore_index=True)
Path("outputs").mkdir(exist_ok=True)
table3_preview.to_csv(OUTPUT_PATH, index=False)
table3_preview.to_excel(EXCEL_OUTPUT_PATH, index=False)

print(f"Saved preview to {OUTPUT_PATH}")
print(f"Saved Excel preview to {EXCEL_OUTPUT_PATH}")
