#!/usr/bin/env python3
"""
tools/cleanup_render_cache.py
清理影片渲染生成產生的中間影格快取目錄（如 proofs/render_18s、proofs/five_races_frames）
避免大量逐格 PNG 佔據磁碟空間與干擾版控。
"""
import os, shutil

dirs_to_clean = [
    "/opt/side/bravesoul-game/proofs/render_18s",
    "/opt/side/bravesoul-game/proofs/five_races_frames",
    "/tmp/contact_sheet_samples"
]

for d in dirs_to_clean:
    if os.path.exists(d):
        shutil.rmtree(d, ignore_errors=True)
        print("Cleaned:", d)

print("CLEANUP_DONE")
