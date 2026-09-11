#!/usr/bin/env python3
"""量測首包／分包，並產出 Godot exclude_filter。

預設只印報告，不改檔。

  python3 tools/measure_bundle.py
  python3 tools/measure_bundle.py --write-filters   # 把 filter 寫進 stdout 區塊，供 export_presets 對照
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
MANIFEST = GAME / "data" / "bundle_manifest.json"
MAPS = GAME / "assets" / "sprites" / "maps"
BGM = GAME / "assets" / "audio" / "bgm"
FONTS = GAME / "assets" / "fonts"
WEB = ROOT / "web"

ALWAYS_EXCLUDE = [
    "scripts/**/test_*.gd",
    "scripts/**/test_*.gd.uid",
    "scripts/**/test_*.json",
    "assets/sprites/_gen*/**",
    "assets/sprites/**/_backup*/**",
    "assets/sprites/**/_backup_*/**",
]


def mb(n: int) -> float:
    return round(n / (1024 * 1024), 2)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def stem_pack(stem: str, mani: dict) -> str:
    core = mani["packs"]["core"]
    chap = mani["packs"]["chapter"]
    for p in core.get("map_prefixes", []):
        if stem == p or stem.startswith(p + "_"):
            return "core"
    if stem in core.get("map_extra", []):
        return "core"
    for p in chap.get("map_prefixes", []):
        if stem == p or stem.startswith(p + "_"):
            return "chapter"
    if stem in chap.get("map_extra", []):
        return "chapter"
    return str(mani.get("default_pack", "chapter"))


def iter_files(d: Path, extra_suffixes: tuple[str, ...] = ()) -> list[Path]:
    if not d.is_dir():
        return []
    out = []
    for p in d.rglob("*"):
        if not p.is_file():
            continue
        if p.name.endswith(".import") or p.name == ".gdignore":
            continue
        out.append(p)
    return out


def file_size(p: Path) -> int:
    try:
        return p.stat().st_size
    except OSError:
        return 0


def map_art_stem(path: Path) -> str | None:
    name = path.name
    for suf in ("_bg.webp", "_bg.png", "_banner.png", "_banner.webp"):
        if name.endswith(suf):
            return name[: -len(suf)]
    if name.startswith("sky_kingdom"):
        return "sky_kingdom"
    return None


def collect(mani: dict) -> dict:
    buckets = {
        "core": 0,
        "chapter": 0,
        "extra": 0,
        "unclassified": 0,
    }
    details: dict[str, list[tuple[int, str]]] = {k: [] for k in buckets}
    exclude_extra: list[str] = []
    exclude_chapter: list[str] = []

    # maps
    png_with_webp: list[Path] = []
    if MAPS.is_dir():
        for p in sorted(MAPS.iterdir()):
            if not p.is_file() or p.name.endswith(".import"):
                continue
            sz = file_size(p)
            rel = str(p.relative_to(GAME)).replace("\\", "/")
            if p.suffix.lower() == ".png" and p.with_suffix(".webp").exists():
                png_with_webp.append(p)
                buckets["extra"] += sz
                details["extra"].append((sz, rel))
                exclude_extra.append(rel)
                continue
            stem = map_art_stem(p)
            if stem is None:
                # walkmasks etc — keep in core (needed to walk C0)
                buckets["core"] += sz
                details["core"].append((sz, rel))
                continue
            pack = stem_pack(stem, mani)
            buckets[pack] += sz
            details[pack].append((sz, rel))
            if pack == "chapter":
                exclude_chapter.append(rel)

    # bgm
    core_bgm = set(mani["packs"]["core"]["bgm"])
    chap_bgm = set(mani["packs"]["chapter"]["bgm"])
    if BGM.is_dir():
        for p in sorted(BGM.iterdir()):
            if not p.is_file() or p.suffix.lower() in {".import", ".json", ".md"}:
                continue
            sz = file_size(p)
            rel = str(p.relative_to(GAME)).replace("\\", "/")
            stem = p.stem
            if p.suffix.lower() == ".wav":
                buckets["extra"] += sz
                details["extra"].append((sz, rel))
                exclude_extra.append(rel)
                continue
            if stem in core_bgm:
                buckets["core"] += sz
                details["core"].append((sz, rel))
            elif stem in chap_bgm:
                buckets["chapter"] += sz
                details["chapter"].append((sz, rel))
                exclude_chapter.append(rel)
            else:
                buckets["unclassified"] += sz
                details["unclassified"].append((sz, rel))

    # fonts
    core_fonts = set(mani["packs"]["core"]["fonts"])
    extra_fonts = set(mani["packs"]["extra"]["fonts"])
    if FONTS.is_dir():
        for p in sorted(FONTS.iterdir()):
            if not p.is_file() or p.suffix.lower() in {".import", ".txt", ".md"}:
                continue
            sz = file_size(p)
            rel = str(p.relative_to(GAME)).replace("\\", "/")
            if p.name in core_fonts:
                buckets["core"] += sz
                details["core"].append((sz, rel))
            elif p.name in extra_fonts:
                buckets["extra"] += sz
                details["extra"].append((sz, rel))
                exclude_extra.append(rel)
            else:
                buckets["unclassified"] += sz
                details["unclassified"].append((sz, rel))

    # illustrations
    ill = GAME / "assets" / "sprites" / "illustrations"
    title_keep = {Path(x).name for x in mani["packs"]["core"].get("title_art", [])}
    if ill.is_dir():
        for p in sorted(ill.iterdir()):
            if not p.is_file() or p.name.endswith(".import"):
                continue
            sz = file_size(p)
            rel = str(p.relative_to(GAME)).replace("\\", "/")
            if p.name in title_keep:
                buckets["core"] += sz
                details["core"].append((sz, rel))
            else:
                buckets["extra"] += sz
                details["extra"].append((sz, rel))
                exclude_extra.append(rel)

    # keep_dirs (core character/ui)
    for drel in mani["packs"]["core"].get("keep_dirs", []):
        d = GAME / drel
        if not d.is_dir():
            continue
        for p in iter_files(d):
            sz = file_size(p)
            rel = str(p.relative_to(GAME)).replace("\\", "/")
            buckets["core"] += sz
            details["core"].append((sz, rel))

    return {
        "buckets": buckets,
        "details": details,
        "exclude_extra": exclude_extra,
        "exclude_chapter": exclude_chapter,
        "png_with_webp": [str(p.name) for p in png_with_webp],
    }


def godot_filter(extra: list[str], chapter: list[str], *, with_chapter: bool, drop_noto: bool) -> str:
    parts = list(ALWAYS_EXCLUDE)
    # compact globs where possible
    parts.append("assets/audio/bgm/*.wav")
    parts.append("assets/sprites/illustrations/duel_*.png")
    if drop_noto:
        parts.append("assets/fonts/NotoSans*.otf")
    # duplicate pngs listed explicitly (Godot exclude has no "if webp exists")
    for rel in extra:
        if rel.endswith(".png") and "/maps/" in rel:
            parts.append(rel)
        elif rel.endswith(".wav") or "NotoSans" in rel or "/illustrations/" in rel:
            continue  # covered by glob
        else:
            parts.append(rel)
    if with_chapter:
        for rel in chapter:
            parts.append(rel)
    # unique preserve order
    seen = set()
    out = []
    for p in parts:
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return ",".join(out)


def web_report() -> tuple[int, list[tuple[int, str]]]:
    if not WEB.is_dir():
        return 0, []
    total = 0
    top: list[tuple[int, str]] = []
    for p in WEB.rglob("*"):
        if p.is_file():
            sz = file_size(p)
            total += sz
            top.append((sz, str(p.relative_to(WEB))))
    top.sort(reverse=True)
    return total, top[:15]


def print_report(col: dict, mani: dict) -> None:
    print("== 勇者之魂 分包量測 ==")
    print("manifest:", MANIFEST.relative_to(ROOT))
    print("first_path:", mani.get("first_path"))
    print("target_mb:", mani.get("target_mb"))
    print()
    web_total, web_top = web_report()
    print("web/ 目錄（行銷站，不是遊戲 export）：%.2f MB" % mb(web_total))
    media = WEB / "media"
    if media.is_dir():
        msz = sum(file_size(p) for p in media.rglob("*") if p.is_file())
        print("  其中 web/media：%.2f MB" % mb(msz))
    print("  最大檔：")
    for sz, rel in web_top[:8]:
        print("   %6.2f MB  %s" % (mb(sz), rel))
    print()
    print("遊戲資產（源檔，進包前）：")
    for k in ("core", "chapter", "extra", "unclassified"):
        print("  %-14s %7.2f MB  (%d files)" % (k, mb(col["buckets"][k]), len(col["details"][k])))
    print()
    print("core 最大 12 項：")
    for sz, rel in sorted(col["details"]["core"], reverse=True)[:12]:
        print("   %6.2f MB  %s" % (mb(sz), rel))
    print("chapter 最大 8 項：")
    for sz, rel in sorted(col["details"]["chapter"], reverse=True)[:8]:
        print("   %6.2f MB  %s" % (mb(sz), rel))
    print("extra 最大 8 項：")
    for sz, rel in sorted(col["details"]["extra"], reverse=True)[:8]:
        print("   %6.2f MB  %s" % (mb(sz), rel))
    print()
    print("與 webp 重複、可移出首包的 png：", len(col["png_with_webp"]))
    core_src = col["buckets"]["core"]
    print()
    print("估計：")
    print("  首包源資產 core = %.2f MB" % mb(core_src))
    print("  Godot 引擎約 25–40 MB（Android arm64 / Linux 視模板）")
    print("  首包估計區間 = %.0f–%.0f MB（源資產 + 引擎；貼圖 import 還會再壓）" % (
        mb(core_src) + 25, mb(core_src) + 40
    ))
    print("  目標 50–80 MB。差額見 docs/BUNDLE.md。")


def apply_presets(extra_f: str, core_f: str) -> None:
    """Mac + mobile first-download use CORE; Win/Linux stay full (extra-only junk strip)."""
    cfg = GAME / "export_presets.cfg"
    text = cfg.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    name = ""
    out: list[str] = []
    # Product Lock §5.2 mobile-first: Mac store + Android/iOS share CORE exclude.
    core_presets = {"macOS", "Android", "iOS"}
    for line in lines:
        if line.startswith("name="):
            name = line.split("=", 1)[1].strip().strip('"')
        if line.startswith("exclude_filter="):
            filt = core_f if name in core_presets else extra_f
            out.append('exclude_filter="%s"\n' % filt)
            continue
        out.append(line)
    cfg.write_text("".join(out), encoding="utf-8")
    print("updated", cfg.relative_to(ROOT), "macOS/Android/iOS=core, Win/Linux=extra-only")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-filters", action="store_true")
    ap.add_argument("--apply-presets", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not MANIFEST.exists():
        print("FATAL: missing", MANIFEST, file=sys.stderr)
        return 2
    mani = load_manifest()
    col = collect(mani)
    if args.json:
        payload = {
            "buckets_mb": {k: mb(v) for k, v in col["buckets"].items()},
            "buckets_bytes": col["buckets"],
            "file_counts": {k: len(v) for k, v in col["details"].items()},
            "png_with_webp": col["png_with_webp"],
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    print_report(col, mani)
    extra_f = godot_filter(col["exclude_extra"], col["exclude_chapter"], with_chapter=False, drop_noto=False)
    core_f = godot_filter(col["exclude_extra"], col["exclude_chapter"], with_chapter=True, drop_noto=True)
    print()
    print("== exclude_filter extra-only（桌面完整包，只丟永不進包的重複檔）==")
    print(extra_f)
    print()
    print("== exclude_filter core（macOS／Android／iOS 首包，再排除 chapter／Pack-A BGM）==")
    print(core_f)
    if args.write_filters:
        out = ROOT / "docs" / "bundle_filters.txt"
        out.write_text(
            "EXTRA_ONLY\n" + extra_f + "\n\nCORE\n" + core_f + "\n",
            encoding="utf-8",
        )
        print("wrote", out)
    if args.apply_presets:
        apply_presets(extra_f, core_f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
