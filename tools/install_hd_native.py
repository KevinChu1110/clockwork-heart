#!/usr/bin/env python3
"""把已有的 4K 底圖原檔裝成「原生像素 ≥ 該 art 的世界尺寸」的 16:9 webp。

regen_maps_hd.py 以前一律縮到 2633×1469，但 road／town／village 等世界比這還大，
螢幕上仍是小圖硬拉。這支不呼叫付費 API，只吃 maps/_gen_hd_maps/ 的 4K PNG。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pixelize_env import build_palette, pixelize  # noqa: E402

HD = ROOT / "game/assets/sprites/maps/_gen_hd_maps"
NOSKY = ROOT / "game/assets/sprites/_gen_r2/maps_nosky"
MAPS = ROOT / "game/assets/sprites/maps"
BACKUP = MAPS / "_backup_prepixel_0827"
CATALOG = ROOT / "game/scripts/world/map_catalog.gd"
ASPECT = 16 / 9
## 舊 4K 仍帶天空時，先丟掉頂部這一段再裝。nosky 原檔為 0。
CROP_TOP = {
	"village": 0.20,
	"road": 0.26,
	"wild": 0.20,
	"dojo_inner": 0.28,
	"coast_wreck": 0.30,
}


def catalog_worlds() -> dict[str, tuple[float, float]]:
    """art → max (w, h) among maps using that art."""
    src = CATALOG.read_text(encoding="utf-8")
    arts: dict[str, tuple[float, float]] = {}
    for m in re.finditer(r"static func (_[a-z0-9_]+)\(\) -> Dictionary:", src):
        nxt = src.find("static func ", m.end())
        blk = src[m.end(): nxt if nxt > 0 else len(src)]
        b = re.search(
            r'_base\(\s*"[^"]+",\s*Color\([^)]*\),\s*([\d.]+),\s*([\d.]+),\s*'
            r'Vector2\([^)]+\),\s*"([a-z0-9_]+)"\)',
            blk,
        )
        if not b:
            continue
        w, h, art = float(b.group(1)), float(b.group(2)), b.group(3)
        if art not in arts:
            arts[art] = (w, h)
        else:
            arts[art] = (max(arts[art][0], w), max(arts[art][1], h))
    return arts


def cover_16x9(need_w: float, need_h: float) -> tuple[int, int]:
    tw = max(int(round(need_w)), int(round(need_h * ASPECT)))
    th = int(round(tw * 9 / 16))
    if th < need_h:
        th = int(round(need_h))
        tw = int(round(th * ASPECT))
    return tw, th


def current_tex(art: str) -> Path | None:
    for ext in (".webp", ".png"):
        p = MAPS / f"{art}_bg{ext}"
        if p.exists():
            return p
    return None


def main() -> int:
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    worlds = catalog_worlds()
    pal = build_palette(96)
    BACKUP.mkdir(exist_ok=True)
    done = skip = miss = 0
    for art, (nw, nh) in sorted(worlds.items()):
        if only and art not in only:
            continue
        nosky = NOSKY / f"{art}.png"
        hd = HD / f"{art}_bg.png"
        src = nosky if nosky.exists() else hd
        cur = current_tex(art)
        tw, th = cover_16x9(nw, nh)
        if not src.exists():
            print(f"  miss {art:20s} need {tw}x{th} (no 4K)")
            miss += 1
            continue
        force = "--force" in sys.argv or src == nosky
        if cur is not None and not force:
            cw, ch = Image.open(cur).size
            if cw >= nw and ch >= nh and abs(cw / ch - ASPECT) / ASPECT <= 0.05:
                print(f"  skip {art:20s} {cw}x{ch} already ≥ {nw:.0f}x{nh:.0f}")
                skip += 1
                continue
        print(f"  inst {art:20s} {nw:.0f}x{nh:.0f} → {tw}x{th} src={src.name}", flush=True)
        im = Image.open(src).convert("RGB")
        crop_f = 0.0 if src == nosky else float(CROP_TOP.get(art, 0.0))
        if crop_f > 0.01:
            y0 = int(im.height * crop_f)
            im = im.crop((0, y0, im.width, im.height))
        im = im.resize((tw, th), Image.Resampling.LANCZOS)
        pre = BACKUP / f"{art}_bg.webp"
        im.save(pre, "WEBP", quality=95, method=6)
        out = pixelize(im, pal, 5)
        dest = MAPS / f"{art}_bg.webp"
        out.save(dest, "WEBP", quality=90, method=6)
        done += 1
    print(f"done={done} skip={skip} miss={miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
