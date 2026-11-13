# SQL query results

Produced by `src/build_db.py` running `sql/queries.sql` against `ev.db`.

## Q1. Germany: EV sales and EV share of new cars, 2010-2025

```sql
SELECT s.Year AS year, s.ev_sales, sh.ev_share AS ev_share_pct
FROM ev_sales s
JOIN ev_share sh ON s.Code = sh.Code AND s.Year = sh.Year
WHERE s.Code = 'DEU'
ORDER BY year;
```

|   year |   ev_sales |   ev_share_pct |
|-------:|-----------:|---------------:|
|   2010 |        140 |         0.0049 |
|   2011 |       1640 |         0.052  |
|   2012 |       3400 |         0.11   |
|   2013 |       6800 |         0.23   |
|   2014 |      13500 |         0.45   |
|   2015 |      23000 |         0.73   |
|   2016 |      24000 |         0.74   |
|   2017 |      54000 |         1.6    |
|   2018 |      67000 |         2      |
|   2019 |     108000 |         3      |
|   2020 |     390000 |        14      |
|   2021 |     690000 |        26      |
|   2022 |     830000 |        31      |
|   2023 |     700000 |        24      |
|   2024 |     570000 |        20      |
|   2025 |     860000 |        30      |

## Q2. Largest EV markets in 2025 (sales)

```sql
SELECT Entity AS country, ev_sales
FROM ev_sales
WHERE Year = 2025 AND Code NOT LIKE 'OWID_%'
ORDER BY ev_sales DESC
LIMIT 10;
```

| country        |   ev_sales |
|:---------------|-----------:|
| China          |   13300000 |
| United States  |    1530000 |
| Germany        |     860000 |
| United Kingdom |     700000 |
| France         |     450000 |
| Turkey         |     237000 |
| Spain          |     230000 |
| Netherlands    |     228000 |
| South Korea    |     217000 |
| Italy          |     193000 |

## Q3. Highest EV shares of new-car sales in 2025

```sql
SELECT Entity AS country, ev_share AS ev_share_pct
FROM ev_share
WHERE Year = 2025 AND Code NOT LIKE 'OWID_%'
ORDER BY ev_share DESC
LIMIT 10;
```

| country     |   ev_share_pct |
|:------------|---------------:|
| Norway      |             97 |
| Denmark     |             71 |
| Nepal       |             68 |
| Iceland     |             62 |
| Sweden      |             61 |
| Netherlands |             58 |
| Finland     |             57 |
| China       |             53 |
| Belgium     |             44 |
| Vietnam     |             40 |

## Q4. Germany: year-on-year change in EV sales

```sql
SELECT Year AS year, ev_sales,
       ROUND(100.0 * (ev_sales - LAG(ev_sales) OVER (ORDER BY Year))
             / LAG(ev_sales) OVER (ORDER BY Year), 1) AS yoy_change_pct
FROM ev_sales
WHERE Code = 'DEU'
ORDER BY year;
```

|   year |   ev_sales |   yoy_change_pct |
|-------:|-----------:|-----------------:|
|   2010 |        140 |            nan   |
|   2011 |       1640 |           1071.4 |
|   2012 |       3400 |            107.3 |
|   2013 |       6800 |            100   |
|   2014 |      13500 |             98.5 |
|   2015 |      23000 |             70.4 |
|   2016 |      24000 |              4.3 |
|   2017 |      54000 |            125   |
|   2018 |      67000 |             24.1 |
|   2019 |     108000 |             61.2 |
|   2020 |     390000 |            261.1 |
|   2021 |     690000 |             76.9 |
|   2022 |     830000 |             20.3 |
|   2023 |     700000 |            -15.7 |
|   2024 |     570000 |            -18.6 |
|   2025 |     860000 |             50.9 |

## Q5. Germany vs the EU-27: EV share, 2020-2025

```sql
SELECT sh.Year AS year,
       MAX(CASE WHEN sh.Code = 'DEU' THEN sh.ev_share END) AS germany_pct,
       MAX(CASE WHEN sh.Code = 'OWID_EU27' THEN sh.ev_share END) AS eu27_pct,
       MAX(CASE WHEN sh.Code = 'OWID_WRL' THEN sh.ev_share END) AS world_pct
FROM ev_share sh
WHERE sh.Code IN ('DEU', 'OWID_EU27', 'OWID_WRL') AND sh.Year >= 2020
GROUP BY sh.Year
ORDER BY year;
```

|   year |   germany_pct |   eu27_pct |   world_pct |
|-------:|--------------:|-----------:|------------:|
|   2020 |            14 |         10 |         4.4 |
|   2021 |            26 |         18 |         9.3 |
|   2022 |            31 |         21 |        15   |
|   2023 |            24 |         22 |        18   |
|   2024 |            20 |         21 |        21   |
|   2025 |            30 |         27 |        25   |

## Q6. Germany: cumulative EV sales (proxy for the EV fleet on the road)

```sql
SELECT Year AS year, ev_sales,
       SUM(ev_sales) OVER (ORDER BY Year) AS cumulative_ev_sales
FROM ev_sales
WHERE Code = 'DEU'
ORDER BY year;
```

|   year |   ev_sales |   cumulative_ev_sales |
|-------:|-----------:|----------------------:|
|   2010 |        140 |                   140 |
|   2011 |       1640 |                  1780 |
|   2012 |       3400 |                  5180 |
|   2013 |       6800 |                 11980 |
|   2014 |      13500 |                 25480 |
|   2015 |      23000 |                 48480 |
|   2016 |      24000 |                 72480 |
|   2017 |      54000 |                126480 |
|   2018 |      67000 |                193480 |
|   2019 |     108000 |                301480 |
|   2020 |     390000 |                691480 |
|   2021 |     690000 |               1381480 |
|   2022 |     830000 |               2211480 |
|   2023 |     700000 |               2911480 |
|   2024 |     570000 |               3481480 |
|   2025 |     860000 |               4341480 |

