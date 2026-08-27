#!/usr/bin/env python3
"""環境層像素歸一（降 AI 感 · 2026-08-27 Kevin 拍板）。

問題：底圖／戰鬥背景／橫幅是每張獨立生成的 AI 插畫（town_bg 有 77,001 色），
和統一像素 chibi 的角色層疊在一起就是「AI 拼貼」。

解法：角色是風格北辰——從角色抽主色盤（加地磚與冷色地圖樣本補綠藍，上限 96 色），
所有環境圖降到像素格（block=5）再量化到這套色盤。零 API 費、可逆。

範圍：maps/*.webp、maps/battle_*.png、maps/*_banner.png、dragon_cave_banner、
      pets/、props/escort_box_*（僅量化不降格）。
不動：角色、NPC、tiles、UI。原圖備份到 maps/_backup_prepixel_0827/。

用法：python3 tools/pixelize_env.py [--block 5] [--colors 96]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "game/assets/sprites/maps"
PETS = ROOT / "game/assets/sprites/pets"
PROPS = ROOT / "game/assets/sprites/props"
BACKUP = MAPS / "_backup_prepixel_0827"

## 色盤來源：角色（暖）＋地磚與冷色地圖（綠藍，取樣避免暖色壓過）
CHAR_SOURCES = [
    "game/assets/sprites/player/rabbit_battle.png",
    "game/assets/sprites/npcs/ding.png",
    "game/assets/sprites/npcs/acha.png",
    "game/assets/sprites/npcs/amber.png",
]
COOL_SOURCES = [
    "game/assets/sprites/maps/forest_bg.webp",
    "game/assets/sprites/maps/coast_bg.webp",
    "game/assets/sprites/maps/mist_village_bg.webp",
    "game/assets/sprites/tiles/grass_atlas.png",
    "game/assets/sprites/tiles/dark_atlas.png",
]


def build_palette(colors: int) -> Image.Image:
    pixels: list[tuple[int, int, int]] = []
    for s in CHAR_SOURCES:
        p = ROOT / s
        if not p.exists():
            continue
        im = Image.open(p).convert("RGBA")
        for px in list(im.getdata()):
            if px[3] > 200:
                pixels.append(px[:3])
    for s in COOL_SOURCES:
        p = ROOT / s
        if not p.exists():
            continue
        im = Image.open(p).convert("RGB")
        im.thumbnail((160, 160), Image.LANCZOS)
        pixels.extend(list(im.getdata()))
    strip = Image.new("RGB", (len(pixels), 1))
    strip.putdata(pixels)
    return strip.quantize(colors=colors, method=Image.MEDIANCUT)


def pixelize(im: Image.Image, pal: Image.Image, block: int) -> Image.Image:
    w, h = im.size
    small = im.convert("RGB").resize((max(1, w // block), max(1, h // block)), Image.LANCZOS)
    q = small.quantize(palette=pal, dither=Image.Dither.NONE)
    return q.convert("RGB").resize((w, h), Image.NEAREST)


def quantize_only(im: Image.Image, pal: Image.Image) -> Image.Image:
    """小圖（寵物／鏢箱）：已是像素密度，僅統一色盤，保留透明。"""
    rgba = im.convert("RGBA")
    alpha = rgba.getchannel("A")
    q = rgba.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE).convert("RGB")
    out = q.convert("RGBA")
    out.putalpha(alpha)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", type=int, default=5)
    ap.add_argument("--colors", type=int, default=96)
    args = ap.parse_args()

    pal = build_palette(args.colors)
    BACKUP.mkdir(exist_ok=True)
    (BACKUP / ".gdignore").write_text("# pre-pixelize originals — not loaded by game\n")

    targets: list[Path] = []
    targets += sorted(MAPS.glob("*.webp"))
    targets += sorted(MAPS.glob("battle_*.png"))
    targets += sorted(MAPS.glob("*_banner.png"))
    dc = MAPS / "dragon_cave_banner.png"
    if dc.exists() and dc not in targets:
        targets.append(dc)

    done = 0
    for t in targets:
        bak = BACKUP / t.name
        if not bak.exists():
            shutil.copy2(t, bak)
        im = Image.open(bak)  ## 以備份為源：重跑不會疊代劣化
        out = pixelize(im, pal, args.block)
        if t.suffix == ".webp":
            out.save(t, quality=90, method=6)
        else:
            out.save(t, optimize=True)
        done += 1
        print(f"  ok {t.name}", flush=True)

    small = sorted(PETS.glob("pet_*.png")) + sorted(PROPS.glob("escort_box_*.png"))
    for t in small:
        bak = BACKUP / t.name
        if not bak.exists():
            shutil.copy2(t, bak)
        out = quantize_only(Image.open(bak), pal)
        out.save(t, optimize=True)
        done += 1
        print(f"  ok(quant) {t.name}", flush=True)

    print(f"done {done} files · block={args.block} · colors={args.colors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
