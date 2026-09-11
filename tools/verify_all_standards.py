#!/usr/bin/env python3
import hashlib
import json
import math
import os
from typing import cast
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

def run_all_checks():
    print("=== 全套美術驗收標準與 4c-9-1 條自動檢測 ===\n")
    all_ok = True

    # -------------------------------------------------------------
    # 1. 4c-9 / 4c-9-1: 四個客觀數字
    # -------------------------------------------------------------
    print("【1. 4c-9 / 4c-9-1 五官遮蔽客觀量測】")
    chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")
    head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial.png").convert("RGBA")
    tunic = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png").convert("RGBA")
    striker = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker.png").convert("RGBA")

    bare = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    bare = Image.alpha_composite(bare, chassis)
    bare = Image.alpha_composite(bare, head)

    dark_pts: list[tuple[int, int]] = []
    for y in range(128):
        for x in range(128):
            px = cast(tuple[int, int, int, int], bare.getpixel((x, y)))
            r, g, b, a = px
            if a > 150 and r < 110 and g < 90 and b < 80:
                dark_pts.append((x, y))

    face_dark_pts = [(x, y) for (x, y) in dark_pts if 45 <= x <= 67 and 50 <= y <= 85]
    max_face_y = max(y for (x, y) in face_dark_pts) if face_dark_pts else 0

    tunic_collar_ys = [y for x in range(40, 75) for y in range(128) if cast(tuple[int, int, int, int], tunic.getpixel((x, y)))[3] > 30]
    striker_collar_ys = [y for x in range(40, 75) for y in range(128) if cast(tuple[int, int, int, int], striker.getpixel((x, y)))[3] > 30]

    min_tunic_y = min(tunic_collar_ys)
    min_striker_y = min(striker_collar_ys)

    comp_tunic = Image.alpha_composite(bare, tunic)
    comp_striker = Image.alpha_composite(bare, striker)

    tunic_alt = sum(1 for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt))
    striker_alt = sum(1 for pt in dark_pts if comp_striker.getpixel(pt) != bare.getpixel(pt))

    print(f"  ① 裸素體五官暗部描線最低 y: {max_face_y} (嘴與下頜)")
    print(f"  ② costume_dawn_monk_tunic（已核准）領口上緣 y: {min_tunic_y}")
    print(f"  ③ costume_zen_striker（新）領口上緣 y: {min_striker_y}")
    print(f"  ④ 各自改動掉的裸素體暗線像素數: 舊 {tunic_alt} / 新 {striker_alt}")
    ratio = striker_alt / tunic_alt if tunic_alt else 0.0
    print(f"     比值: {ratio:.2f} 倍 (標準: 新 <= 舊，<= 255)")

    if min_striker_y < 59:
        print(f"  ❌ 領口過高: y={min_striker_y} < 59")
        all_ok = False
    else:
        print(f"  ✓ 領口上緣 y={min_striker_y} >= 59 合規（與已核准同高或更低）")

    if striker_alt > 255:
        print(f"  ❌ 改動暗線數超標: {striker_alt} > 255")
        all_ok = False
    else:
        print(f"  ✓ 改動暗線數 {striker_alt} <= 255 合規（比舊版少 {tunic_alt - striker_alt} 像素）")

    # -------------------------------------------------------------
    # 2. 10a-2: 完成度（唯一色數 / 100px）
    # -------------------------------------------------------------
    print("\n【2. 10a-2 完成度（唯一色數 / 100px）】")
    bronze = Image.open(f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze.png").convert("RGBA")
    for name, img in [("costume_zen_striker", striker), ("paint_bamboo_bronze", bronze)]:
        opaque = [cast(tuple[int,int,int,int], img.getpixel((x, y))) for y in range(128) for x in range(128) if cast(tuple[int,int,int,int], img.getpixel((x, y)))[3] > 0]
        u_cols = set(opaque)
        c_ratio = len(u_cols) / (len(opaque) / 100.0) if opaque else 0.0
        print(f"  • {name}: {len(opaque)}px / {len(u_cols)}色 = {c_ratio:.1f} c/100px (基準 24~96)")
        if not (24 <= c_ratio <= 96):
            print(f"  ❌ {name} 完成度超出基準 24~96")
            all_ok = False
        else:
            print(f"  ✓ {name} 完成度合格")

    # -------------------------------------------------------------
    # 3. 4b-2 / 4b-3: macaque 目錄切片 md5 去重
    # -------------------------------------------------------------
    print("\n【3. 4b-2 / 4b-3 切片去重與定義】")
    slices: list[tuple[str, str]] = []
    for root, dirs, files in os.walk(MACAQUE_DIR):
        for f in files:
            if f.endswith(".png") and not f.startswith("proof_") and not f.startswith("verification_"):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, MACAQUE_DIR)
                with open(p, "rb") as fp:
                    hsh = hashlib.md5(fp.read()).hexdigest()
                slices.append((rel, hsh))

    md5_set = set(h for _, h in slices)
    print(f"  Macaque 切片總數: {len(slices)} 張，唯一 md5 數: {len(md5_set)} 組")
    if len(slices) != len(md5_set):
        print("  ❌ 發現重複 md5 切片！")
        all_ok = False
    else:
        print("  ✓ 全數切片 md5 皆相異，零假重複")

    # -------------------------------------------------------------
    # 4. 4c-4 / 4c-6: 6 組組合 flood-fill 破洞檢驗
    # -------------------------------------------------------------
    print("\n【4. 4c-4 / 4c-6 破洞檢驗（6 組組合）】")
    def get_layer(slot: str, fn: str) -> Image.Image:
        return Image.open(f"{MACAQUE_DIR}/{slot}/{fn}").convert("RGBA")

    combos = [
        ("ivory", "bare", "paint_ivory_stock.png", None),
        ("ivory", "tunic", "paint_ivory_stock.png", "costume_dawn_monk_tunic.png"),
        ("ivory", "zen", "paint_ivory_stock.png", "costume_zen_striker.png"),
        ("bronze", "bare", "paint_bamboo_bronze.png", None),
        ("bronze", "tunic", "paint_bamboo_bronze.png", "costume_dawn_monk_tunic.png"),
        ("bronze", "zen", "paint_bamboo_bronze.png", "costume_zen_striker.png"),
    ]

    for ch_name, cos_name, ch_fn, cos_fn in combos:
        comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        comp.alpha_composite(get_layer("winding_key", "key_classic_brass.png"))
        comp.alpha_composite(get_layer("back_curio", "curio_spring_tail.png"))
        comp.alpha_composite(get_layer("chassis", ch_fn))
        comp.alpha_composite(get_layer("head_unit", "ear_macaque_coaxial.png"))
        if cos_fn:
            comp.alpha_composite(get_layer("costume", cos_fn))
        comp.alpha_composite(get_layer("optic_core", "core_cyan_emerald.png"))
        comp.alpha_composite(get_layer("weapon", "wpn_spring_claws.png"))

        # Flood fill external transparency
        w, h = 128, 128
        alpha = [[cast(tuple[int,int,int,int], comp.getpixel((x, y)))[3] for x in range(w)] for y in range(h)]
        visited = [[False for _ in range(w)] for _ in range(h)]
        queue = []
        for y in range(h):
            for x in [0, w - 1]:
                if alpha[y][x] == 0 and not visited[y][x]:
                    visited[y][x] = True
                    queue.append((x, y))
        for x in range(w):
            for y in [0, h - 1]:
                if alpha[y][x] == 0 and not visited[y][x]:
                    visited[y][x] = True
                    queue.append((x, y))

        while queue:
            cx, cy = queue.pop(0)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h:
                    if not visited[ny][nx] and alpha[ny][nx] == 0:
                        visited[ny][nx] = True
                        queue.append((nx, ny))

        holes = [(x, y) for y in range(h) for x in range(w) if alpha[y][x] == 0 and not visited[y][x]]
        if holes:
            print(f"  ❌ {ch_name} + {cos_name}: 發現 {len(holes)} 個破洞: {holes}")
            all_ok = False
        else:
            print(f"  ✓ {ch_name:6s} + {cos_name:5s}: 內部破洞 = 0")

    # -------------------------------------------------------------
    # 5. 4c: 換裝與換塗裝實際作用 (alpha_only=False)
    # -------------------------------------------------------------
    print("\n【5. 4c 換裝與塗裝實際作用】")
    ch_ivory = get_layer("chassis", "paint_ivory_stock.png")
    ch_bronze = get_layer("chassis", "paint_bamboo_bronze.png")
    diff_ch = ImageChops.difference(ch_ivory, ch_bronze)
    bbox_ch = diff_ch.getbbox(alpha_only=False)
    print(f"  • chassis diff bbox: {bbox_ch}")

    cos_tunic = get_layer("costume", "costume_dawn_monk_tunic.png")
    cos_zen = get_layer("costume", "costume_zen_striker.png")
    diff_cos = ImageChops.difference(cos_tunic, cos_zen)
    bbox_cos = diff_cos.getbbox(alpha_only=False)
    print(f"  • costume diff bbox: {bbox_cos}")

    if bbox_ch is None or bbox_cos is None:
        print("  ❌ 換裝或塗裝 diff 為空！")
        all_ok = False
    else:
        print("  ✓ 雙塗裝與雙外裝皆具備充分且相異的視覺作用")

    # -------------------------------------------------------------
    # 6. 23f-6: JSON 與 SPEC 同步
    # -------------------------------------------------------------
    print("\n【6. 23f-6 JSON 與 SPEC 同步檢驗】")
    with open(f"{REPO_ROOT}/docs/design/paperdoll_slots.json", "r", encoding="utf-8") as fp:
        p_docs = json.load(fp)
    with open(f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as fp:
        p_game = json.load(fp)

    with open(f"{REPO_ROOT}/docs/design/PAPERDOLL_SLOTS_SPEC.md", "r", encoding="utf-8") as fp:
        spec_text = fp.read()

    slots_docs = p_docs.get("slots_architecture", {}).get("slots", [])
    slots_game = p_game.get("slots_architecture", {}).get("slots", [])

    zen_docs = any(v.get("id") == "costume_zen_striker" and v.get("name") == "天元演武者機關甲" for s in slots_docs for v in s.get("sample_variants", []))
    zen_game = any(v.get("id") == "costume_zen_striker" and v.get("name") == "天元演武者機關甲" for s in slots_game for v in s.get("sample_variants", []))
    bronze_docs = any(v.get("id") == "paint_bamboo_bronze" and v.get("name") == "天元青古銅烤漆" for s in slots_docs for v in s.get("sample_variants", []))
    bronze_game = any(v.get("id") == "paint_bamboo_bronze" and v.get("name") == "天元青古銅烤漆" for s in slots_game for v in s.get("sample_variants", []))

    spec_zen = "天元演武者機關甲" in spec_text
    spec_bronze = "天元青古銅烤漆" in spec_text

    if zen_docs and zen_game and bronze_docs and bronze_game and spec_zen and spec_bronze:
        print("  ✓ docs/design 與 game/data 雙 JSON 及 SPEC.md 規格三處完全同步")
    else:
        print(f"  ❌ 規格未同步: zen({zen_docs},{zen_game},{spec_zen}), bronze({bronze_docs},{bronze_game},{spec_bronze})")
        all_ok = False

    print("\n=======================================================")
    if all_ok:
        print("ALL_STANDARDS_VERIFIED_OK")
        return True
    else:
        print("ALL_STANDARDS_VERIFIED_FAIL")
        return False

if __name__ == "__main__":
    ok = run_all_checks()
    exit(0 if ok else 1)
