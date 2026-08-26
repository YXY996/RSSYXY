#!/usr/bin/env python3
"""
XHS Login Helper v2
- Opens browser, waits indefinitely for user to QR-scan login
- Polls publish-page selector every 5s, prints progress
- Never raises on timeout; keeps browser open until login detected
"""
import sys, asyncio, time
from pathlib import Path
from playwright.async_api import async_playwright

USER_DATA_DIR = "output/xhs_profile_v2"
TOTAL_WAIT = 3600  # 1 hour max

def log(msg):
    print(msg, flush=True)

async def main():
    log("=== XHS Login Helper v2 ===")
    log("user_data_dir: " + USER_DATA_DIR)
    log("Browser will open. Scan QR with XHS app to login.")
    log("After login, this script keeps running. Ctrl+C to exit.")
    Path(USER_DATA_DIR).mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 800},
            locale="zh-CN",
        )
        page = context.pages[0] if context.pages else await context.new_page()

        try:
            log("Opening XHS creator center...")
            await page.goto("https://creator.xiaohongshu.com/publish/publish",
                            wait_until="networkidle", timeout=60000)

            deadline = time.monotonic() + TOTAL_WAIT
            checked = 0
            while time.monotonic() < deadline:
                url = page.url
                try:
                    await page.wait_for_selector(
                        ".publish-container, .creator-main, [data-testid='publish-page']",
                        timeout=5000)
                    log("LOGIN OK - publish page reached")
                    log("Session saved to " + USER_DATA_DIR)
                    log("Now safe to close browser (Ctrl+C). TrendRadar will reuse session.")
                    # keep alive until user Ctrl+C
                    await asyncio.Event().wait()
                    return
                except Exception:
                    if "login" in url:
                        if checked % 6 == 0:
                            log("Still on login page. Scanning required...")
                        checked += 1
                    else:
                        log("Current URL: " + url)
                        checked += 1
                    await asyncio.sleep(5)

            log("Timeout after 1 hour - no login detected. Exiting.")
        except asyncio.CancelledError:
            log("\nCancelled.")
        except KeyboardInterrupt:
            log("\nUser exit.")
        finally:
            await context.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