## Q7. Cross-country regression input: EV share vs GDP per capita, 2022

```sql
SELECT sh.Entity AS country, sh.ev_share AS ev_share_pct,
       ROUND(g.gdppc, 0) AS gdp_per_capita_usd
FROM ev_share sh
JOIN gdp_pc g ON sh.Code = g.iso_code
WHERE sh.Year = 2022 AND sh.Code NOT LIKE 'OWID_%'
ORDER BY ev_share DESC;
```

| country              |   ev_share_pct |   gdp_per_capita_usd |
|:---------------------|---------------:|---------------------:|
| Norway               |          89    |                88390 |
| Iceland              |          69    |                42116 |
| Sweden               |          54    |                47125 |
| Denmark              |          38    |                50726 |
| Finland              |          38    |                40607 |
| Netherlands          |          35    |                49128 |
| Germany              |          31    |                46495 |
| China                |          29    |                18921 |
| Nepal                |          29    |                 3229 |
| Belgium              |          26    |                42062 |
| Switzerland          |          26    |                63623 |
| Luxembourg           |          24    |                55300 |
| New Zealand          |          24    |                39091 |
| Austria              |          22    |                43997 |
| Ireland              |          22    |                60350 |
| Portugal             |          22    |                28387 |
| United Kingdom       |          22    |                38358 |
| France               |          20    |                40309 |
| Singapore            |          15    |                81736 |
| Israel               |          12    |                36990 |
| South Korea          |           9.6  |                41280 |
| Canada               |           9.5  |                45369 |
| Romania              |           9    |                26334 |
| Spain                |           8.9  |                33979 |
| Hungary              |           8.6  |                29469 |
| Italy                |           8.5  |                35828 |
| Latvia               |           8.1  |                27244 |
| Greece               |           7.9  |                25344 |
| Lithuania            |           7.9  |                30109 |
| United States        |           7.7  |                57075 |
| Costa Rica           |           7.6  |                15811 |
| Jordan               |           7.2  |                 8820 |
| Slovenia             |           6.2  |                32803 |
| Poland               |           5.9  |                32070 |
| United Arab Emirates |           5.8  |                76127 |
| Cyprus               |           5.4  |                25729 |
| Estonia              |           5.4  |                29627 |
| Australia            |           5.1  |                51305 |
| Croatia              |           5    |                26180 |
| Bulgaria             |           4    |                20274 |
| Czechia              |           3.9  |                32133 |
| Slovakia             |           3.7  |                27472 |
| Laos                 |           3.2  |                 7270 |
| Japan                |           2.8  |                38197 |
| Vietnam              |           2.6  |                 8365 |
| Thailand             |           2.3  |                15671 |
| Colombia             |           2.2  |                14355 |
| Seychelles           |           1.7  |                24323 |
| India                |           1.4  |                 7350 |
| Indonesia            |           1.4  |                12553 |
| Turkey               |           1.3  |                27407 |
| Brazil               |           1.2  |                15156 |
| Mexico               |           0.96 |                15810 |
| Chile                |           0.6  |                22929 |
| Malaysia             |           0.49 |                25294 |
| Cambodia             |           0.45 |                 3787 |
| South Africa         |           0.17 |                11600 |
| Philippines          |           0.15 |                 8905 |
| Russia               |           0.13 |                25632 |

## Q8. Which countries lost EV share between 2022 and 2024?

```sql
SELECT a.Entity AS country, a.ev_share AS share_2022, b.ev_share AS share_2024,
       ROUND(b.ev_share - a.ev_share, 1) AS change_pp
FROM ev_share a
JOIN ev_share b ON a.Code = b.Code AND b.Year = 2024
WHERE a.Year = 2022 AND a.Code NOT LIKE 'OWID_%'
ORDER BY change_pp ASC
LIMIT 10;
```

| country      |   share_2022 |   share_2024 |   change_pp |
|:-------------|-------------:|-------------:|------------:|
| Iceland      |        69    |        43    |       -26   |
| New Zealand  |        24    |        11    |       -13   |
| Germany      |        31    |        20    |       -11   |
| Romania      |         9    |         6.5  |        -2.5 |
| South Korea  |         9.6  |         7.4  |        -2.2 |
| Italy        |         8.5  |         7.5  |        -1   |
| Croatia      |         5    |         4.9  |        -0.1 |
| Japan        |         2.8  |         2.8  |         0   |
| South Africa |         0.17 |         0.54 |         0.4 |
| India        |         1.4  |         2.1  |         0.7 |

## Q9. World and EU-27 EV sales, 2020-2025

```sql
SELECT Year AS year,
       MAX(CASE WHEN Code = 'OWID_WRL' THEN ev_sales END) AS world_ev_sales,
       MAX(CASE WHEN Code = 'OWID_EU27' THEN ev_sales END) AS eu27_ev_sales
FROM ev_sales
WHERE Code IN ('OWID_WRL', 'OWID_EU27') AND Year >= 2020
GROUP BY Year
ORDER BY year;
```

|   year |   world_ev_sales |   eu27_ev_sales |
|-------:|-----------------:|----------------:|
|   2020 |          2980000 |         1050000 |
|   2021 |          6600000 |         1760000 |
|   2022 |         10200000 |         1980000 |
|   2023 |         13700000 |         2420000 |
|   2024 |         17500000 |         2270000 |
|   2025 |         21200000 |         2900000 |
