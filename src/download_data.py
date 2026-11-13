"""Download the source datasets into data/.

Sources (all published by Our World in Data, CC BY, compiled from the
International Energy Agency's Global EV Outlook and the World Bank):
  * ev-sales.csv  - Electric cars sold per country/year (BEV + PHEV),
    OWID grapher dataset "electric-car-sales", source IEA.
  * ev-share.csv  - Share of new cars sold that are electric (BEV + PHEV),
    OWID grapher dataset "electric-car-sales-share", source IEA.
  * owid-co2-data.csv - OWID CO2 dataset; used here only for GDP per capita
    (gdp / population, 2011 international-$) in the cross-country regression.
Run once before src/analysis.py.
"""
import urllib.request

FILES = {
    "data/ev-sales.csv":
        "https://ourworldindata.org/grapher/electric-car-sales.csv",
    "data/ev-share.csv":
        "https://ourworldindata.org/grapher/electric-car-sales-share.csv",
    "data/owid-co2-data.csv":
        "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
}

for path, url in FILES.items():
    print(f"downloading {url} -> {path}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(path, "wb") as out:
        out.write(resp.read())
print("done")
