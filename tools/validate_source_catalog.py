"""Validate RSS/Atom candidates and print a compact Chinese report."""

import json
from pathlib import Path
from urllib.request import Request, urlopen


catalog = json.loads(Path("config/source_catalog.json").read_text(encoding="utf-8"))
for source in catalog["sources"]:
    request = Request(
        source["url"],
        headers={"User-Agent": "RSSYXY/1.0 source validation (personal reader)"},
    )
    try:
        with urlopen(request, timeout=20) as response:
            sample = response.read(4096).lower()
            is_feed = any(marker in sample for marker in (b"<rss", b"<feed", b"<rdf:rdf"))
            state = "通过" if is_feed else "响应但未识别为 Feed"
            print(f"{state}\t{response.status}\t{source['id']}\t{source['url']}")
    except Exception as exc:
        print(f"失败\t-\t{source['id']}\t{type(exc).__name__}: {exc}")
