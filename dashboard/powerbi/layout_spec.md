# Power BI Layout Spec — Germany EV Adoption Dashboard

Design language follows modern end-to-end Power BI project style (cf. "The Developer"
YouTube channel's end-to-end dashboard projects): a clean canvas, a slicer header,
rounded KPI cards, bookmark-driven metric switching and page-navigation buttons.
The web edition in `dashboard/index.html` is the visual reference — build the PBIX
to match it page for page.

## Global formatting
- Page size: 16:9 (1280 × 720)
- Background: #F7F6FA · Cards: white, subtle shadow, rounded-corner shape underlay
- Accent: purple #7C3AED · Secondary blue #0078D4
- Font: Segoe UI (titles bold 14–16 pt, KPI values bold 20–24 pt, body 10–11 pt)
- Country colors: Germany #7C3AED · France #0078D4 · United Kingdom #D97706 ·
  Netherlands #0891B2 · Denmark #DC2626 · Norway #059669 · Sweden #65A30D ·
  China #DB2777 · United States #475569 · European Union (27) #A8A29E
- Growth bars: positive #059669 · negative #DC2626 · Market split: EV #7C3AED,
  other cars #C9C2DD

## Data model (Get Data → the CSVs in `powerbi/data/`)
Build on the **full dataset** (`FactCountryYear_Full.csv`, `FactIndicator_Full.csv`,
`DimCountry_Full.csv` + shared `DimYear.csv`, `DimIndicator.csv`): 64 countries/
aggregates in the dimension, 823 wide fact rows, 1,699 long fact rows. The focus
files (`FactCountryYear.csv`, `FactIndicator.csv`, `DimCountry.csv`) are the
paper's 10-country peer panel — same model, numbers agree. Default the country
slicer to Germany.
Relationships (single direction, from dims to facts):
- DimCountry[CountryKey] → FactCountryYear[CountryKey], FactIndicator[CountryKey], FactCountryYear_Full[CountryKey]
- DimYear[YearKey] → FactCountryYear[YearKey], FactIndicator[YearKey], FactCountryYear_Full[YearKey]
- DimIndicator[IndicatorKey] → FactIndicator[IndicatorKey], FactIndicator_Full[IndicatorKey]
Hide all key columns. Paste all measures from `DAX_measures.md` into a `_Measures` table.

## Page 1 — Overview (the page from the video-style template)
Slicer header (top band, synced to all pages):
- Country: chiclet slicer (DimCountry[Country]), single select, Germany default
- Year: slider slicer (DimYear[Year]) + a card showing [Selected Year Label]
- Metric switch: three buttons (EV sales / EV share / Cumulative sales) wired to
  bookmarks that swap the main trend visual's measure (field parameter is the
  modern alternative — either is fine)

KPI card row (6 cards, each with its vs-2010 delta underneath):
1. EV Sales · 2. EV Share % · 3. Cumulative EV Sales · 4. YoY Growth % ·
5. Implied Total Market · 6. Share of World EV Sales %

Visuals:
- Main trend: line chart, axis DimYear[Year], values = bookmark-switched measure,
  legend DimCountry[Country] (all 10 panel countries shown, toggled by buttons)
- Right: clustered column — EV Share % by DimCountry[Country] for the selected
  year, country colors, drill-through enabled to Page 3
- Gauge (small, under the KPI row): Fleet Target Progress % (Germany), max 100
- Bottom left: bar — YoY Growth % per year for the selected country,
  conditional formatting green/red
- Bottom right: stacked column — EV vs Non-EV Sales per year (implied market
  split) for the selected country

## Page 2 — Shock & Target Deep-Dive
- Waterfall: Δ EV Sales by phase (2010→19, 2019→22, 2022→24, 2024→25), Germany
- Bar: Share Change 2022-2024 (pp) by panel country, sorted ascending —
  Germany alone in negative territory
- Area: Cumulative EV Sales per year, Germany
- Combo (bar + line): cumulative fleet bars with the required-pace and
  flat-2025-pace projection lines to 2030 (static reference table built from
  the paper's target arithmetic: gap 10,658,520 ÷ 5 years = 2,131,704/yr)
- Decomposition tree: EV Sales change 2022→2024 → share effect × market effect

## Page 3 — Country Comparison (drill-through target)
- Horizontal bar: EV Share % 2025, top 12 countries (FactCountryYear_Full,
  aggregates filtered out via DimCountry[EntityType] = "Country")
- Filled map: EV Share % by country, 2025
- Treemap: EV Sales by country, 2025
- Donut: share of world EV sales, 2025 (top 5 + rest)
- Ribbon: Germany's rank by EV Sales across years (Country Rank by EV Sales)
- Scatter: EV Share % (y) vs GDP per capita 2022 (x, log axis) from
  FactIndicator_Full (IndicatorKey 3), Germany highlighted
- Drill-through filter: DimCountry[Country]

## Page 4 — About & Method
- Text box: research question, headline findings (sales 140 → 860,000;
  subsidy shock −31.3% across 2022–2024 while the total market grew +6.4%;
  rebound +50.9% in 2025 at 30.0% share; 15m-by-2030 target needs 2.48× the
  2025 pace; income explains only 19% of cross-country adoption)
- Method note: electric cars are BEV + PHEV combined (no split in the source);
  fleet is proxied by cumulative sales (scrappage ignored), total market is
  implied as sales ÷ share — both exactly as in the paper
- Data source: Our World in Data, based on the IEA Global EV Outlook
  (accessed Nov 2026); GDP per capita from the OWID CO2 dataset (2022)
- Links (buttons with web URL actions): GitHub project, portfolio site
- Note: companion research paper by Rashed Rana

## Navigation
Left vertical button bar on every page (home icon style): Overview · Shock &
Target · Countries · About — page navigator or buttons with "Page navigation"
actions, selected page highlighted in the accent color.

## Publish checklist
- [ ] All slicers synced across pages 1–3
- [ ] Bookmarks tested (metric switch)
- [ ] Drill-through from Page 1 comparison bar to Page 3 works
- [ ] Mobile layout: KPI cards 2 × 3, trend chart full width
- [ ] File saved as `Germany_EV_Adoption.pbix` next to this spec
