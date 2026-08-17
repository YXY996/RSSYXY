"""Build a local-only UI preview from the latest public report."""

from pathlib import Path
import re
import runpy
from urllib.request import Request, urlopen

personal_module = runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "trendradar/report/personal_dashboard.py")
)
personalize_html = personal_module["personalize_html"]


PUBLIC_REPORT = "https://yxy996.github.io/RSSYXY/"
LOCAL_REPORT = Path("output/html/latest/current.html")
OUTPUT = Path("output/local-preview/index.html")


if LOCAL_REPORT.exists():
    html = LOCAL_REPORT.read_text(encoding="utf-8")
    print(f"使用本机抓取结果: {LOCAL_REPORT}")
else:
    request = Request(PUBLIC_REPORT, headers={"User-Agent": "RSSYXY local preview"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    print(f"本机尚无报告，使用线上快照: {PUBLIC_REPORT}")

html = re.sub(
    r'<style id="wisdom-signal-theme">.*?</style>', "", html, flags=re.DOTALL
)
html = re.sub(
    r'<script id="wisdom-signal-script">.*?</script>', "", html, flags=re.DOTALL
)
html = personalize_html(html)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(html, encoding="utf-8")
print(OUTPUT.resolve())
