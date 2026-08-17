"""Apply the user-editable source catalog to TrendRadar's runtime config."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "config" / "sources.json"
CONFIG_PATH = ROOT / "config" / "config.yaml"
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")


def _validate(catalog: dict) -> None:
    for section in ("platforms", "rss"):
        if not isinstance(catalog.get(section), list):
            raise ValueError(f"{section} must be a list")
        seen: set[str] = set()
        for item in catalog[section]:
            source_id = str(item.get("id", ""))
            if not SAFE_ID.fullmatch(source_id) or source_id in seen:
                raise ValueError(f"invalid or duplicate {section} id: {source_id}")
            seen.add(source_id)
            if not str(item.get("name", "")).strip():
                raise ValueError(f"missing name for {source_id}")
            if section == "rss":
                parsed = urlparse(str(item.get("url", "")))
                if parsed.scheme != "https" or not parsed.hostname:
                    raise ValueError(f"RSS URL must be HTTPS: {source_id}")


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    _validate(catalog)
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))

    platforms = []
    for item in catalog["platforms"]:
        if not item.get("enabled", True):
            continue
        entry = {"id": item["id"], "name": item["name"]}
        if item.get("expected_domain"):
            entry["expected_domain"] = item["expected_domain"]
        platforms.append(entry)

    feeds = []
    for item in catalog["rss"]:
        entry = {
            "id": item["id"],
            "name": item["name"],
            "url": item["url"],
            "enabled": bool(item.get("enabled", True)),
        }
        if item.get("max_age_days") is not None:
            entry["max_age_days"] = int(item["max_age_days"])
        feeds.append(entry)

    config["platforms"]["sources"] = platforms
    config["rss"]["feeds"] = feeds
    CONFIG_PATH.write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Applied {len(platforms)} platforms and {len(feeds)} RSS feeds")


if __name__ == "__main__":
    main()
