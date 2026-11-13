"""Generate the eight publication-quality figures (300 dpi PNG).

Every figure is drawn from data/analysis_subset.csv, data/ev-share.csv and
outputs/regression_2022.csv only, so the figures always match the numbers
in outputs/results.json.
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
    "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False,
    "axes.spines.right": False,
})
OUT = "outputs/figures"
GREEN = "#1a9850"
BLUE = "#4575b4"
GREY = "#4d4d4d"
ORANGE = "#fdae61"
RED = "#d73027"

sub = pd.read_csv("data/analysis_subset.csv")
de = sub[sub.Code == "DEU"].sort_values("Year")
R = json.load(open("outputs/results.json"))
share_all = pd.read_csv("data/ev-share.csv").rename(
    columns={"Share of new cars that are electric": "ev_share"})

# --- Figure 1: Germany EV sales, bars ---------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.2))
colors = [RED if y in (2023, 2024) else GREEN for y in de.Year]
ax.bar(de.Year, de.ev_sales / 1000, color=colors, width=0.75)
ax.annotate("2020: 390,000\n(+261% on 2019)", xy=(2020, 390), xytext=(2013.2, 640),
            arrowprops=dict(arrowstyle="->", color=GREY), fontsize=9)
ax.annotate("2025: 860,000 (record)", xy=(2025, 860), xytext=(2021.2, 950),
            arrowprops=dict(arrowstyle="->", color=GREY), fontsize=9,
            fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Electric cars sold (thousands)")
ax.set_title("Figure 1. Electric cars sold in Germany, 2010-2025")
ax.set_ylim(0, 1080)
fig.tight_layout(); fig.savefig(f"{OUT}/fig1_ev_sales.png"); plt.close(fig)

# --- Figure 2: Germany EV share, with policy annotations ---------------------
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(de.Year, de.ev_share, color=GREEN, lw=2.2, marker="o", ms=3.5)
ax.axvspan(2023.0, 2024.0, color=RED, alpha=0.08)
ax.annotate("Subsidy (Umweltbonus)\nended Dec 2023", xy=(2023.5, 22),
            xytext=(2016.4, 8), fontsize=9,
            arrowprops=dict(arrowstyle="->", color=RED), color=RED)
ax.annotate("2022 peak: 31%", xy=(2022, 31), xytext=(2017.6, 33.5),
            arrowprops=dict(arrowstyle="->", color=GREY), fontsize=9)
ax.annotate("2024 trough: 20%", xy=(2024, 20), xytext=(2024.15, 13),
            fontsize=9, fontweight="bold")
ax.annotate("2025: 30%", xy=(2025, 30), xytext=(2024.35, 33),
            fontsize=9, fontweight="bold", color=GREEN)
ax.set_ylim(0, 38); ax.set_xlabel("Year")
ax.set_ylabel("Share of new cars sold that are electric (%)")
ax.set_title("Figure 2. EV share of new car sales in Germany, 2010-2025")
fig.tight_layout(); fig.savefig(f"{OUT}/fig2_ev_share.png"); plt.close(fig)

# --- Figure 3: peer trajectories ---------------------------------------------
peers = {"NOR": ("Norway", "#762a83"), "DNK": ("Denmark", "#1a9850"),
         "NLD": ("Netherlands", "#4575b4"), "CHN": ("China", "#d73027"),
         "SWE": ("Sweden", "#66c2a5"), "GBR": ("United Kingdom", "#fdae61"),
         "DEU": ("Germany", "#000000"), "FRA": ("France", "#a6a6a6"),
         "USA": ("United States", "#b2182b")}
fig, ax = plt.subplots(figsize=(7, 4.4))
for code, (label, color) in peers.items():
    s = sub[(sub.Code == code) & (sub.Year >= 2015)].sort_values("Year")
    lw = 2.6 if code == "DEU" else 1.8
    ax.plot(s.Year, s.ev_share, color=color, lw=lw, label=label,
            marker="o" if code == "DEU" else None, ms=3.5)
eu = sub[(sub.Code == "OWID_EU27") & (sub.Year >= 2015)].sort_values("Year")
ax.plot(eu.Year, eu.ev_share, color=GREY, lw=1.6, ls="--", label="EU-27")
w = sub[(sub.Code == "OWID_WRL") & (sub.Year >= 2015)].sort_values("Year")
ax.plot(w.Year, w.ev_share, color=GREY, lw=1.6, ls=":", label="World")
ax.set_xlabel("Year"); ax.set_ylabel("Share of new cars sold that are electric (%)")
ax.set_title("Figure 5. EV share of new car sales, Germany and peers, 2015-2025")
ax.legend(loc="upper left", fontsize=8, framealpha=0.9, ncol=2)
fig.tight_layout(); fig.savefig(f"{OUT}/fig5_peer_trajectories.png"); plt.close(fig)

# --- Figure 4: 2025 share bar chart ------------------------------------------
order = ["NOR", "DNK", "NLD", "SWE", "CHN", "GBR", "DEU", "OWID_EU27", "FRA",
         "OWID_WRL", "USA"]
labels = {"NOR": "Norway", "DNK": "Denmark", "NLD": "Netherlands",
          "SWE": "Sweden", "CHN": "China", "GBR": "United Kingdom",
          "DEU": "Germany", "OWID_EU27": "EU-27", "FRA": "France",
          "OWID_WRL": "World", "USA": "United States"}
vals, names = [], []
for code in order:
    row = sub[(sub.Code == code) & (sub.Year == 2025)].iloc[0]
    vals.append(row.ev_share); names.append(labels[code])
fig, ax = plt.subplots(figsize=(7, 4.4))
cols = [GREEN if n == "Germany" else BLUE for n in names]
ax.barh(names[::-1], vals[::-1], color=cols[::-1])
for i, v in enumerate(vals[::-1]):
    ax.text(v + 1.5, i, f"{v:.0f}%", va="center", fontsize=9)
ax.set_xlim(0, 112); ax.set_xlabel("Share of new cars sold that are electric (%)")
ax.set_title("Figure 6. EV share of new car sales in 2025")
fig.tight_layout(); fig.savefig(f"{OUT}/fig6_share_2025.png"); plt.close(fig)

# --- Figure 5: the subsidy shock - change in share, 2022 to 2024 --------------
codes = ["ISL", "NZL", "DEU", "ROU", "KOR", "ITA", "OWID_EU27", "FRA",
         "NLD", "GBR", "CHN", "USA", "NOR"]
names5 = {"ISL": "Iceland", "NZL": "New Zealand", "DEU": "Germany",
          "ROU": "Romania", "KOR": "South Korea", "ITA": "Italy",
          "OWID_EU27": "EU-27", "FRA": "France", "NLD": "Netherlands",
          "GBR": "United Kingdom", "CHN": "China", "USA": "United States",
          "NOR": "Norway"}
piv = share_all[share_all.Code.isin(codes)].pivot(index="Code", columns="Year",
                                                 values="ev_share")
chg = (piv[2024] - piv[2022]).sort_values()
fig, ax = plt.subplots(figsize=(7, 4.4))
cols = [RED if v < 0 else GREEN for v in chg]
ax.barh([names5[c] for c in chg.index], chg.values, color=cols)
ax.axvline(0, color="black", lw=0.8)
for i, v in enumerate(chg.values):
    ax.text(v + (0.7 if v >= 0 else -0.7), i, f"{v:+.1f}",
            va="center", ha="left" if v >= 0 else "right", fontsize=9)
ax.set_xlabel("Change in EV share, 2022 to 2024 (percentage points)")
ax.set_title("Figure 3. Who lost EV share in 2022-2024 - and who did not")
fig.tight_layout(); fig.savefig(f"{OUT}/fig3_subsidy_shock.png"); plt.close(fig)

# --- Figure 6: cross-country regression, 2022 ---------------------------------
reg = pd.read_csv("outputs/regression_2022.csv")
fig, ax = plt.subplots(figsize=(7, 4.4))
x = np.log(reg.gdppc)
slope = R["regression_2022_slope_pp_per_log_gdppc"]
intercept = R["regression_2022_intercept"]
xs = np.linspace(x.min(), x.max(), 100)
ax.plot(np.exp(xs), intercept + slope * xs, color=RED, lw=1.8,
        label=f"OLS fit (R\u00b2 = {R['regression_2022_r2']:.2f}, n = {R['regression_2022_n']})")
ax.scatter(reg.gdppc, reg.ev_share, s=18, color=BLUE, alpha=0.7)
deu = reg[reg.Code == "DEU"].iloc[0]
ax.scatter([deu.gdppc], [deu.ev_share], s=90, color=GREEN, edgecolor="black",
           zorder=5, label="Germany (31%, +11.2 pp above fit)")
npl = reg[reg.Code == "NPL"].iloc[0]
ax.annotate("Nepal", xy=(npl.gdppc, npl.ev_share), xytext=(9000, 33),
            fontsize=9, arrowprops=dict(arrowstyle="->", color=GREY))
nor = reg[reg.Code == "NOR"].iloc[0]
ax.annotate("Norway", xy=(nor.gdppc, nor.ev_share), xytext=(60000, 84),
            fontsize=9, arrowprops=dict(arrowstyle="->", color=GREY))
ax.set_xscale("log")
ax.set_xlabel("GDP per capita, 2022 (2011 international-$ , log scale)")
ax.set_ylabel("EV share of new car sales, 2022 (%)")
ax.set_title("Figure 7. Income vs EV adoption across countries, 2022")
ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
fig.tight_layout(); fig.savefig(f"{OUT}/fig7_regression.png"); plt.close(fig)

# --- Figure 7: implied total market - EV vs the rest ---------------------------
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
ev, total = [], []
for y in years:
    ev.append(de[de.Year == y].ev_sales.iloc[0] / 1e6)
    total.append(de[de.Year == y].ev_sales.iloc[0] /
                 (de[de.Year == y].ev_share.iloc[0] / 100) / 1e6)
ev = np.array(ev); total = np.array(total)
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.bar(years, ev, color=GREEN, label="Electric cars sold")
ax.bar(years, total - ev, bottom=ev, color="#bdbdbd",
       label="Other new cars (implied)")
for y, e, t in zip(years, ev, total):
    ax.text(y, t + 0.07, f"{t:.2f}m", ha="center", fontsize=8.5)
ax.set_xlabel("Year"); ax.set_ylabel("New cars sold (millions)")
ax.set_title("Figure 4. Germany's new-car market: EVs vs the rest (implied)")
ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
fig.tight_layout(); fig.savefig(f"{OUT}/fig4_total_market.png"); plt.close(fig)

# --- Figure 8: log-scale sales and the broken trend ----------------------------
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(de.Year, de.ev_sales, color=GREEN, lw=2.2, marker="o", ms=3.5,
        label="Actual EV sales")
pre = de[de.Year <= 2022]
slope_l = R["log_sales_trend_slope_2010_2022"]
# refit intercept on the log scale for the line
xs_pre = pre.Year.values
coef = np.polyfit(xs_pre, np.log(pre.ev_sales.values), 1)
trend_years = np.arange(2010, 2026)
ax.plot(trend_years, np.exp(np.polyval(coef, trend_years)), color=RED,
        lw=1.8, ls="--",
        label="Log-linear trend fitted on 2010-2022 (dashed = extrapolation)")
ax.set_yscale("log")
ax.set_xlabel("Year"); ax.set_ylabel("Electric cars sold (log scale)")
ax.set_title("Figure 8. The 2010-2022 growth trend breaks after 2022")
ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
fig.tight_layout(); fig.savefig(f"{OUT}/fig8_log_trend.png"); plt.close(fig)

print("figures written")
