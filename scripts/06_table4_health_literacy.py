import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import sem, t

DATA_PATH = "data/raw/hl_qol.csv"
HL_ORDER = ["inadequate", "marginal", "adequate"]
REFERENCE_CATEGORY = "adequate"


def print_section(title):
    print(f"\n--- {title} ---")


def mean_ci(series):
    n = series.count()
    mean = series.mean()
    se = sem(series, nan_policy="omit")
    ci = t.ppf(0.975, n - 1) * se
    return mean, mean - ci, mean + ci


def prepare_table4_data(df):
    return df.dropna(subset=["hltcatnew"]).copy()


def make_mean_rows(df_table4):
    rows = []

    for category in HL_ORDER:
        group = df_table4[df_table4["hltcatnew"] == category]

        pcs_mean, pcs_low, pcs_high = mean_ci(group["pcs"])
        mcs_mean, mcs_low, mcs_high = mean_ci(group["mcs"])

        rows.append({
            "health_literacy": category,
            "n": len(group),
            "pcs_mean": round(pcs_mean, 1),
            "pcs_95_ci": f"{pcs_low:.1f}-{pcs_high:.1f}",
            "mcs_mean": round(mcs_mean, 1),
            "mcs_95_ci": f"{mcs_low:.1f}-{mcs_high:.1f}",
        })

    return pd.DataFrame(rows)


def fit_crude_model(df_table4, score_name):
    formula = (
        f'{score_name} ~ '
        f'C(hltcatnew, Treatment(reference="{REFERENCE_CATEGORY}"))'
    )
    return smf.ols(formula, data=df_table4).fit()


def find_model_term(model, category):
    for term in model.params.index:
        if f"[T.{category}]" in term:
            return term
    return None


def format_beta_ci(model, category):
    if category == REFERENCE_CATEGORY:
        return "Ref"

    term = find_model_term(model, category)
    if term is None:
        return ""

    beta = model.params[term]
    ci_low, ci_high = model.conf_int().loc[term]
    return f"{beta:.1f} ({ci_low:.1f} to {ci_high:.1f})"


def make_table4_preview(df_table4):
    result = make_mean_rows(df_table4)

    pcs_model = fit_crude_model(df_table4, "pcs")
    mcs_model = fit_crude_model(df_table4, "mcs")

    result["pcs_beta_crude_95_ci"] = [
        format_beta_ci(pcs_model, category)
        for category in result["health_literacy"]
    ]
    result["mcs_beta_crude_95_ci"] = [
        format_beta_ci(mcs_model, category)
        for category in result["health_literacy"]
    ]

    return result


df = pd.read_csv(DATA_PATH)
df_table4 = prepare_table4_data(df)
table4_preview = make_table4_preview(df_table4)

print_section("table4 preview")
print(table4_preview.to_string(index=False))

print_section("note")
print("This preview includes means and crude regression coefficients only.")
