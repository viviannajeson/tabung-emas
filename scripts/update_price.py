"""Read the GAP 1 gram price from publicgold.com.my and write it to price.json.

The app reads price.json to show the adviser's price. The file is only rewritten when
the price or its date changes, so the commit history stays readable.

    python3 scripts/update_price.py
"""
import datetime
import json
import pathlib
import re
import sys
import urllib.request

URL = "https://publicgold.com.my/"
OUT = pathlib.Path(__file__).resolve().parent.parent / "price.json"
MYT = datetime.timezone(datetime.timedelta(hours=8))


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Tabung Emas price check)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(html):
    start = html.find("GOLD ACCUMULATION PROGRAM")
    if start < 0:
        raise ValueError("GAP section not found on the page")
    m = re.search(r"RM\s*([\d,]+(?:\.\d+)?)\s*=\s*1\.0+\s*gram", html[start:start + 6000])
    if not m:
        raise ValueError("GAP 1 gram price not found in the GAP section")
    price = float(m.group(1).replace(",", ""))
    if not 100 <= price <= 5000:
        raise ValueError(f"GAP price looks wrong: {price}")

    # The page carries several "Last Update" stamps (some hidden and old); use the newest.
    stamps = []
    for d, t in re.findall(r"Last Update (\d{1,2}-[A-Za-z]+-\d{4}) (\d{2}:\d{2})", html):
        for fmt in ("%d-%b-%Y %H:%M", "%d-%B-%Y %H:%M"):
            try:
                stamps.append(datetime.datetime.strptime(f"{d} {t}", fmt))
                break
            except ValueError:
                pass
    when = max(stamps) if stamps else datetime.datetime.now(MYT).replace(tzinfo=None)
    return {
        "price": int(price) if price.is_integer() else price,
        "date": when.strftime("%Y-%m-%d"),
        "time": when.strftime("%H:%M"),
        "source": URL,
    }


def main():
    new = parse(fetch(URL))
    try:
        old = json.loads(OUT.read_text())
    except (OSError, ValueError):
        old = {}
    if old.get("price") == new["price"] and old.get("date") == new["date"]:
        print(f"No change: RM {new['price']} on {new['date']}")
        return
    OUT.write_text(json.dumps(new, indent=2) + "\n")
    print(f"Updated: RM {new['price']} on {new['date']} {new['time']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # report clearly in the Actions log and fail the run
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
