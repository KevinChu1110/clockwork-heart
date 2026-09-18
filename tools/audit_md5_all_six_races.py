#!/usr/bin/env python3
"""
tools/audit_md5_all_six_races.py
Audits MD5 hashes across all head_unit files for six races:
Lion, Fox, Boar, Macaque, Tiger, Crane.
Follows review.md 0-ART28n and 0-ART28q.
"""

import os
import glob
import hashlib

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll"
RACES = ["lion", "fox", "boar", "macaque", "tiger", "crane"]

def get_md5(p: str) -> str:
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    print("====================================================================================================")
    print("【驗收查重】六族 head_unit 全量切片 MD5 排序與唯一性查核 (0-ART28n / 0-ART28q)")
    print("====================================================================================================")
    
    known_base_aliases = {
        ("lion", "ear_lion_gilded_mane_brass_512.png"): "ear_lion_gilded_mane_512.png",
        ("macaque", "ear_macaque_coaxial_ivory_512.png"): "ear_macaque_coaxial_512.png",
    }
    
    all_clean = True
    for race in RACES:
        print(f"\n--- [{race.upper()}] head_unit ---")
        pattern = f"{BASE}/{race}/head_unit/*_512.png"
        files = sorted(glob.glob(pattern))
        
        file_hashes = [(os.path.basename(p), get_md5(p)) for p in files]
        file_hashes.sort(key=lambda x: x[1])
        
        hash_counts = {}
        for fname, h in file_hashes:
            hash_counts.setdefault(h, []).append(fname)
            
        for fname, h in file_hashes:
            dup_list = hash_counts[h]
            if len(dup_list) == 1:
                status = "✅ PASS (唯一獨立)"
            else:
                # Check intentional pairings
                if race == "tiger" and any(f.startswith("head_") for f in dup_list) and any(f.startswith("ear_") for f in dup_list):
                    status = "ℹ️ INFO (虎族 head/ear 刻意共用同一切片)"
                elif (race, fname) in known_base_aliases:
                    target_base = known_base_aliases[(race, fname)]
                    status = f"ℹ️ INFO (共用 base [{target_base}]、不另列交付格)"
                elif any((race, other) in known_base_aliases for other in dup_list):
                    status = "ℹ️ INFO (被指定為共用 base 之基底檔)"
                else:
                    status = f"❌ FAIL (非預期重複檔: {', '.join(dup_list)})"
                    all_clean = False
            print(f"{h}  {fname:42s} | {status}")
            
    print("\n" + "=" * 100)
    if all_clean:
        print("🎉 MD5 查重通過！所有切片皆為唯一獨立或符合已知共用 base 設計。")
    else:
        print("❌ 發現未經宣告的切片重複複製問題，未通過 0-ART28n 規範！")
    return all_clean

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
