import csv
import json
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set
from urllib.parse import urlencode
from urllib.request import Request, urlopen


WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"


@dataclass
class Country:
    id: str
    name: str
    region_value: str  # WB region label (used as a proxy for continent)


def http_get_json(path: str, params: Dict[str, str]) -> Tuple[Dict, List[Dict]]:
    query = urlencode(params)
    url = f"{WORLD_BANK_API_BASE}{path}?{query}"
    req = Request(url, headers={"User-Agent": "wb-client/1.0"})
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not isinstance(data, list) or len(data) < 2:
        raise RuntimeError(f"Unexpected response from World Bank API: {url}")
    return data[0], data[1]


def fetch_countries() -> List[Country]:
    countries: List[Country] = []
    page = 1
    while True:
        meta, rows = http_get_json(
            "/country",
            {
                "format": "json",
                "per_page": "400",
                "page": str(page),
            },
        )
        for row in rows:
            # Filter out aggregates: region.id == 'NA' are aggregates in WB API
            region = row.get("region", {})
            if region and region.get("id") == "NA":
                continue
            income_level = row.get("incomeLevel", {})
            if income_level and income_level.get("id") == "NA":
                # Defensive: exclude non-applicable income aggregates
                continue
            iso3 = row.get("id")
            name = row.get("name")
            if not iso3 or not name:
                continue
            region_value = (region or {}).get("value") or "Unknown"
            countries.append(Country(id=iso3, name=name, region_value=region_value))
        if page >= meta.get("pages", 1):
            break
        page += 1
    return countries


def fetch_un_member_iso3_to_region() -> Dict[str, str]:
    """Return mapping of ISO3 -> continent using Rest Countries for UN members only."""
    url = "https://restcountries.com/v3.1/all?fields=cca3,region,unMember"
    req = Request(url, headers={"User-Agent": "wb-client/1.0"})
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    iso3_to_region: Dict[str, str] = {}
    for row in data:
        if not isinstance(row, dict):
            continue
        if not row.get("unMember"):
            continue
        iso3 = row.get("cca3")
        region = row.get("region") or "Unknown"
        if iso3:
            iso3_to_region[iso3] = region
    return iso3_to_region


def fetch_indicator_latest(indicator: str, years: List[int]) -> Dict[str, Tuple[int, Optional[float]]]:
    """Return mapping: country_iso3 -> (year, value or None) for first available year in years order."""
    results: Dict[str, Tuple[int, Optional[float]]] = {}
    # Fetch all data for the full year range in one call for performance
    start, end = min(years), max(years)
    page = 1
    while True:
        meta, rows = http_get_json(
            f"/country/all/indicator/{indicator}",
            {
                "format": "json",
                "per_page": "20000",
                "page": str(page),
                "date": f"{start}:{end}",
            },
        )
        for row in rows:
            country = row.get("countryiso3code")
            year_str = row.get("date")
            value = row.get("value")
            if not country or not year_str:
                continue
            try:
                year = int(year_str)
            except ValueError:
                continue
            if year not in years:
                continue
            # Record first available by preferred order
            existing = results.get(country)
            if existing is None:
                if value is not None:
                    results[country] = (year, float(value))
                else:
                    # Keep track of missing to possibly fill with older year later
                    results[country] = (year, None)
            else:
                # If we had None and now have a value for an earlier-preferred year, replace
                prev_year, prev_val = existing
                if prev_val is None:
                    # Prefer earliest in the provided order; since API returns mixed order,
                    # rely on the explicit years list priority.
                    if years.index(year) < years.index(prev_year):
                        results[country] = (year, float(value) if value is not None else None)
        if page >= meta.get("pages", 1):
            break
        page += 1
    return results


def build_dataset(output_csv_path: str, target_years: List[int]) -> None:
    countries = fetch_countries()
    country_index: Dict[str, Country] = {c.id: c for c in countries}

    # Restrict to UN member states and map to continents
    un_iso3_to_continent = fetch_un_member_iso3_to_region()
    un_iso3_set: Set[str] = set(un_iso3_to_continent.keys())

    # GDP per capita (constant USD): NY.GDP.PCAP.CD (current US$)
    gdp_pc_map = fetch_indicator_latest("NY.GDP.PCAP.CD", target_years)
    pop_map = fetch_indicator_latest("SP.POP.TOTL", target_years)

    rows_out: List[Dict[str, object]] = []
    for iso3, country in country_index.items():
        if iso3 not in un_iso3_set:
            continue
        gdp_pc_year, gdp_pc_value = gdp_pc_map.get(iso3, (target_years[0], None))
        pop_year, pop_value = pop_map.get(iso3, (target_years[0], None))
        # Choose a year to report; take the newer available among the two
        year_candidates = [y for y, v in [(gdp_pc_year, gdp_pc_value), (pop_year, pop_value)] if v is not None]
        _final_year = max(year_candidates) if year_candidates else max(target_years)

        rows_out.append(
            {
                "continent": un_iso3_to_continent.get(iso3, country.region_value),
                "country": country.name,
                "population": int(pop_value) if pop_value is not None else None,
                "gdp_per_capita": float(gdp_pc_value) if gdp_pc_value is not None else None,
            }
        )

    # Sort for determinism
    rows_out.sort(key=lambda r: (r["continent"], r["country"]))

    # Write CSV
    fieldnames = ["continent", "country", "population", "gdp_per_capita"]
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows_out:
            writer.writerow(row)


def main() -> int:
    # Prefer most recent years first. Adjust as needed.
    preferred_years = [2024, 2023, 2022, 2021, 2020]
    output_path = "country_gdp_population.csv"
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    build_dataset(output_path, preferred_years)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


