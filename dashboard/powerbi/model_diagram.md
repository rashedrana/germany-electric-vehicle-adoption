# Star Schema — Germany EV Adoption (Power BI model)

```
                    DimCountry                      DimYear
                 (CountryKey PK)                 (YearKey PK)
                  Country, ISO_Code,              Year, Phase
                  EntityType                          |
                        |                              |
          +-------------+--------------+---------------+-----------+
          |                            |                           |
  FactCountryYear              FactIndicator            FactCountryYear_Full
  (CountryKey FK,              (CountryKey FK,           (CountryKey FK,
   YearKey FK,                  YearKey FK,               YearKey FK,
   EVSales,                     IndicatorKey FK,          EVSales,
   EVShare_Pct,                 Value)                    EVShare_Pct,
   CumulativeEVSales,                 |                   CumulativeEVSales,
   ImpliedTotalMarket,          DimIndicator              ImpliedTotalMarket,
   YoYGrowth_Pct)              (IndicatorKey PK)          YoYGrowth_Pct)
                                Indicator, IndicatorCode,
                                Category, Unit
```

## Tables (CSVs in `data/`)
| Table | Grain | Rows | Contents |
|---|---|---|---|
| FactCountryYear | country × year | 159 | Wide table: the 10-country peer panel (2010–2025) with EV sales, EV share and the derived cumulative sales, implied total market and YoY growth |
| FactIndicator | country × year × indicator | 318 | Long table: the 2 source indicators for the panel |
| FactCountryYear_Full | country × year | 823 | Wide table for all 64 entities in the OWID extract (2010–2025) |
| FactIndicator_Full | country × year × indicator | 1,699 | Long table for all 64 entities: EV sales (822 rows) + EV share (816) + the 2022 GDP-per-capita cross-section (59) |
| DimCountry | country | 10 | Germany, France, United Kingdom, Netherlands, Denmark, Norway, Sweden, China, United States, European Union (27) |
| DimCountry_Full | country | 64 | Every country/aggregate in the OWID extract, flagged Country vs Aggregate (Europe, EU27, Rest of World, World) |
| DimYear | year | 16 | 2010–2025, with the paper's phase band (Take-off 2010–19 · Boom 2020–22 · Subsidy shock 2023–24 · Rebound 2025) |
| DimIndicator | indicator | 3 | EV sales, EV share, and GDP per capita 2022 (the regression cross-section), with category and unit |

## Design notes
- Two fact shapes share the conformed DimCountry and DimYear dimensions: a wide
  country-year table for the KPI/chart measures, and a long indicator table so
  any series can be sliced by DimIndicator[Category] — the same pattern as
  Projects 1 and 2.
- Total fact rows: **2,999**. The EV panel is intrinsically smaller than
  Projects 1–2 (16 years × 64 entities is everything the source holds) — the
  count is stated openly, and no rows are padded or interpolated.
- Derived columns (in FactCountryYear and its _Full counterpart) are computed
  in data prep exactly as in the paper: cumulative sales = running sum of
  annual sales (the fleet proxy behind the 15m-target gap); implied total
  market = EV sales ÷ EV share; YoY growth = change vs the previous year.
  All three are labelled derivations, not source data.
- Coverage gaps are real source gaps, kept as missing rows: a few small
  markets enter the OWID panel after 2010, and 6 entity-years carry sales
  without a published share (so no implied market can be computed for them).
- Source data: `data/ev-sales.csv` + `data/ev-share.csv` + `outputs/regression_2022.csv`
  of this repository (Our World in Data / IEA, accessed November 2026) — the
  same dataset used in the research paper, so the dashboard and the paper
  always agree number for number.
