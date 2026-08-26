#!/usr/bin/env python3
"""R2 二批補圖：靈寵幼體×4（去背）、龍窟頭圖×1（保留背景）、鏢箱×4（去背）。

風格鎖 chibi／既有 palette（CLAUDE.md 契約 4）；產圖走 asset-gen（付費，已獲同意）。
輸出：
  game/assets/sprites/pets/pet_<species>.png       96x112 透明
  game/assets/sprites/maps/dragon_cave_banner.png  640x360
  game/assets/sprites/props/escort_box_<id>.png    64x64 透明
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_GEN = ROOT / ".agents/skills/asset-gen/tools/asset_gen.py"
PY = ROOT / ".venv-asset/bin/python"
GEN = ROOT / "game/assets/sprites/_gen_r2"
PETS = ROOT / "game/assets/sprites/pets"
MAPS = ROOT / "game/assets/sprites/maps"
PROPS = ROOT / "game/assets/sprites/props"

STYLE = "cute chibi pixel art game sprite, warm muted palette, solid dark gray background, no text, single centered subject, game-ready"

PET_JOBS = [
    ("ember_rat", "tiny baby rat covered in soft ash-gray fur with small ember-orange glowing eyes and a curled tail, " + STYLE),
    ("grey_pup", "tiny fluffy grey wolf puppy with oversized paws and bright eyes, sitting, " + STYLE),
    ("wind_chick", "tiny falcon chick with fluffy wind-blown feathers and stubby wings, " + STYLE),
    ("stone_piglet", "tiny boar piglet with faint stone-pattern markings on its back, " + STYLE),
]

BOX_JOBS = [
    ("wood", "small plain wooden cargo box with rope binding, " + STYLE),
    ("bronze", "small bronze-banded cargo chest with rivets, " + STYLE),
    ("silver", "small silver-trimmed cargo chest with a gleam, " + STYLE),
    ("goldbox", "ornate violet-and-gold treasure chest glowing faintly, " + STYLE),
]

BANNER = (
    "dragon_cave_banner",
    "painterly fantasy game location art, mysterious dragon grotto cave entrance with faint "
    "amber light inside, mossy stone dragon carvings, warm muted palette matching a cozy "
    "chibi RPG, wide landscape composition, no text, no characters",
)


def _matte(im):
    """砍掉深灰背景（沿用 smart_matte_props 的判定）。"""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 10:
                continue
            mx = max(abs(r - g), abs(g - b), abs(r - b))
            bright = (r + g + b) / 3.0
            if bright < 32 or (18 <= r <= 88 and 18 <= g <= 88 and 18 <= b <= 88 and mx <= 16):
                px[x, y] = (0, 0, 0, 0)
    return im


def _gen(prompt: str, out: Path, aspect: str = "1:1") -> bool:
    if out.exists() and out.stat().st_size > 20000:
        print("  skip(gen cached)", flush=True)
        return True
    cmd = [
        str(PY if PY.exists() else sys.executable), str(ASSET_GEN), "image",
        "--model", "gemini", "--size", "1K", "--aspect-ratio", aspect,
        "--prompt", prompt, "-o", str(out),
    ]
    for attempt in range(1, 4):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode == 0 and out.exists():
            return True
        if "503" in (r.stderr or ""):
            time.sleep(6 * attempt)
    print("  FAIL", (r.stderr or "")[-200:], flush=True)
    return False


def main() -> int:
    if not os.environ.get("GOOGLE_API_KEY"):
        print("no GOOGLE_API_KEY", file=sys.stderr)
        return 2
    from PIL import Image

    for d in (GEN, PETS, MAPS, PROPS):
        d.mkdir(parents=True, exist_ok=True)
    (GEN / ".gdignore").write_text("# gen sources — not loaded by game\n")

    ok = fail = cost = 0

    for name, prompt in PET_JOBS:
        print(f"==> pet {name}", flush=True)
        raw = GEN / f"pet_{name}.png"
        if not _gen(prompt, raw):
            fail += 1
            continue
        cost += 7
        im = _matte(Image.open(raw))
        im = im.crop(im.getbbox() or (0, 0, im.width, im.height))
        im.thumbnail((88, 104), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (96, 112), (0, 0, 0, 0))
        canvas.paste(im, ((96 - im.width) // 2, (112 - im.height) // 2), im)
        canvas.save(PETS / f"pet_{name}.png")
        ok += 1

    for name, prompt in BOX_JOBS:
        print(f"==> box {name}", flush=True)
        raw = GEN / f"box_{name}.png"
        if not _gen(prompt, raw):
            fail += 1
            continue
        cost += 7
        im = _matte(Image.open(raw))
        im = im.crop(im.getbbox() or (0, 0, im.width, im.height))
        im.thumbnail((60, 60), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        canvas.paste(im, ((64 - im.width) // 2, (64 - im.height) // 2), im)
        canvas.save(PROPS / f"escort_box_{name}.png")
        ok += 1

    print("==> banner", flush=True)
    raw = GEN / "dragon_cave_banner.png"
    if _gen(BANNER[1], raw, aspect="16:9"):
        cost += 7
        im = Image.open(raw).convert("RGB")
        im.thumbnail((640, 360), Image.Resampling.LANCZOS)
        im.save(MAPS / "dragon_cave_banner.png", optimize=True)
        ok += 1
    else:
        fail += 1

    print(json.dumps({"ok": ok, "fail": fail, "cost_cents_est": cost}))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
