"""Electric vehicle adoption in Germany, 2010-2025.

Main analysis for the project *germany-electric-vehicle-adoption*.
Data: Our World in Data grapher datasets (source: IEA Global EV Outlook)
  * data/ev-sales.csv - electric cars sold (battery-electric + plug-in
    hybrid) per country and year,
  * data/ev-share.csv - share of new cars sold that are electric (BEV+PHEV),
  * data/owid-co2-data.csv - used only for GDP per capita (gdp/population,
    2011 international-$) in the cross-country regression; GDP is published
    through 2022 in this file, so the cross-section uses 2022.

The script:
  1. extracts Germany + comparator countries/aggregates into
     data/analysis_subset.csv,
  2. computes every headline finding used in the README and the paper,
  3. writes the numbers to outputs/results.json so that no number in any
     document is typed by hand.
"""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm

PEERS = ["DEU", "FRA", "GBR", "NLD", "DNK", "NOR", "CHN", "USA", "SWE"]
AGGREGATES = ["OWID_EU27", "OWID_WRL"]
YEARS = range(2010, 2026)


def cagr(first, last, n_years):
    return (last / first) ** (1 / n_years) - 1


def linfit(x, y):
    """Simple OLS: returns slope, intercept, Pearson r, R^2."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    slope, intercept = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]
    return slope, intercept, r, r ** 2


def main():
    sales = pd.read_csv("data/ev-sales.csv")
    share = pd.read_csv("data/ev-share.csv")
    sales = sales.rename(columns={"Electric cars sold": "ev_sales"})
    share = share.rename(columns={"Share of new cars that are electric": "ev_share"})
    df = sales.merge(share, on=["Entity", "Code", "Year"], how="outer")
    df = df.sort_values(["Code", "Year"])

    keep = PEERS + AGGREGATES
    sub = df[df.Code.isin(keep) & df.Year.isin(YEARS)].copy()
    sub.to_csv("data/analysis_subset.csv", index=False)

    de = sub[sub.Code == "DEU"].set_index("Year")
    R = {"data_rows_germany": int(len(de)),
         "years": [int(de.index.min()), int(de.index.max())]}

    # --- Finding 1: growth 2010 -> 2025 --------------------------------------
    s10, s25 = de.loc[2010, "ev_sales"], de.loc[2025, "ev_sales"]
    sh10, sh25 = de.loc[2010, "ev_share"], de.loc[2025, "ev_share"]
    R["sales_2010"] = int(s10)
    R["sales_2025"] = int(s25)
    R["sales_multiple"] = round(float(s25 / s10), 1)
    R["share_2010_pct"] = round(float(sh10), 3)
    R["share_2025_pct"] = round(float(sh25), 1)
    R["sales_cagr_2010_2022_pct"] = round(
        float(cagr(de.loc[2010, "ev_sales"], de.loc[2022, "ev_sales"], 12)) * 100, 1)
    R["sales_cagr_2010_2025_pct"] = round(
        float(cagr(s10, s25, 15)) * 100, 1)

    # --- Finding 2: the 2020 take-off ----------------------------------------
    R["sales_2019"] = int(de.loc[2019, "ev_sales"])
    R["sales_2020"] = int(de.loc[2020, "ev_sales"])
    R["sales_2021"] = int(de.loc[2021, "ev_sales"])
    R["sales_2022"] = int(de.loc[2022, "ev_sales"])
    R["share_2019_pct"] = round(float(de.loc[2019, "ev_share"]), 1)
    R["share_2020_pct"] = round(float(de.loc[2020, "ev_share"]), 1)
    R["share_2021_pct"] = round(float(de.loc[2021, "ev_share"]), 1)
    R["share_2022_pct"] = round(float(de.loc[2022, "ev_share"]), 1)
    R["sales_growth_2019_2020_pct"] = round(
        float(de.loc[2020, "ev_sales"] / de.loc[2019, "ev_sales"] - 1) * 100, 1)

    # --- Finding 3: the subsidy shock, 2023-2024 ------------------------------
    R["sales_2023"] = int(de.loc[2023, "ev_sales"])
    R["sales_2024"] = int(de.loc[2024, "ev_sales"])
    R["share_2023_pct"] = round(float(de.loc[2023, "ev_share"]), 1)
    R["share_2024_pct"] = round(float(de.loc[2024, "ev_share"]), 1)
    R["sales_change_2022_2024_pct"] = round(
        float(de.loc[2024, "ev_sales"] / de.loc[2022, "ev_sales"] - 1) * 100, 1)
    R["share_change_2022_2024_pp"] = round(
        float(de.loc[2024, "ev_share"] - de.loc[2022, "ev_share"]), 1)
    R["sales_change_2024_2025_pct"] = round(
        float(de.loc[2025, "ev_sales"] / de.loc[2024, "ev_sales"] - 1) * 100, 1)
    R["share_change_2024_2025_pp"] = round(
        float(de.loc[2025, "ev_share"] - de.loc[2024, "ev_share"]), 1)
    # peers over the same window (share, percentage points)
    for code in ["OWID_EU27", "FRA", "NLD", "GBR", "CHN", "USA", "NOR"]:
        s = sub[sub.Code == code].set_index("Year")["ev_share"]
        R[f"peer_{code}_share_2022"] = round(float(s.loc[2022]), 1)
        R[f"peer_{code}_share_2024"] = round(float(s.loc[2024]), 1)
        R[f"peer_{code}_share_2025"] = round(float(s.loc[2025]), 1)
        R[f"peer_{code}_change_2022_2024_pp"] = round(
            float(s.loc[2024] - s.loc[2022]), 1)
    # implied total new-car market (EV sales / EV share)
    de_total = (de["ev_sales"] / (de["ev_share"] / 100)).round(0)
    for yr in [2019, 2020, 2022, 2023, 2024, 2025]:
        R[f"implied_total_market_{yr}"] = int(de_total.loc[yr])
    R["implied_total_change_2022_2024_pct"] = round(
        float(de_total.loc[2024] / de_total.loc[2022] - 1) * 100, 1)

    # --- Finding 4: cumulative fleet proxy ------------------------------------
    R["cumulative_ev_sales_2010_2025"] = int(de["ev_sales"].sum())
    R["cumulative_ev_sales_2010_2022"] = int(de.loc[2010:2022, "ev_sales"].sum())
    R["cumulative_ev_sales_2010_2024"] = int(de.loc[2010:2024, "ev_sales"].sum())

    # --- Finding 5: 2025 international comparison ----------------------------
    comp = {}
    for code in PEERS + AGGREGATES:
        row = sub[(sub.Code == code) & (sub.Year == 2025)]
        if row.empty:
            continue
        row = row.iloc[0]
        comp[code] = {
            "country": row["Entity"],
            "ev_sales_2025": (int(row["ev_sales"]) if pd.notna(row["ev_sales"]) else None),
            "ev_share_2025": round(float(row["ev_share"]), 1),
        }
        s = sub[sub.Code == code].set_index("Year")["ev_share"]
        comp[code]["ev_share_2015"] = round(float(s.loc[2015]), 2) if 2015 in s.index and pd.notna(s.loc[2015]) else None
        comp[code]["ev_share_2020"] = round(float(s.loc[2020]), 1) if pd.notna(s.loc[2020]) else None
    R["comparison_2025"] = comp
    # Germany's rank by share and by sales among countries in 2025
    sh25_all = share[share.Year == 2025].dropna(subset=["Code"])
    sh25_all = sh25_all[~sh25_all.Code.str.startswith("OWID_")]
    R["germany_share_rank_2025"] = int(
        (sh25_all["ev_share"] > sh25).sum() + 1)
    R["countries_with_2025_share"] = int(len(sh25_all))
    sa25_all = sales[sales.Year == 2025].dropna(subset=["Code"])
    sa25_all = sa25_all[~sa25_all.Code.str.startswith("OWID_")]
    R["germany_sales_rank_2025"] = int(
        (sa25_all["ev_sales"] > s25).sum() + 1)
    R["world_ev_sales_2025"] = int(
        sales[(sales.Code == "OWID_WRL") & (sales.Year == 2025)]["ev_sales"].iloc[0])
    R["germany_share_of_world_ev_sales_2025_pct"] = round(
        float(s25 / R["world_ev_sales_2025"]) * 100, 1)
    R["world_ev_share_2025"] = round(float(
        share[(share.Code == "OWID_WRL") & (share.Year == 2025)]["ev_share"].iloc[0]), 1)

    # --- Finding 6: cross-country regression, 2022 ---------------------------
    # GDP per capita (2011 int-$) from the OWID CO2 dataset; published to 2022.
    co2 = pd.read_csv("data/owid-co2-data.csv", usecols=["iso_code", "year", "gdp", "population"])
    co2 = co2[co2.year == 2022].copy()
    co2["gdppc"] = co2["gdp"] / co2["population"]
    cs = share[share.Year == 2022][["Code", "ev_share"]].dropna()
    cs = cs[~cs.Code.str.startswith("OWID_")].drop_duplicates("Code")
    m = cs.merge(co2[["iso_code", "gdppc"]], left_on="Code", right_on="iso_code",
                 how="inner").dropna()
    m["log_gdppc"] = np.log(m["gdppc"])
    X = sm.add_constant(m["log_gdppc"])
    model = sm.OLS(m["ev_share"], X).fit()
    R["regression_2022_n"] = int(len(m))
    R["regression_2022_slope_pp_per_log_gdppc"] = round(float(model.params["log_gdppc"]), 2)
    R["regression_2022_intercept"] = round(float(model.params["const"]), 2)
    R["regression_2022_r2"] = round(float(model.rsquared), 3)
    R["regression_2022_p_slope"] = float(model.pvalues["log_gdppc"])
    R["regression_2022_corr"] = round(
        float(np.corrcoef(m["log_gdppc"], m["ev_share"])[0, 1]), 3)
    # sensitivity: Nepal is an outlier (29% share at $3,229 GDP per capita,
    # driven by a near-total EV import-tax exemption); refit without it.
    m2 = m[m.Code != "NPL"]
    model2 = sm.OLS(m2["ev_share"], sm.add_constant(m2["log_gdppc"])).fit()
    R["regression_2022_ex_nepal_n"] = int(len(m2))
    R["regression_2022_ex_nepal_slope"] = round(float(model2.params["log_gdppc"]), 2)
    R["regression_2022_ex_nepal_r2"] = round(float(model2.rsquared), 3)
    R["regression_2022_ex_nepal_p_slope"] = float(model2.pvalues["log_gdppc"])
    # scenario: sales grow 20% every year from the 2025 level
    scen = [R["sales_2025"] * (1.2 ** k) for k in range(1, 6)]
    R["scenario_20pct_sales_2030"] = int(round(scen[-1]))
    R["scenario_20pct_total_2026_2030"] = int(round(sum(scen)))
    R["nepal_share_2022"] = round(float(m[m.Code == "NPL"]["ev_share"].iloc[0]), 1)
    R["nepal_gdppc_2022"] = round(float(m[m.Code == "NPL"]["gdppc"].iloc[0]), 0)
    deu_row = m[m.Code == "DEU"].iloc[0]
    R["germany_gdppc_2022"] = round(float(deu_row["gdppc"]), 0)
    R["germany_share_2022"] = round(float(deu_row["ev_share"]), 1)
    pred_deu = float(model.predict([1, np.log(deu_row["gdppc"])])[0])
    R["germany_predicted_share_2022"] = round(pred_deu, 1)
    R["germany_residual_2022_pp"] = round(float(deu_row["ev_share"] - pred_deu), 1)
    m.to_csv("outputs/regression_2022.csv", index=False)

    # --- Finding 8: the 2030 target arithmetic --------------------------------
    # Germany's stated target: 15 million electric cars on the road by 2030.
    # Cumulative sales 2010-2025 are an upper-bound proxy for the fleet
    # (retirements are ignored, so the true fleet is smaller).
    target = 15_000_000
    R["target_2030_ev_fleet"] = target
    R["target_gap_vs_cumulative_2025"] = int(target - R["cumulative_ev_sales_2010_2025"])
    R["target_required_sales_per_year_2026_2030"] = int(
        round((target - R["cumulative_ev_sales_2010_2025"]) / 5))
    R["target_multiple_of_2025_sales"] = round(
        float(R["target_required_sales_per_year_2026_2030"] / R["sales_2025"]), 2)
    pre = de.loc[2010:2022]
    slope, intercept, r, r2 = linfit(pre.index, np.log(pre["ev_sales"]))
    R["log_sales_trend_slope_2010_2022"] = round(float(slope), 3)
    R["log_sales_trend_r2"] = round(float(r2), 3)
    R["log_sales_doubling_years"] = round(float(np.log(2) / slope), 2)
    for yr in [2023, 2024, 2025]:
        trend = float(np.exp(intercept + slope * yr))
        actual = float(de.loc[yr, "ev_sales"])
        R[f"trend_sales_{yr}"] = int(round(trend))
        R[f"shortfall_vs_trend_{yr}_pct"] = round((actual / trend - 1) * 100, 1)
    # share trend 2010-2022 (percentage points per year)
    slope_sh, _, r_sh, r2_sh = linfit(pre.index, pre["ev_share"])
    R["share_trend_pp_per_year_2010_2022"] = round(float(slope_sh), 2)
    R["share_trend_r2"] = round(float(r2_sh), 3)

    with open("outputs/results.json", "w") as f:
        json.dump(R, f, indent=2)
    de.reset_index().to_csv("outputs/germany_yearly.csv", index=False)
    print(json.dumps(R, indent=2))


if __name__ == "__main__":
    main()
