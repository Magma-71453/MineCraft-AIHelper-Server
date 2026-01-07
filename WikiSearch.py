#!/usr/bin/env python3
import sys
import requests
import json

if len(sys.argv) < 2:
    print("missing")
    sys.exit(0)

title = sys.argv[1]

API = "https://minecraft.wiki/api.php"
params = {
    "action": "query",
    "prop": "extracts",
    "explaintext": 1,
    "exintro": 0,
    "format": "json",
    "titles": title
}

try:
    r = requests.get(API, params=params, timeout=5)
    data = r.json()

    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))

    extract = page.get("extract", "").strip()
    if not extract:
        print("missing")
    else:
        print(extract.replace("\n", " "))

except Exception:
    print("missing")
