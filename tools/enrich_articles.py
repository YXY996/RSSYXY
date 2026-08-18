"""Generate cached Chinese in-site reading editions via the local LiteLLM proxy."""

from __future__ import annotations

import hashlib
import html as html_lib
import json
import os
from pathlib import Path
import re
import time
from urllib.parse import urlparse

import requests
from json_repair import repair_json

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output/html/latest/current.html"
PUBLIC_CACHE = ROOT / "site-data/enriched.json"
PRIVATE_CACHE = ROOT / "output/enriched/private.json"
LOCAL_PREVIEW = ROOT / "output/local-preview/index.html"
LITELLM_URL = os.environ.get("RSSYXY_LITELLM_URL", "http://127.0.0.1:20130")
MODEL = os.environ.get("RSSYXY_LITELLM_MODEL", "gateway-auto")
LIMIT = int(os.environ.get("RSSYXY_AI_LIMIT", "8"))


def load_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def find_local_key() -> str:
    names = ("RSSYXY_LITELLM_KEY", "LITELLM_MASTER_KEY", "LITELLM_PROXY_API_KEY", "LITELLM_API_KEY", "AI_API_KEY")
    for name in names:
        if os.environ.get(name, "").strip():
            return os.environ[name].strip()
    if os.name == "nt":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                for name in names:
                    try:
                        value, _ = winreg.QueryValueEx(key, name)
                        if str(value).strip():
                            return str(value).strip()
                    except FileNotFoundError:
                        continue
        except OSError:
            pass
    return ""


def extract_candidates(report_html: str) -> list[dict]:
    pattern = re.compile(r'<a href="(?P<url>https?://[^"]+)"[^>]*class="rss-link"[^>]*>(?P<title>.*?)</a>', re.DOTALL)
    seen, items = set(), []
    for match in pattern.finditer(report_html):
        url = html_lib.unescape(match.group("url"))
        if url in seen:
            continue
        seen.add(url)
        title = re.sub(r"<[^>]+>", "", match.group("title"))
        items.append({"url": url, "title": html_lib.unescape(title).strip(), "source": urlparse(url).netloc.removeprefix("www.")})
    return items


def fetch_readable(url: str) -> str:
    response = requests.get(f"https://r.jina.ai/{url}", headers={"Accept": "text/markdown", "X-Return-Format": "markdown"}, timeout=50)
    response.raise_for_status()
    return response.text.strip()[:24000]


def generate_chinese(item: dict, readable: str, key: str) -> dict:
    prompt = f"""你是企业高管的中文情报编辑。根据文章生成站内阅读稿。输出严格 JSON，不要代码围栏。
字段要求：zh_title 为准确自然的中文标题；summary 为 120-200 字中文摘要；key_points 为 4-6 条具体事实；reading_text 为 700-1200 字中文详细转述，覆盖背景、论点、数据、影响和限制，不逐句翻译、不虚构；why_it_matters 用 80-150 字说明对日本市场、企业 IT、制造业、数据平台、云架构或金融判断的价值。保留产品名、公司名和专有名词原文。

原始标题：{item['title']}
来源：{item['source']}
正文：
{readable}"""
    response = requests.post(
        f"{LITELLM_URL}/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": [{"role": "system", "content": "只输出合法 JSON，使用简体中文。"}, {"role": "user", "content": prompt}], "temperature": 0.2, "max_tokens": 2400},
        timeout=180,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.DOTALL)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return json.loads(repair_json(content))


def inject_cache(path: Path, articles: dict) -> None:
    if not path.exists():
        return
    report_html = path.read_text(encoding="utf-8")
    report_html = re.sub(r'<script id="wisdom-enriched-data" type="application/json">.*?</script>', "", report_html, flags=re.DOTALL)
    # Use json.dumps with ensure_ascii=False and compact separators
    # No HTML escaping needed - the browser's JSON.parse handles the content correctly
    payload = json.dumps(articles, ensure_ascii=False, separators=(",", ":"))
    block = f'<script id="wisdom-enriched-data" type="application/json">{payload}</script>'
    path.write_text(report_html.replace("</body>", f"{block}\n</body>", 1), encoding="utf-8")


def main() -> None:
    if not REPORT.exists():
        raise SystemExit("未找到本机报告，请先运行 TrendRadar。")
    key = find_local_key()
    if not key:
        raise SystemExit("LiteLLM 已在线，但未找到授权变量。请设置 RSSYXY_LITELLM_KEY。")
    public = load_json(PUBLIC_CACHE, {"updated_at": "", "articles": {}})
    private = load_json(PRIVATE_CACHE, {"articles": {}})
    articles, private_articles = public.setdefault("articles", {}), private.setdefault("articles", {})
    for url, cached in list(articles.items()):
        if not cached.get("zh_title") or len(cached.get("reading_text", "")) < 200:
            articles.pop(url, None)
            private_articles.pop(url, None)
    candidates = extract_candidates(REPORT.read_text(encoding="utf-8"))
    pending = [item for item in candidates if item["url"] not in articles][:LIMIT]
    print(f"匹配文章 {len(candidates)} 条，本次新增处理 {len(pending)} 条")
    for index, item in enumerate(pending, 1):
        try:
            print(f"[{index}/{len(pending)}] 生成中文阅读稿: {item['title'][:46]}")
            readable = fetch_readable(item["url"])
            enriched = generate_chinese(item, readable, key)
            if not enriched.get("zh_title") or len(enriched.get("reading_text", "")) < 200:
                raise ValueError("模型未返回完整中文阅读稿")
            article_id = hashlib.sha256(item["url"].encode()).hexdigest()[:16]
            articles[item["url"]] = {"article_id": article_id, "source": item["source"], "original_title": item["title"], "original_url": item["url"], "zh_title": enriched.get("zh_title", item["title"]), "summary": enriched.get("summary", ""), "key_points": enriched.get("key_points", []), "reading_text": enriched.get("reading_text", ""), "why_it_matters": enriched.get("why_it_matters", ""), "generated_by": f"local-litellm/{MODEL}"}
            private_articles[item["url"]] = {"article_id": article_id, "source_markdown": readable}
            time.sleep(1)
        except Exception as exc:
            print(f"  跳过：{type(exc).__name__}: {exc}")
    public["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    PUBLIC_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PRIVATE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_CACHE.write_text(json.dumps(public, ensure_ascii=False, indent=2), encoding="utf-8")
    PRIVATE_CACHE.write_text(json.dumps(private, ensure_ascii=False, indent=2), encoding="utf-8")
    inject_cache(REPORT, articles)
    inject_cache(LOCAL_PREVIEW, articles)
    print(f"中文阅读稿缓存：{len(articles)} 条")


if __name__ == "__main__":
    main()
