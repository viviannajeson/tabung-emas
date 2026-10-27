"""Read the GAP 1 gram price from publicgold.com.my and write price.json and prices.json.

price.json holds the latest price. prices.json is the price history the app shows in the
Harga tab: a new entry is added whenever the price changes, and at least one per day.
Files are only rewritten when something changes, so the commit history stays readable.

    python3 scripts/update_price.py
"""
import datetime
import json
import pathlib
import re
import sys
import urllib.request

URL = "https://publicgold.com.my/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "price.json"
HISTORY = ROOT / "prices.json"
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


def load(path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default


def main():
    new = parse(fetch(URL))

    old = load(OUT, {})
    if old.get("price") == new["price"] and old.get("date") == new["date"]:
        print(f"Latest unchanged: RM {new['price']} on {new['date']}")
    else:
        OUT.write_text(json.dumps(new, indent=2) + "\n")
        print(f"Latest updated: RM {new['price']} on {new['date']} {new['time']}")

    hist = load(HISTORY, {"source": URL, "prices": []})
    rows = hist.setdefault("prices", [])
    last = rows[-1] if rows else None
    if last and last["price"] == new["price"] and last["date"] == new["date"]:
        print("History unchanged")
        return
    if last and (last["date"], last["time"]) >= (new["date"], new["time"]):
        print("History already has a newer entry; not adding")
        return
    rows.append({"date": new["date"], "time": new["time"], "price": new["price"]})
    hist["source"] = URL
    # one entry per line keeps the file readable and the diffs small
    body = ",\n".join("    " + json.dumps(r) for r in rows)
    HISTORY.write_text('{\n  "source": %s,\n  "prices": [\n%s\n  ]\n}\n' % (json.dumps(URL), body))
    print(f"History: added RM {new['price']} on {new['date']} {new['time']} ({len(rows)} entries)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # report clearly in the Actions log and fail the run
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
