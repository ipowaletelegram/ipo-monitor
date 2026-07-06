from bs4 import BeautifulSoup
import re


def clean(value):
    if value is None:
        return ""

    return " ".join(value.split()).strip()


def extract_gmp(text):
    """
    Example:
    ₹28 (13.08%)
    """

    match = re.search(r"₹\s*([\d\.]+)\s*\((.*?)\)", text)

    if match:

        return {
            "gmp": match.group(1),
            "gain": match.group(2)
        }

    return {
        "gmp": "",
        "gain": ""
    }


def parse_investorgain(html):

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", id="reportTable")

    if table is None:
        raise Exception("reportTable not found")

    rows = table.select("tbody tr")
    print("Rows Found :", len(rows))

    ipos = []

    for row in rows:

        cols = row.find_all("td")

        if len(cols) < 12:
            continue

        company = clean(cols[0].find("a").get_text())

gmp_text = clean(cols[1].get_text(" ", strip=True))

gmp_data = extract_gmp(gmp_text)

issue_price = clean(cols[4].get_text())

lot = clean(cols[6].get_text())

open_date = clean(cols[7].get_text())

close_date = clean(cols[8].get_text())

listing = clean(cols[10].get_text())

updated = clean(cols[11].get_text())

        ipos.append({

            "company": company,

            "gmp": gmp_data["gmp"],

            "gain": gmp_data["gain"],

            "issue_price": issue_price,

            "lot": lot,

            "open": open_date,

            "close": close_date,

            "listing": listing,

            "updated": updated

        })

    return ipos
