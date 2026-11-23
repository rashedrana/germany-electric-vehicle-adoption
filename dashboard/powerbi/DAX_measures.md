# DAX Measures — Germany EV Adoption (Power BI)

Model tables: `FactCountryYear`, `FactIndicator`, `FactCountryYear_Full`,
`DimCountry`, `DimYear`, `DimIndicator`.
Create a dedicated measure table (`_Measures`) in Power BI and paste these in one by one.
All measures respond to the Year and Country slicers unless stated otherwise.
`FactCountryYear` holds one row per country × year, so AVERAGE returns the
selected country-year value under the slicers (same pattern as Projects 1–2).

---

## Core measures (FactCountryYear)

```dax
EV Sales =
AVERAGE ( FactCountryYear[EVSales] )
```

```dax
EV Share % =
AVERAGE ( FactCountryYear[EVShare_Pct] )
```

```dax
Cumulative EV Sales =
AVERAGE ( FactCountryYear[CumulativeEVSales] )
```

```dax
Implied Total Market =
AVERAGE ( FactCountryYear[ImpliedTotalMarket] )
```

```dax
Non-EV Sales =
[Implied Total Market] - [EV Sales]
```

```dax
YoY Growth % =
AVERAGE ( FactCountryYear[YoYGrowth_Pct] )
```

## Target measures (Germany's 15m-by-2030 fleet goal)

```dax
Fleet Target 2030 =
15000000
```

```dax
Fleet Target Progress % =
DIVIDE ( [Cumulative EV Sales], [Fleet Target 2030] ) * 100
```

```dax
Fleet Target Gap =
[Fleet Target 2030] - [Cumulative EV Sales]
```

```dax
Required Annual Sales to Target =
DIVIDE ( [Fleet Target Gap], 2030 - MAX ( DimYear[Year] ) )
```

```dax
Required Pace vs 2025 Sales =
VAR Sales2025 =
    CALCULATE ( [EV Sales], DimYear[Year] = 2025, DimCountry[ISO_Code] = "DEU" )
RETURN
    DIVIDE ( [Required Annual Sales to Target], Sales2025 )
```

## Time-intelligence measures (vs start year 2010)

```dax
EV Sales (2010) =
CALCULATE ( [EV Sales], DimYear[Year] = 2010 )
```

```dax
EV Sales Change vs 2010 % =
DIVIDE ( [EV Sales] - [EV Sales (2010)], [EV Sales (2010)] ) * 100
```

```dax
EV Share Change vs 2010 (pp) =
[EV Share %] - CALCULATE ( [EV Share %], DimYear[Year] = 2010 )
```

```dax
EV Sales CAGR Since 2010 % =
VAR n = MAX ( DimYear[Year] ) - 2010
RETURN
    ( POWER ( DIVIDE ( [EV Sales], [EV Sales (2010)] ), DIVIDE ( 1, n ) ) - 1 ) * 100
```

```dax
Share Change 2022-2024 (pp) =
CALCULATE ( [EV Share %], DimYear[Year] = 2024 )
    - CALCULATE ( [EV Share %], DimYear[Year] = 2022 )
```

## World-relative measures

```dax
World EV Sales =
CALCULATE ( [EV Sales], DimCountry[ISO_Code] = "OWID_WRL" )
```

```dax
Share of World EV Sales % =
DIVIDE ( [EV Sales], [World EV Sales] ) * 100
```

```dax
Country Rank by EV Sales =
RANKX ( ALL ( DimCountry[Country] ), [EV Sales],, DESC, DENSE )
```

```dax
Country Rank by EV Share =
RANKX ( ALL ( DimCountry[Country] ), [EV Share %],, DESC, DENSE )
```

## Long-table measure (FactIndicator — any indicator via slicer)

```dax
Indicator Value =
AVERAGE ( FactIndicator[Value] )
```

## Cross-section measure (FactCountryYear_Full — all 64 entities)

```dax
EV Share 2025 % =
CALCULATE ( AVERAGE ( FactCountryYear_Full[EVShare_Pct] ), DimYear[Year] = 2025 )
```

## Display helpers

```dax
Selected Country =
SELECTEDVALUE ( DimCountry[Country], "All countries" )
```

```dax
Selected Year Label =
"Focus year: " & SELECTEDVALUE ( DimYear[Year], 2025 )
```

## Retrofit measures (Q15–Q19 visuals)

```dax
EV Share 2015 % =
CALCULATE ( [EV Share %], DimYear[Year] = 2015 )
```

```dax
EV Share Change 2015-2025 (pp) =
CALCULATE ( [EV Share %], DimYear[Year] = 2025 ) - [EV Share 2015 %]
```
(Drives the Q15 slope chart — one line per country between the two years.)

```dax
EVs per 100 New Cars =
ROUND ( [EV Share %], 0 )
```
(Drives the Q17 waffle chart — filled squares out of 100.)

```dax
Required Fleet Path (DE) =
VAR StartFleet =
    CALCULATE ( [Cumulative EV Sales], DimYear[Year] = 2025, DimCountry[ISO_Code] = "DEU" )
VAR AnnualNeed =
    DIVIDE ( [Fleet Target 2030] - StartFleet, 5 )
RETURN
    StartFleet + AnnualNeed * ( MAX ( DimYear[Year] ) - 2025 )
```
(Drives the Q18 step line — the straight-line path from the 2025 fleet to
15,000,000 at 2030; plot alongside [Cumulative EV Sales] with stepped lines.)

```dax
Countries at 50%+ Share (2025) =
CALCULATE (
    COUNTROWS ( DimCountry ),
    FILTER ( DimCountry, CALCULATE ( [EV Share %], DimYear[Year] = 2025 ) >= 50 )
)
```
(Supporting count for the Q19 tile map — run over the full country
dimension restricted to Europe it returns 6 for 2025: Norway, Denmark,
Iceland, Sweden, the Netherlands and Finland.)

---

Notes
- KPI cards on Page 1 use: EV Sales, EV Share %, Cumulative EV Sales,
  YoY Growth %, Implied Total Market, Share of World EV Sales % — each with
  its "vs 2010" companion measure as the delta visual.
- The gauge on Page 1 uses [Fleet Target Progress %] (Germany selected)
  with the maximum set to 100 so it reads as progress to the 15m target.
- Implied Total Market and Cumulative EV Sales are derived in data prep
  exactly as in the paper (total = sales ÷ share; fleet proxied by
  cumulative sales, ignoring scrappage) and are labelled as derivations.
- `Share Change 2022-2024 (pp)` drives the subsidy-shock comparison visual;
  Germany is the only panel country with a negative value.
