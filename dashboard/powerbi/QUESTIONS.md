# Business Questions & Chart Problem-Solving
## Germany EV Adoption Dashboard — 14 questions, 14 visual types

Dataset: Our World in Data (based on the IEA Global EV Outlook), the dataset of
this repository's research paper: **64 countries/aggregates in the dimension ·
10-country peer panel 2010–2025 · 59-country income cross-section for 2022 ·
2,999 fact rows** across the four fact tables (country × year wide table,
country × year × indicator long table, and their full-dataset counterparts).
Every answer below was computed from the project data and cross-checked
against the research paper — the dashboard and the paper agree number for
number (e.g. Germany's EV sales 140 in 2010 → 860,000 in 2025 in both).
Electric cars = battery-electric + plug-in hybrid combined; the source data
has no BEV/PHEV split, so no question pretends otherwise.

---

**Q1. Where does German EV adoption stand in the selected year — at a glance?**
Visual: **KPI cards** (EV Sales, EV Share %, Cumulative EV Sales, YoY Growth %,
Implied Total Market, Share of World EV Sales) with vs-2010 deltas.
Answer (2025): **860,000 EVs sold** (6,143× the 140 of 2010) · **30.0% share**
of new cars (+30.0 pp) · **4,341,480 cumulative** sales since 2010 · **+50.9%**
growth year-on-year · implied total market 2,866,667 cars · **4.1% of world
EV sales**.

**Q2. How close is Germany to its 15-million-by-2030 fleet target?**
Visual: **Gauge** — cumulative EV sales (fleet proxy, the paper's method)
against the 15,000,000 target.
Answer: 4,341,480 by end-2025 = **28.9% of the target**. The remaining gap is
10,658,520 cars in five years — **2,131,704 sales per year, 2.48× the 2025
pace**. At a flat 2025 pace Germany would reach only ~8.64m by 2030.

**Q3. How did adoption unfold from 2010 to 2025?**
Visual: **Line chart** with bookmark metric switch (EV sales / EV share /
cumulative sales), 10 peer countries + slicer.
Answer: Sales grew from **140 (2010) to 860,000 (2025)** — a 6,143× increase,
a **78.9% compound annual growth rate**. Share rose from 0.005% to 30.0%.
Growth came in waves: a slow take-off to 108,000 by 2019, a subsidy-fuelled
boom to 830,000 by 2022, a two-year dip, then the 2025 rebound.

**Q4. How does Germany's 2025 share compare with its peers?**
Visual: **Clustered column chart** (EV share by panel country, 2025).
Answer: Norway 97.0%, Denmark 71.0%, Sweden 61.0%, Netherlands 58.0%,
China 53.0%, United Kingdom 35.0%, **Germany 30.0%**, European Union (27)
27.0%, France 26.0%, United States 10.0%. Germany sits mid-pack — ahead of
the EU average, far behind the Nordic leaders.

**Q5. Which periods built — and destroyed — German EV sales?**
Visual: **Waterfall chart** (Δ annual EV sales by phase, Germany).
Answer: 2010→2019 **+107,860** (the long take-off) · 2019→2022 **+722,000**
(the subsidy boom) · 2022→2024 **−260,000** (the subsidy shock) ·
2024→2025 **+290,000** (the rebound). Net 2010→2025: +859,860.

**Q6. Was the 2023–24 dip a German story or a global one?**
Visual: **Bar chart** of EV-share change in percentage points, 2022 → 2024,
panel countries sorted.
Answer: **A German story.** Germany lost **−11.0 pp** (31% → 20%) while every
peer gained or held: China +19.0 pp, Denmark +18.0, Netherlands +13.0,
United Kingdom +5.0, France +4.0, Sweden +4.0, Norway +3.0, United States
+2.3, EU27 0.0. Germany is the only panel country whose share fell — the
January 2023 subsidy cut (and the end of PHEV support) hit a market that had
been pulled forward by the bonus.

**Q7. Did the whole car market shrink, or just the EV slice?**
Visual: **Stacked column chart** (implied market split: EV vs other cars,
Germany).
Answer: The market **grew**. Implied total sales rose from 2,677,419 (2022)
to 2,850,000 (2024), +6.4% — while EV sales fell from 830,000 to 570,000 and
non-EV sales jumped from 1,847,419 to 2,280,000. Buyers didn't stop buying
cars; they switched back to combustion when the bonus ended.

**Q8. How young is Germany's EV fleet?**
Visual: **Area chart** (cumulative EV sales, Germany).
Answer: Very young — **49.1% of every EV ever sold in Germany was sold in
2023–2025 alone** (2,130,000 of 4,341,480). Nearly half the fleet arrived in the
last three years, subsidy shock included; the pre-2020 fleet is just
301,480 cars (6.9%).

**Q9. Does being rich explain EV adoption?**
Visual: **Scatter chart** — EV share (y) vs GDP per capita (x, log scale),
59 countries, 2022 (the paper's regression sample).
Answer: Partly. The fitted slope is **+10.63 pp of EV share per log unit of
GDP per capita** (p = 0.0006), but income explains only **18.9%** of the
variation (R² = 0.189). Germany (31.0% at $46,495 per capita) sits
**+11.2 pp above** its income-predicted share of 19.8% — policy, not just
wealth. Nepal is the famous outlier: 29.0% share on $3,229 per capita.

**Q10. Where in the world is the new-car market most electric?**
Visual: **Filled map** (EV share of new cars by country, 2025).
Answer: Norway **97.0%**, Denmark 71.0%, Nepal 68.0%, Iceland 62.0%,
Sweden 61.0% and the Netherlands 58.0% top the map. Germany's 30.0% ranks
**#19 of the 59 countries** with 2025 data — respectable in volume terms
(see Q11), mid-table in share terms.

**Q11. Where are the world's EVs actually sold?**
Visual: **Treemap** (EV sales by country, 2025).
Answer: China dominates with **13,300,000** of the world's 21,200,000 EVs,
ahead of the United States 1,530,000 and **Germany 860,000 — #3 in the
world by volume**, then the United Kingdom 700,000 and France 450,000.
Germany's share rank (#19) and volume rank (#3) tell opposite stories:
a big market at a middling adoption rate.

**Q12. How did Germany's volume ranking evolve?**
Visual: **Ribbon chart** (Germany's rank by EV sales among countries, by year).
Answer: **#8 in 2010** (140 cars) → #7 in 2015 → **#2 in 2020** (390,000,
the first bonus-boom year, behind only China) → #3 in 2022 → **#3 in 2025**.
Germany has been a top-3 EV market by volume since 2022 even while its
share ranking slid from #7 (2022) to #19 (2025) as smaller markets
electrified faster.

**Q13. What does the world's 2025 EV market look like?**
Visual: **Donut chart** (share of world EV sales, 2025).
Answer: China **62.7%**, United States 7.2%, Germany 4.1%, United Kingdom
3.3%, France 2.1%, rest of the world 20.6%. Nearly two of every three EVs
sold on Earth in 2025 were sold in China.

**Q14. What do the phases show — and what actually drove the 2022→24 decline?**
Visual: **Matrix with conditional formatting** (phase averages, Germany) +
**decomposition tree** (sales change → share effect × market-size effect).
Answer: Phase means — average EV share 0.9% (2010–19 take-off) → 23.7%
(2020–22 boom) → 22.0% (2023–24 shock) → 30.0% (2025 rebound); sales CAGR
+109.3%/yr → +97.3%/yr → **−17.1%/yr** → +50.9%. The decomposition of the
decline is unambiguous: sales −31.3% = EV share −35.5% (relative) × total
market **+6.4%**. The market grew; the share collapsed. The shock was a
policy-and-mix event, not a demand collapse.

---

Coverage checklist (Power BI visual palette): KPI card ✓ · gauge ✓ · line ✓ ·
clustered column ✓ · waterfall ✓ · bar (change) ✓ · stacked column ✓ ·
area ✓ · scatter ✓ · filled map ✓ · treemap ✓ · ribbon ✓ · donut ✓ ·
matrix + decomposition tree ✓ — plus slicers, bookmarks and drill-through
(layout spec).
