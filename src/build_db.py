"""Build the SQLite database used by sql/queries.sql and check its answers.

Creates ev.db with three tables from the downloaded data:
  * ev_sales - electric cars sold (BEV + PHEV), IEA via OWID,
  * ev_share - share of new cars sold that are electric, IEA via OWID,
  * gdp_pc   - GDP per capita (2011 international-$), OWID CO2 dataset.
Runs every query in sql/queries.sql and writes the results to
outputs/sql_results.md so the README and paper can cite SQL output that
was actually produced by the queries.
"""
import sqlite3
import pandas as pd

sales = pd.read_csv("data/ev-sales.csv").rename(
    columns={"Electric cars sold": "ev_sales"})
share = pd.read_csv("data/ev-share.csv").rename(
    columns={"Share of new cars that are electric": "ev_share"})
co2 = pd.read_csv("data/owid-co2-data.csv", usecols=["iso_code", "year", "gdp", "population"])
gdp_pc = co2[co2.year == 2022].copy()
gdp_pc["gdppc"] = gdp_pc["gdp"] / gdp_pc["population"]
gdp_pc = gdp_pc[["iso_code", "gdppc"]]

con = sqlite3.connect("ev.db")
sales.to_sql("ev_sales", con, if_exists="replace", index=False)
share.to_sql("ev_share", con, if_exists="replace", index=False)
gdp_pc.to_sql("gdp_pc", con, if_exists="replace", index=False)

with open("sql/queries.sql") as f:
    script = f.read()

blocks, current = [], []
for line in script.splitlines():
    if line.startswith("-- Q") and current:
        blocks.append("\n".join(current))
        current = [line]
    else:
        current.append(line)
if current:
    blocks.append("\n".join(current))

out = ["# SQL query results\n",
       "Produced by `src/build_db.py` running `sql/queries.sql` against "
       "`ev.db`.\n"]
for block in blocks:
    lines = [l for l in block.splitlines() if not l.strip().startswith("-- ====")]
    title = next((l[3:].strip() for l in lines if l.startswith("-- Q")), "Query")
    sql = "\n".join(l for l in lines if not l.startswith("--")).strip()
    if not sql:
        continue
    df = pd.read_sql_query(sql, con)
    out.append(f"## {title}\n")
    out.append("```sql\n" + sql + "\n```\n")
    out.append(df.to_markdown(index=False) + "\n")

with open("outputs/sql_results.md", "w") as f:
    f.write("\n".join(out))
con.close()
print("ev.db built; outputs/sql_results.md written")
