# From 140 to 860,000: Electric Vehicle Adoption in Germany, 2010–2025

A data-analysis project (Python + SQL) on how electric cars went from a
rounding error to 30% of new car sales in Germany — and what happened
when the purchase subsidy was suddenly removed. Germany is compared
with European peers, China, the United States and the world to show
that the 2023–2024 collapse was a German policy event, not a market
collapse.

**Data (100% real, published sources):** International Energy Agency
(Global EV Outlook) electric-car sales and market-share series, via
Our World in Data; GDP per capita from the World Bank via the OWID CO₂
dataset — see `src/download_data.py`. Every number below is produced
by `src/analysis.py` / `sql/queries.sql` and stored in
`outputs/results.json` / `outputs/sql_results.md`; nothing is typed by
hand. "Electric car" means battery-electric plus plug-in hybrid
throughout, as in the IEA series.

## Key findings

1. **Fifteen years of near-unbroken growth.** Germany sold **140**
   electric cars in 2010 and **860,000 in 2025** (a 6,142.9-fold
   increase); the electric share of new car sales rose from **0.005%
   to 30.0%**. Sales grew at **106.3% per year** (CAGR) between 2010
   and 2022, doubling roughly every **1.1 years**.
2. **The take-off came in 2020.** Sales jumped **261.1% in one year**
   (108,000 → 390,000) and the share leapt from 3% to 14%, as the
   purchase subsidy was raised to up to €9,000 and the EU fleet CO₂
   target of 95 g/km took effect.
3. **The subsidy shock of 2023–2024.** After the Umweltbonus was cut
   in January 2023 and terminated in December 2023, German electric
   sales fell **31.3%** (830,000 → 570,000) and the share fell **11
   percentage points** (31% → 20%) — while the EU-27 share was flat
   and France (+4.0), the Netherlands (+13.0), the UK (+5.0) and
   China (+19.0 points) all gained. Germany was the third-largest
   share loser in the world, after Iceland (−26) and New Zealand
   (−13); New Zealand had likewise just removed its purchase
   subsidy, the Clean Car Discount, on 31 December 2023.
4. **It was a share collapse, not a market collapse.** The implied
   total new-car market was 2.68 million in 2022 and 2.85 million in
   2024 (+6.4%): buyers kept buying cars, they stopped buying
   electric ones.
5. **The 2025 rebound came without a subsidy.** Sales rose **50.9%**
   to a record **860,000** and the share recovered to **30.0%** —
   before the new income-graduated purchase grant (from 1 January
   2026) existed.
6. **Third in volume, 19th in share.** In 2025 Germany was the
   world's third-largest electric market (860,000 sales, 4.1% of the
   21.2 million sold worldwide) but only 19th of 59 countries by
   share — behind Norway (97%), Denmark (71%), the Netherlands (58%)
   and China (53%).
7. **Income explains little.** Across 59 countries in 2022, EV share
   rises with log GDP per capita (OLS slope 10.63 points per log
   unit, R² = 0.19, p = 0.0006), but Germany sat **11.2 points above**
   its income-predicted share (31.0% vs 19.8%): policy, not income,
   does the heavy lifting.
8. **The 2030 target is out of reach on this trajectory.** Cumulative
   electric sales by 2025 were **4.34 million**; reaching 15 million
   electric cars on the road by 2030 needs about **2.13 million
   sales per year** — **2.48 times** the record 2025 pace.

## Project structure

```
germany-electric-vehicle-adoption/
├── README.md
├── requirements.txt
├── data/
│   ├── ev-sales.csv            # IEA via OWID: electric cars sold
│   ├── ev-share.csv            # IEA via OWID: EV share of new cars
│   ├── owid-co2-data.csv       # OWID: GDP per capita (to 2022)
│   └── analysis_subset.csv     # Germany + peers, 2010-2025
├── src/
│   ├── download_data.py        # fetch the three source datasets
│   ├── analysis.py             # all headline numbers -> outputs/results.json
│   ├── build_db.py             # build ev.db, run sql/queries.sql
│   └── figures.py              # 8 figures, 300 dpi -> outputs/figures/
├── sql/queries.sql             # 9 documented SQL queries
├── outputs/
│   ├── results.json            # every headline number
│   ├── germany_yearly.csv      # Germany 2010-2025
│   ├── regression_2022.csv     # cross-country regression input
│   ├── sql_results.md          # query results
│   └── figures/fig1_...fig8_...png
└── paper/
    ├── paper.md                # full paper (single-column source)
    ├── paper_twocol.md         # same paper (two-column source)
    ├── paper.docx / paper_twocol.docx
    └── build_journal.py        # journal-format builder (Times New Roman)
```

The paper PDFs are **not** in this repository by design: the author
keeps them out of GitHub until journal submission. The paper is
available here as `.md` and `.docx`.

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/download_data.py
python src/analysis.py
python src/build_db.py
python src/figures.py
python paper/build_journal.py paper/paper_twocol.md --two-col
python paper/build_journal.py paper/paper.md
```

## Paper

Rashed Rana (2026). "From 140 to 860,000: Electric Vehicle Adoption
in Germany, 2010–2025 — Growth, the Subsidy Shock, and the European
Comparison." Manuscript prepared for journal submission. The paper was
prepared with AI assistance for data analysis and drafting, under the
author's direction; all results were computed from the published
datasets with the code in this repository.
