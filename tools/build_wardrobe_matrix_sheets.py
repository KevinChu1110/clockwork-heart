import os
from PIL import Image, ImageDraw, ImageFont

races_meta = {
    "lion": {
        "name_zh": "烈鬃獅 (Lion)",
        "costumes": [("nutcracker_guard", "胡桃鉗近衛軍裝"), ("steam_artisan", "蒸氣工匠吊帶裝"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("brass_gold", "黃銅原金拋光"), ("ivory_stock", "原廠象牙白"), ("midnight_navy", "午夜深藍烤漆")]
    },
    "fox": {
        "name_zh": "靈尾狐 (Fox)",
        "costumes": [("astral_cape", "星紋見習斗篷"), ("astral_observer", "星象觀測者儀裝"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("fox_orange", "靈狐曜橙烤漆"), ("ivory_stock", "原廠象牙白"), ("emerald_glaze", "翡翠螢光釉面")]
    },
    "boar": {
        "name_zh": "鋼牙豕 (Boar)",
        "costumes": [("viking_harness", "粗獷鍛爐鐵束帶"), ("viking_ironclad", "維京重裝鍛鐵板甲"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("brass_gold", "黃銅原金拋光"), ("ivory_stock", "原廠象牙白"), ("molten_crimson", "赤焰熔爐烤漆")]
    },
    "macaque": {
        "name_zh": "靈爪猴 (Macaque)",
        "costumes": [("dawn_monk_tunic", "晨曦行者武道短褂"), ("zen_striker", "天元演武者機關甲"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("ivory_stock", "原廠象牙白"), ("bamboo_bronze", "天元青古銅烤漆")]
    },
    "tiger": {
        "name_zh": "烈焰虎 (Tiger)",
        "costumes": [("ember_tunic", "餘燼工匠淬火戰褂"), ("ash_ninja_garb", "灰燼夜行機關裝"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("ember_orange", "原廠餘燼橙紅"), ("volcano_black", "鍛爐淬火曜黑"), ("ivory_stock", "原廠象牙白")]
    },
    "crane": {
        "name_zh": "雲嵐鶴 (Crane)",
        "costumes": [("zephyr_robe", "凌雲羽衣輕鋼道袍"), ("sky_hunter_mail", "晴空巡獵機關羽甲"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("crane_porcelain", "原廠冷淬青瓷白"), ("zephyr_azure", "晴空凌雲湛藍"), ("ivory_stock", "原廠象牙白")]
    },
    "bear": {
        "name_zh": "玄軸熊 (Bear)",
        "costumes": [("ironclad_overalls", "玄軸工坊工作吊帶甲"), ("berserker_cuirass", "狂戰破陣機關戰鎧"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("bear_amber", "原廠玄軸琥珀棕"), ("iron_quarry", "重裝礦山玄鐵灰"), ("ivory_stock", "原廠象牙白")]
    },
    "penguin": {
        "name_zh": "蒸氣企鵝 (Penguin)",
        "costumes": [("navigator_harness", "深海導航員大衣"), ("abyssal_diver_cuirass", "淵海深潛耐壓機關鎧"), ("none", "無外裝 (裸機素體)")],
        "chassis": [("penguin_navy", "原廠深海鍍鈦藍"), ("polar_frost", "極光冰川銀白"), ("ivory_stock", "原廠象牙白")]
    }
}

base_proofs = "/opt/side/bravesoul-game/proofs/eight_races_paperdoll_review"
ws_proofs = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6735af1a/proofs/eight_races_paperdoll_review"

# Try loading font
try:
    font_path = "/opt/side/bravesoul-game/game/assets/fonts/jf-openhuninn-2.1.ttf"
    font_title = ImageFont.truetype(font_path, 20)
    font_sub = ImageFont.truetype(font_path, 14)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

for r, meta in races_meta.items():
    print(f"Building matrix sheet for {r}...")
    n_cols = len(meta["costumes"])
    n_rows = len(meta["chassis"])
    
    cell_w = 260
    cell_h = 440
    header_h = 60
    label_w = 160
    
    total_w = label_w + n_cols * cell_w + 20
    total_h = header_h + n_rows * cell_h + 20
    
    sheet = Image.new("RGB", (total_w, total_h), (248, 246, 240))
    draw = ImageDraw.Draw(sheet)
    
    # Title
    draw.text((20, 15), f"【{meta['name_zh']}】衣櫥全套件實機對照矩陣 (All Costumes x All Paints)", fill=(30, 20, 50), font=font_title)
    
    # Column Headers (Costumes)
    for c_idx, (cid, cname) in enumerate(meta["costumes"]):
        x = label_w + c_idx * cell_w + cell_w // 2
        draw.text((x, 40), cname, fill=(80, 50, 20), font=font_sub, anchor="mt")
        
    # Rows (Chassis) & Images
    for r_idx, (pid, pname) in enumerate(meta["chassis"]):
        y = header_h + r_idx * cell_h
        # Row label
        draw.text((15, y + cell_h // 2), pname, fill=(50, 40, 70), font=font_sub, anchor="lm")
        draw.text((15, y + cell_h // 2 + 18), f"({pid})", fill=(120, 110, 130), font=font_sub, anchor="lm")
        
        for c_idx, (cid, cname) in enumerate(meta["costumes"]):
            x = label_w + c_idx * cell_w
            crop_fn = f"crop_{r}_{cid}_{pid}.png"
            crop_path = os.path.join(base_proofs, r, crop_fn)
            
            # draw cell background
            draw.rectangle([x + 4, y + 4, x + cell_w - 4, y + cell_h - 4], fill=(255, 255, 255), outline=(210, 200, 190), width=1)
            
            if os.path.exists(crop_path):
                im = Image.open(crop_path).convert("RGB")
                # paste centered in cell
                im_w, im_h = im.size
                scale = min((cell_w - 12) / im_w, (cell_h - 30) / im_h)
                new_w, new_h = int(im_w * scale), int(im_h * scale)
                im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                px = x + (cell_w - new_w) // 2
                py = y + 10 + (cell_h - 30 - new_h) // 2
                sheet.paste(im_resized, (px, py))
            else:
                draw.text((x + cell_w // 2, y + cell_h // 2), "NOT FOUND", fill=(200, 50, 50), font=font_sub, anchor="mm")
                
            # label bottom
            draw.text((x + cell_w // 2, y + cell_h - 18), f"{cid} × {pid}", fill=(140, 140, 150), font=font_sub, anchor="mb")

    # Save to both repo and workspace
    out_repo = os.path.join(base_proofs, f"proof_wardrobe_matrix_{r}.png")
    out_ws = os.path.join(ws_proofs, f"proof_wardrobe_matrix_{r}.png")
    sheet.save(out_repo)
    sheet.save(out_ws)
    print(f"  ✓ Saved matrix: {out_repo}")
