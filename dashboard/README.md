# Germany EV Adoption — Interactive Dashboard

The interactive companion to this repository's research paper
(*From 140 to 860,000: Electric Vehicle Adoption in Germany, 2010–2025 —
Growth, the Subsidy Shock, and the European Comparison*).
Same data, same numbers — the paper explains the adoption story, this
dashboard lets you explore it.

## Web edition (live, no install)
Open `index.html` in a browser (or via GitHub Pages). Features:

- **Country buttons** — Germany plus France, the UK, the Netherlands,
  Denmark, Norway, Sweden, China, the US and the EU as the main view
- **Focus-year slider (2010–2025)** — every KPI card and the country
  comparison update to the selected year
- **Metric switch** — the trend chart flips between EV sales, EV share and
  cumulative sales; per-country show/hide toggles
- **6 KPI cards** with change vs the start year (2010), a year-on-year
  growth chart (boom, subsidy shock, rebound), the implied whole-market
  split (EV vs other cars), the road-to-15-million target trajectory, a
  top-12 share league table for 2025, and a 59-country scatter (EV share vs
  income, 2022)
- Clicking a bar in the country comparison switches the whole dashboard to
  that country

## Power BI edition (build guide)
Everything needed to rebuild this as a native Power BI report sits in `powerbi/`:

- `powerbi/data/` — star-schema CSVs (4 fact tables, 4 dimensions; see
  `powerbi/model_diagram.md`). Two sizes: the paper's 10-country peer panel
  (159 country-years, 318 long fact rows), and the **full dataset — 64
  countries/aggregates in the dimension, 823 wide fact rows and 1,699 long
  fact rows** (`*_Full.csv`), which the report is built on (default view:
  Germany). Total: **2,999 fact rows**. The EV source is a compact annual
  panel (16 years × 64 entities) — smaller than Projects 1–2, stated openly;
  every row is a real published OWID/IEA value, nothing is padded.
- `powerbi/DAX_measures.md` — all measures, copy-paste ready (sales, share,
  cumulative fleet, implied market, YoY and CAGR, vs-2010 deltas, the
  15m-target pace measures, ranks)
- `powerbi/QUESTIONS.md` — 14 business questions, each solved with a different
  Power BI visual type (KPI cards, gauge, waterfall, treemap, scatter, map,
  ribbon, matrix…), with the verified answers
- `powerbi/layout_spec.md` — page-by-page layout in modern end-to-end project
  style: slicer header, KPI row, bookmark metric switching, drill-through
  country page, navigation buttons, exact color palette

On a Windows PC with Power BI Desktop: load the CSVs, set the relationships
in `model_diagram.md`, paste the DAX, and place the visuals per the layout spec.

## Data
Our World in Data (based on the IEA Global EV Outlook) via `data/ev-sales.csv`
and `data/ev-share.csv` in this repository, plus the paper's 2022 income
cross-section (`outputs/regression_2022.csv`) — 64 countries/aggregates ×
16 years (2010–2025). Electric cars are battery-electric and plug-in hybrid
combined; the source carries **no BEV/PHEV split**, so neither does the
dashboard. Cumulative sales (fleet proxy), implied total market (sales ÷
share) and YoY growth are derived exactly as in the paper and labelled as
derivations. Coverage gaps are kept as gaps, never filled.
