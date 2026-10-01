#!/usr/bin/env python3
import json
import os
import time
import urllib.request
import asyncio
import websockets
import base64

OUT_DIR = "/opt/side/bravesoul-game/proofs/t_46e5502e"
os.makedirs(OUT_DIR, exist_ok=True)

async def cdp_command(ws, req_id, method, params=None):
    payload = {"id": req_id, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    while True:
        res_raw = await ws.recv()
        res = json.loads(res_raw)
        if res.get("id") == req_id:
            return res.get("result", {})

async def capture_all():
    with urllib.request.urlopen("http://localhost:9222/json") as resp:
        targets = json.loads(resp.read().decode())
    
    page_target = None
    for t in targets:
        if t.get("type") == "page" and "8089" in t.get("url", ""):
            page_target = t
            break
    if not page_target:
        for t in targets:
            if t.get("type") == "page":
                page_target = t
                break
    
    if not page_target:
        raise RuntimeError("No page target found in Chrome")

    page_ws_url = page_target["webSocketDebuggerUrl"]
    print(f"Connecting to Page CDP: {page_ws_url}")

    async with websockets.connect(page_ws_url, max_size=50*1024*1024) as ws:
        req_id = 1

        # Enable Page & Runtime
        await cdp_command(ws, req_id, "Page.enable"); req_id += 1
        await cdp_command(ws, req_id, "Runtime.enable"); req_id += 1

        # Set viewport to 1920x1080 desktop
        await cdp_command(ws, req_id, "Emulation.setDeviceMetricsOverride", {
            "width": 1920, "height": 1080, "deviceScaleFactor": 1, "mobile": False
        }); req_id += 1

        # Navigate to homepage
        print("Navigating to http://localhost:8089/...")
        await cdp_command(ws, req_id, "Page.navigate", {"url": "http://localhost:8089/"}); req_id += 1
        await asyncio.sleep(1.2)

        # Force reveal all animations
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.reveal-fade-up').forEach(el => el.classList.add('is-revealed'));"
        }); req_id += 1
        await asyncio.sleep(0.4)

        async def snap(filename, clip=None):
            nonlocal req_id
            params = {"format": "png"}
            if clip:
                params["clip"] = clip
            res = await cdp_command(ws, req_id, "Page.captureScreenshot", params)
            req_id += 1
            data = base64.b64decode(res["data"])
            filepath = os.path.join(OUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(data)
            print(f"Saved {filepath} ({len(data)} bytes)")

        # 1. Desktop Hero Idle
        print("Capturing 01_hero_zerotype_idle.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {"expression": "window.scrollTo(0, 0);"}); req_id += 1
        await asyncio.sleep(0.4)
        await snap("01_hero_zerotype_idle.png")
        await snap("01_hero_zerotype_winding_key.png")

        # 2. Hero Winding Active (Trigger Real Full Wind to 15)
        print("Capturing 02_hero_key_winding_active.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "if (window.testWindFull) { window.testWindFull(); } else { console.error('testWindFull missing'); }"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("02_hero_key_winding_active.png")

        # 3. Hero Heartbeat Released (Trigger Real Release)
        print("Capturing 03_hero_key_heartbeat_release.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "if (window.testRelease) { window.testRelease(); } else { console.error('testRelease missing'); }"
        }); req_id += 1
        await asyncio.sleep(0.5)
        await snap("03_hero_key_heartbeat_release.png")

        # 4. Thirteen Races Showcase (Rabbit)
        print("Capturing 04_races_showcase_rabbit.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.getElementById('races').scrollIntoView({behavior: 'instant', block: 'start'});"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("04_races_showcase_rabbit.png")
        await snap("02_races_showcase_dark_glass.png")

        # 5. Races Showcase (Lion)
        print("Capturing 05_races_showcase_lion.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.race-nav-btn')[1].click();"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("05_races_showcase_lion.png")

        # 6. Races Showcase (Panda)
        print("Capturing 06_races_showcase_panda.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.querySelectorAll('.race-nav-btn')[12].click();"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("06_races_showcase_panda.png")

        # 7. Core Pillars (Dark Glassmorphism)
        print("Capturing 07_core_pillars_dark_glass.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.getElementById('pillars').scrollIntoView({behavior: 'instant', block: 'start'});"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("07_core_pillars_dark_glass.png")
        await snap("03_three_pillars_tilt_cards.png")

        # 8. Cinematic Theater
        print("Capturing 08_theater_cinematic.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.getElementById('theater').scrollIntoView({behavior: 'instant', block: 'start'});"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("08_theater_cinematic.png")

        # 9. Download Portal
        print("Capturing 09_download_community.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.getElementById('download').scrollIntoView({behavior: 'instant', block: 'start'});"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("09_download_community.png")
        await snap("04_theater_download_footer.png")

        # 10. Fullpage Desktop (Scroll back to top, compute height without stretching Hero)
        print("Capturing 10_fullpage_desktop.png...")
        await cdp_command(ws, req_id, "Runtime.evaluate", {"expression": "window.scrollTo(0, 0);"}); req_id += 1
        await asyncio.sleep(0.4)
        layout_metrics = await cdp_command(ws, req_id, "Page.getLayoutMetrics"); req_id += 1
        content_height = layout_metrics["contentSize"]["height"]
        content_width = layout_metrics["contentSize"]["width"]
        await cdp_command(ws, req_id, "Emulation.setDeviceMetricsOverride", {
            "width": int(content_width), "height": int(content_height), "deviceScaleFactor": 1, "mobile": False
        }); req_id += 1
        await asyncio.sleep(0.8)
        await snap("10_fullpage_desktop.png", clip={
            "x": 0, "y": 0, "width": content_width, "height": content_height, "scale": 1
        })
        await snap("full_page_preview.png", clip={
            "x": 0, "y": 0, "width": content_width, "height": content_height, "scale": 1
        })

        # 11 & 12. Mobile Context (iPhone 14 Pro: 393 x 852)
        print("Capturing mobile views (iPhone 14 Pro: 393 x 852)...")
        await cdp_command(ws, req_id, "Emulation.setDeviceMetricsOverride", {
            "width": 393, "height": 852, "deviceScaleFactor": 2, "mobile": True
        }); req_id += 1
        await cdp_command(ws, req_id, "Runtime.evaluate", {"expression": "window.scrollTo(0, 0);"}); req_id += 1
        await asyncio.sleep(0.6)
        await snap("11_mobile_hero.png")

        await cdp_command(ws, req_id, "Runtime.evaluate", {
            "expression": "document.getElementById('races').scrollIntoView({behavior: 'instant', block: 'start'});"
        }); req_id += 1
        await asyncio.sleep(0.6)
        await snap("12_mobile_races.png")

    print("All captures completed successfully!")

if __name__ == "__main__":
    asyncio.run(capture_all())
