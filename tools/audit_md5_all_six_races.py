#!/usr/bin/env python3
import os
import hashlib

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll"

def get_md5(p: str) -> str:
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

PAIRS = [
    # Lion
    ("Lion Mane Midnight (512)",
     f"{BASE}/lion/head_unit/ear_lion_gilded_mane_midnight_512.png",
     f"{BASE}/lion/head_unit/ear_lion_gilded_mane_ivory_512.png"),
    ("Lion Mane Brass (512)",
     f"{BASE}/lion/head_unit/ear_lion_gilded_mane_brass_512.png",
     f"{BASE}/lion/head_unit/ear_lion_gilded_mane_ivory_512.png"),

    # Fox
    ("Fox Radar Emerald (512)",
     f"{BASE}/fox/head_unit/ear_fox_radar_emerald_512.png",
     f"{BASE}/fox/head_unit/ear_fox_radar_ivory_512.png"),
    ("Fox Radar Emerald vs Stock (512)",
     f"{BASE}/fox/head_unit/ear_fox_radar_emerald_512.png",
     f"{BASE}/fox/head_unit/ear_fox_radar_512.png"),
    ("Fox Radar Orange (512)",
     f"{BASE}/fox/head_unit/ear_fox_radar_orange_512.png",
     f"{BASE}/fox/head_unit/ear_fox_radar_512.png"),

    # Boar
    ("Boar Cowl Crimson (512)",
     f"{BASE}/boar/head_unit/ear_boar_rivet_cowl_crimson_512.png",
     f"{BASE}/boar/head_unit/ear_boar_rivet_cowl_ivory_512.png"),
    ("Boar Cowl Brass (512)",
     f"{BASE}/boar/head_unit/ear_boar_rivet_cowl_brass_512.png",
     f"{BASE}/boar/head_unit/ear_boar_rivet_cowl_ivory_512.png"),

    # Macaque
    ("Macaque Ear Bronze (512)",
     f"{BASE}/macaque/head_unit/ear_macaque_coaxial_bronze_512.png",
     f"{BASE}/macaque/head_unit/ear_macaque_coaxial_ivory_512.png"),

    # Tiger Head & Ear
    ("Tiger Head Volcano (512)",
     f"{BASE}/tiger/head_unit/head_ember_tiger_volcano_512.png",
     f"{BASE}/tiger/head_unit/head_ember_tiger_ivory_512.png"),
    ("Tiger Head Ember (512)",
     f"{BASE}/tiger/head_unit/head_ember_tiger_ember_512.png",
     f"{BASE}/tiger/head_unit/head_ember_tiger_ivory_512.png"),
    ("Tiger Ear Volcano (512)",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_volcano_512.png",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_ivory_512.png"),
    ("Tiger Ear Ember (512)",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_ember_512.png",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_ivory_512.png"),

    # Crane Head
    ("Crane Head Azure (512)",
     f"{BASE}/crane/head_unit/head_cloud_crane_azure_512.png",
     f"{BASE}/crane/head_unit/head_cloud_crane_ivory_512.png"),
    ("Crane Head Porcelain (512)",
     f"{BASE}/crane/head_unit/head_cloud_crane_porcelain_512.png",
     f"{BASE}/crane/head_unit/head_cloud_crane_ivory_512.png"),
]

def main():
    print(f"{'切片名稱':35s} | {'變體 MD5':10s} | {'對照 Stock MD5':14s} | {'比對結果'}")
    print("-" * 75)
    all_pass = True
    for name, p1, p2 in PAIRS:
        if not os.path.exists(p1):
            print(f"Missing {p1}")
            all_pass = False
            continue
        if not os.path.exists(p2):
            print(f"Missing {p2}")
            all_pass = False
            continue
        m1 = get_md5(p1)
        m2 = get_md5(p2)
        diff = (m1 != m2)
        if not diff:
            all_pass = False
        res = "✅ PASS (唯一獨立)" if diff else "❌ FAIL (內容重複)"
        print(f"{name:35s} | {m1[:10]:10s} | {m2[:10]:14s} | {res}")
    print("-" * 75)
    if all_pass:
        print("🎉 全部新切片 MD5 與同族 stock 100% 互異獨立，無偽裝重複檔案！")
    else:
        print("❌ 發現重複切片！")
    return all_pass

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
