-- Q1. Germany: EV sales and EV share of new cars, 2010-2025
SELECT s.Year AS year, s.ev_sales, sh.ev_share AS ev_share_pct
FROM ev_sales s
JOIN ev_share sh ON s.Code = sh.Code AND s.Year = sh.Year
WHERE s.Code = 'DEU'
ORDER BY year;

-- Q2. Largest EV markets in 2025 (sales)
SELECT Entity AS country, ev_sales
FROM ev_sales
WHERE Year = 2025 AND Code NOT LIKE 'OWID_%'
ORDER BY ev_sales DESC
LIMIT 10;

-- Q3. Highest EV shares of new-car sales in 2025
SELECT Entity AS country, ev_share AS ev_share_pct
FROM ev_share
WHERE Year = 2025 AND Code NOT LIKE 'OWID_%'
ORDER BY ev_share DESC
LIMIT 10;

-- Q4. Germany: year-on-year change in EV sales
SELECT Year AS year, ev_sales,
       ROUND(100.0 * (ev_sales - LAG(ev_sales) OVER (ORDER BY Year))
             / LAG(ev_sales) OVER (ORDER BY Year), 1) AS yoy_change_pct
FROM ev_sales
WHERE Code = 'DEU'
ORDER BY year;

-- Q5. Germany vs the EU-27: EV share, 2020-2025
SELECT sh.Year AS year,
       MAX(CASE WHEN sh.Code = 'DEU' THEN sh.ev_share END) AS germany_pct,
       MAX(CASE WHEN sh.Code = 'OWID_EU27' THEN sh.ev_share END) AS eu27_pct,
       MAX(CASE WHEN sh.Code = 'OWID_WRL' THEN sh.ev_share END) AS world_pct
FROM ev_share sh
WHERE sh.Code IN ('DEU', 'OWID_EU27', 'OWID_WRL') AND sh.Year >= 2020
GROUP BY sh.Year
ORDER BY year;

-- Q6. Germany: cumulative EV sales (proxy for the EV fleet on the road)
SELECT Year AS year, ev_sales,
       SUM(ev_sales) OVER (ORDER BY Year) AS cumulative_ev_sales
FROM ev_sales
WHERE Code = 'DEU'
ORDER BY year;

-- Q7. Cross-country regression input: EV share vs GDP per capita, 2022
SELECT sh.Entity AS country, sh.ev_share AS ev_share_pct,
       ROUND(g.gdppc, 0) AS gdp_per_capita_usd
FROM ev_share sh
JOIN gdp_pc g ON sh.Code = g.iso_code
WHERE sh.Year = 2022 AND sh.Code NOT LIKE 'OWID_%'
ORDER BY ev_share DESC;

-- Q8. Which countries lost EV share between 2022 and 2024?
SELECT a.Entity AS country, a.ev_share AS share_2022, b.ev_share AS share_2024,
       ROUND(b.ev_share - a.ev_share, 1) AS change_pp
FROM ev_share a
JOIN ev_share b ON a.Code = b.Code AND b.Year = 2024
WHERE a.Year = 2022 AND a.Code NOT LIKE 'OWID_%'
ORDER BY change_pp ASC
LIMIT 10;

-- Q9. World and EU-27 EV sales, 2020-2025
SELECT Year AS year,
       MAX(CASE WHEN Code = 'OWID_WRL' THEN ev_sales END) AS world_ev_sales,
       MAX(CASE WHEN Code = 'OWID_EU27' THEN ev_sales END) AS eu27_ev_sales
FROM ev_sales
WHERE Code IN ('OWID_WRL', 'OWID_EU27') AND Year >= 2020
GROUP BY Year
ORDER BY year;
