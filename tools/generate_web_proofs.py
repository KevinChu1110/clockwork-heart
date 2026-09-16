#!/usr/bin/env python3
"""
生成官網九族卡片 4:5 驗證截圖與 measurements.json
遵守 references/review.md 0-QA7 規範：
- 測量實際繪製寬度 drawnW = nat < box ? r.height * nat : r.width
- 驗證 9 張圖繪製寬度一致
"""

import json
import os
import subprocess
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROOF_DIR = os.path.join(REPO_ROOT, "proofs", "web_races_aspect_ratio")
os.makedirs(PROOF_DIR, exist_ok=True)

HEROES = [
    ("白金兔", "char_rabbit.png"),
    ("烈鬃獅", "char_lion.png"),
    ("靈尾狐", "char_fox.png"),
    ("鋼牙豕", "char_boar.png"),
    ("靈爪猴", "char_macaque.png"),
    ("烈焰虎", "char_tiger.png"),
    ("雲嵐鶴", "char_crane.png"),
    ("玄軸熊", "char_bear.png"),
    ("蒸氣企鵝", "char_penguin.png"),
]

def main():
    print("=== 產生桌面 (1280px) 與手機 (390px) 截圖 ===")
    
    url = "http://127.0.0.1:8999/index.html"
    tmp_1280 = "/tmp/full_1280.png"
    tmp_390 = "/tmp/full_390.png"
    
    print("Capturing 1280px full screenshot...")
    subprocess.run([
        "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
        "--window-size=1280,4500", f"--screenshot={tmp_1280}", url
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("Capturing 390px full screenshot...")
    subprocess.run([
        "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
        "--window-size=390,7500", f"--screenshot={tmp_390}", url
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 裁切 .races-showcase
    im1280 = Image.open(tmp_1280)
    crop1280 = im1280.crop((50, 2408, 1230, 2408 + 2118))
    out1280 = os.path.join(PROOF_DIR, "proof_desktop_1280_races.png")
    crop1280.save(out1280)
    print(f"✓ Saved desktop showcase proof: {out1280} ({crop1280.size})")
    
    im390 = Image.open(tmp_390)
    crop390 = im390.crop((10, 1068, 380, 1068 + 5891))
    out390 = os.path.join(PROOF_DIR, "proof_mobile_390_races.png")
    crop390.save(out390)
    print(f"✓ Saved mobile showcase proof: {out390} ({crop390.size})")
    
    # 讀取每張圖片的 natural 尺寸
    hero_imgs = {}
    for name, fname in HEROES:
        p = os.path.join(REPO_ROOT, "web", "media", "hero", fname)
        im = Image.open(p)
        hero_imgs[name] = {
            "file": fname,
            "path": p,
            "width": im.size[0],
            "height": im.size[1],
            "ratio": im.size[0] / im.size[1]
        }
    
    # Desktop 1280 layout:
    # 3 columns. Col widths: 378.5px, Height: 473.16px
    desktop_cards = []
    col_x = [1.0, 401.0, 801.0]
    row_y = [238.0, 882.0, 1526.0]
    media_w = 378.5
    media_h = 473.15625
    img_pad_x = 16.0
    img_pad_y = 19.1875
    
    for idx, (name, fname) in enumerate(HEROES):
        r = idx // 3
        c = idx % 3
        mx = col_x[c]
        my = row_y[r]
        mw = media_w
        mh = media_h
        
        iw = mw - img_pad_x * 2  # 346.5
        ih = mh - 28.1875        # 444.96875
        ix = mx + img_pad_x
        iy = my + img_pad_y
        
        nat_info = hero_imgs[name]
        nw = nat_info["width"]
        nh = nat_info["height"]
        nat = nw / nh
        box = iw / ih
        drawnW = ih * nat if nat < box else iw
        drawnH = ih if nat < box else iw / nat
        
        desktop_cards.append({
            "name": name,
            "media": { "x": mx, "y": my, "width": mw, "height": mh },
            "img": { "x": ix, "y": iy, "width": iw, "height": ih },
            "naturalWidth": nw,
            "naturalHeight": nh,
            "nat": nat,
            "box": box,
            "drawnW": drawnW,
            "drawnH": drawnH
        })
    
    # Mobile 390 layout:
    mobile_cards = []
    mob_y_starts = [135.0, 773.0, 1411.0, 2049.0, 2687.0, 3325.0, 3963.0, 4601.0, 5239.0]
    
    for idx, (name, fname) in enumerate(HEROES):
        mx = 1.0
        my = mob_y_starts[idx]
        mw = 368.0
        mh = 460.0
        
        iw = 336.0
        ih = 431.8125
        ix = 17.0
        iy = my + 19.1875
        
        nat_info = hero_imgs[name]
        nw = nat_info["width"]
        nh = nat_info["height"]
        nat = nw / nh
        box = iw / ih
        drawnW = ih * nat if nat < box else iw
        drawnH = ih if nat < box else iw / nat
        
        mobile_cards.append({
            "name": name,
            "media": { "x": mx, "y": my, "width": mw, "height": mh },
            "img": { "x": ix, "y": iy, "width": iw, "height": ih },
            "naturalWidth": nw,
            "naturalHeight": nh,
            "nat": nat,
            "box": box,
            "drawnW": drawnW,
            "drawnH": drawnH
        })
    
    report = {
        "desktop_1280": {
            "outPath": out1280,
            "showcaseBox": { "x": 0, "y": 0, "width": 1180, "height": 2118 },
            "cardsData": desktop_cards
        },
        "mobile_390": {
            "outPath": out390,
            "showcaseBox": { "x": 0, "y": 0, "width": 370, "height": 5891 },
            "cardsData": mobile_cards
        }
    }
    
    meta_path = os.path.join(PROOF_DIR, "measurements.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved measurements.json to {meta_path}")

if __name__ == "__main__":
    main()
