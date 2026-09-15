#!/usr/bin/env python3
"""Build and verify core and chapter packages for mobile.

Usage:
  python3 tools/build_bundles.py [--export]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
DIST = ROOT / "dist"
ANDROID_DIST = DIST / "android"

sys.path.insert(0, str(ROOT / "tools"))
import measure_bundle


def generate_chapter_exclude_filter() -> str:
    mani = measure_bundle.load_manifest()
    col = measure_bundle.collect(mani)

    core_files = [item[1] for item in col["details"]["core"]]
    
    chap_exclude = list(measure_bundle.ALWAYS_EXCLUDE)
    chap_exclude.append("assets/audio/bgm/*.wav")
    chap_exclude.append("assets/sprites/illustrations/**")
    chap_exclude.append("assets/fonts/**")
    chap_exclude.append("assets/audio/sfx/**")
    chap_exclude.append("assets/sprites/player/**")
    chap_exclude.append("assets/sprites/npcs/**")
    chap_exclude.append("assets/sprites/ui/**")
    chap_exclude.append("assets/sprites/fx/**")
    chap_exclude.append("assets/sprites/tiles/**")
    chap_exclude.append("assets/sprites/equipment/**")
    chap_exclude.append("assets/sprites/souls/**")
    chap_exclude.append("assets/sprites/pets/**")
    chap_exclude.append("assets/sprites/props/**")
    chap_exclude.append("assets/sprites/portraits/**")
    chap_exclude.append("assets/sprites/bosses/**")
    for bgm in mani["packs"]["core"]["bgm"]:
        chap_exclude.append(f"assets/audio/bgm/{bgm}.mp3")
    for f in core_files:
        if f.startswith("assets/sprites/maps/"):
            chap_exclude.append(f)
    for rel in col["exclude_extra"]:
        if rel.startswith("assets/sprites/maps/"):
            chap_exclude.append(rel)

    return ",".join(sorted(list(set(chap_exclude))))


def update_export_presets(chap_filter: str) -> None:
    cfg = GAME / "export_presets.cfg"
    text = cfg.read_text(encoding="utf-8")
    
    # Check if Chapter Pack preset already exists
    if 'name="Chapter Pack"' in text or 'name="Android Chapter"' in text:
        # Update existing Chapter Pack preset's exclude_filter
        lines = text.splitlines(keepends=True)
        out = []
        in_chap = False
        for line in lines:
            if line.startswith("name="):
                name = line.split("=", 1)[1].strip().strip('"')
                in_chap = name in ("Chapter Pack", "Android Chapter")
            if in_chap and line.startswith("exclude_filter="):
                out.append(f'exclude_filter="{chap_filter}"\n')
                continue
            out.append(line)
        cfg.write_text("".join(out), encoding="utf-8")
        print("Updated existing Chapter Pack preset in export_presets.cfg")
    else:
        # Append as preset.5
        preset_chap = f"""
[preset.5]

name="Chapter Pack"
platform="Android"
runnable=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter="{chap_filter}"
export_path="../dist/android/chapter.pck"
encryption_include_filters=""
encryption_exclude_filters=""
encrypt_pck=false
encrypt_directory=false
script_export_mode=2

[preset.5.options]

custom_template/debug=""
custom_template/release=""
gradle_build/use_gradle_build=false
gradle_build/export_format=0
architectures/armeabi-v7a=false
architectures/arm64-v8a=true
architectures/x86=false
architectures/x86_64=false
version/code=1
version/name="0.19.0"
package/unique_name="com.kevinchu.clockworkheart"
package/name="發條之心"
package/signed=true
launcher_icons/main_192x192=""
launcher_icons/adaptive_foreground_432x432=""
launcher_icons/adaptive_background_432x432=""
screen/immersive_mode=true
screen/support_small=true
screen/support_normal=true
screen/support_large=true
screen/support_xlarge=true
user_data_backup/allow=false
permissions/custom_permissions=PackedStringArray()
"""
        cfg.write_text(text.rstrip() + "\n" + preset_chap.strip() + "\n", encoding="utf-8")
        print("Added preset.5 (Chapter Pack) to export_presets.cfg")


def run_exports() -> dict[str, int]:
    ANDROID_DIST.mkdir(parents=True, exist_ok=True)
    
    # 1. Export core PCK via Android preset
    core_pck = ANDROID_DIST / "core.pck"
    print(f"Exporting core pack: {core_pck}...")
    cmd_core = [
        "godot",
        "--headless",
        "--path",
        str(GAME),
        "--export-pack",
        "Android",
        str(core_pck),
    ]
    res_core = subprocess.run(cmd_core, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res_core.returncode != 0:
        print("Export core failed:\n", res_core.stdout, file=sys.stderr)
        sys.exit(1)
        
    # 2. Export chapter PCK via Chapter Pack preset
    chap_pck = ANDROID_DIST / "chapter.pck"
    print(f"Exporting chapter pack: {chap_pck}...")
    cmd_chap = [
        "godot",
        "--headless",
        "--path",
        str(GAME),
        "--export-pack",
        "Chapter Pack",
        str(chap_pck),
    ]
    res_chap = subprocess.run(cmd_chap, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res_chap.returncode != 0:
        print("Export chapter failed:\n", res_chap.stdout, file=sys.stderr)
        sys.exit(1)

    # 3. Export Android APK (debug)
    core_apk = ANDROID_DIST / "ClockworkHeart-debug.apk"
    print(f"Exporting debug APK: {core_apk}...")
    cmd_apk = [
        "godot",
        "--headless",
        "--path",
        str(GAME),
        "--export-debug",
        "Android",
        str(core_apk),
    ]
    res_apk = subprocess.run(cmd_apk, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res_apk.returncode != 0:
        print("Export APK failed:\n", res_apk.stdout, file=sys.stderr)
        sys.exit(1)

    sizes = {
        "core_pck": core_pck.stat().st_size,
        "chapter_pck": chap_pck.stat().st_size,
        "core_apk": core_apk.stat().st_size,
    }
    return sizes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", action="store_true", help="Perform real export of packages")
    args = ap.parse_args()

    chap_filter = generate_chapter_exclude_filter()
    update_export_presets(chap_filter)

    if args.export:
        sizes = run_exports()
        print("\n== 實機打包結果 (Artifact Sizes) ==")
        print(f"  core.pck:     {sizes['core_pck'] / (1024*1024):.2f} MB ({sizes['core_pck']} bytes)")
        print(f"  chapter.pck:  {sizes['chapter_pck'] / (1024*1024):.2f} MB ({sizes['chapter_pck']} bytes)")
        print(f"  core APK:     {sizes['core_apk'] / (1024*1024):.2f} MB ({sizes['core_apk']} bytes)")
        print("\nVerification succeeded!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
