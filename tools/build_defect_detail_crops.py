import os
from PIL import Image, ImageDraw, ImageFont

base_proofs = "/opt/side/bravesoul-game/proofs/eight_races_paperdoll_review"
ws_proofs = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6735af1a/proofs/eight_races_paperdoll_review"

try:
    font_path = "/opt/side/bravesoul-game/game/assets/fonts/jf-openhuninn-2.1.ttf"
    font_title = ImageFont.truetype(font_path, 16)
    font_sub = ImageFont.truetype(font_path, 12)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# Focus on:
# 1. Bear berserker_cuirass neckline vs ironclad_overalls neckline vs none
# 2. Penguin abyssal_diver_cuirass neckline vs navigator_harness neckline vs none
# 3. Fox ears across orange, ivory, emerald
# 4. Lion ears across brass, ivory, midnight
# 5. Boar cowl across brass, ivory, crimson
# 6. Tiger head/ears across orange, black, ivory
# 7. Macaque monk/striker thickness
# 8. Crane robe/mail thickness

# Let us generate specific side-by-side comparison images for these:
os.makedirs(os.path.join(base_proofs, "details"), exist_ok=True)
os.makedirs(os.path.join(ws_proofs, "details"), exist_ok=True)

# 1. Bear Neckline Detail (berserker vs ironclad vs bare)
# Crop regions from crop_bear_*.png:
# size of crop is approx 250 x 420. Neckline is around y: 80 to 200, x: 50 to 200
def make_comparison_strip(images_info, out_filename, title):
    # images_info: list of (img_path, label, sublabel)
    n = len(images_info)
    w, h = 200, 240
    strip = Image.new("RGB", (n * w + 20, h + 50), (245, 245, 240))
    draw = ImageDraw.Draw(strip)
    draw.text((10, 10), title, fill=(30, 20, 40), font=font_title)
    
    for i, (p, label, sub) in enumerate(images_info):
        x = 10 + i * w
        y = 40
        draw.rectangle([x, y, x + w - 4, y + h - 4], fill=(255, 255, 255), outline=(200, 190, 180))
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            # Crop to chest/neck region: x: 30..220, y: 50..260
            cropped = im.crop((30, 50, 220, 260))
            im_resized = cropped.resize((w - 8, h - 40), Image.Resampling.LANCZOS)
            strip.paste(im_resized, (x + 2, y + 2))
        draw.text((x + w // 2, y + h - 32), label, fill=(50, 40, 60), font=font_sub, anchor="mt")
        draw.text((x + w // 2, y + h - 16), sub, fill=(120, 110, 130), font=font_sub, anchor="mt")
        
    p1 = os.path.join(base_proofs, "details", out_filename)
    p2 = os.path.join(ws_proofs, "details", out_filename)
    strip.save(p1)
    strip.save(p2)
    print(f"  ✓ Saved detail: {p1}")

# Detail 1: Bear Neckline (Berserker Cuirass has flat horizontal neckline at chin)
make_comparison_strip([
    (os.path.join(base_proofs, "bear", "crop_bear_berserker_cuirass_bear_amber.png"), "狂戰破陣機關戰鎧", "筆直水平切線(瑕疵2)"),
    (os.path.join(base_proofs, "bear", "crop_bear_ironclad_overalls_bear_amber.png"), "重裝工作吊帶甲", "具備圓弧吊帶(正常)"),
    (os.path.join(base_proofs, "bear", "crop_bear_none_bear_amber.png"), "無外裝 (素體)", "基準裸機")
], "detail_bear_neckline_comparison.png", "【玄軸熊】狂戰戰鎧領口筆直水平切線 vs 吊帶甲弧度對照")

# Detail 2: Penguin Neckline (Abyssal Diver Cuirass has flat horizontal neckline at chin)
make_comparison_strip([
    (os.path.join(base_proofs, "penguin", "crop_penguin_abyssal_diver_cuirass_penguin_navy.png"), "淵海深潛耐壓機關鎧", "筆直水平切線(瑕疵2)"),
    (os.path.join(base_proofs, "penguin", "crop_penguin_navigator_harness_penguin_navy.png"), "深海導航員大衣", "具備大衣領口(正常)"),
    (os.path.join(base_proofs, "penguin", "crop_penguin_none_penguin_navy.png"), "無外裝 (素體)", "基準裸機")
], "detail_penguin_neckline_comparison.png", "【蒸氣企鵝】淵海機關鎧領口筆直水平切線 vs 導航大衣對照")

# Detail 3: Fox Ears across 3 paints
def make_ear_strip(images_info, out_filename, title):
    n = len(images_info)
    w, h = 180, 200
    strip = Image.new("RGB", (n * w + 20, h + 50), (245, 245, 240))
    draw = ImageDraw.Draw(strip)
    draw.text((10, 10), title, fill=(30, 20, 40), font=font_title)
    for i, (p, label, sub) in enumerate(images_info):
        x = 10 + i * w
        y = 40
        draw.rectangle([x, y, x + w - 4, y + h - 4], fill=(255, 255, 255), outline=(200, 190, 180))
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            # Crop to head/ears: x: 30..220, y: 10..150
            cropped = im.crop((30, 10, 220, 160))
            im_resized = cropped.resize((w - 8, h - 40), Image.Resampling.LANCZOS)
            strip.paste(im_resized, (x + 2, y + 2))
        draw.text((x + w // 2, y + h - 32), label, fill=(50, 40, 60), font=font_sub, anchor="mt")
        draw.text((x + w // 2, y + h - 16), sub, fill=(120, 110, 130), font=font_sub, anchor="mt")
    p1 = os.path.join(base_proofs, "details", out_filename)
    p2 = os.path.join(ws_proofs, "details", out_filename)
    strip.save(p1)
    strip.save(p2)
    print(f"  ✓ Saved detail: {p1}")

make_ear_strip([
    (os.path.join(base_proofs, "fox", "crop_fox_none_fox_orange.png"), "靈狐曜橙 (基準)", "橙耳配橙身 (吻合)"),
    (os.path.join(base_proofs, "fox", "crop_fox_none_ivory_stock.png"), "原廠象牙白", "橙耳配白身 (未同步)"),
    (os.path.join(base_proofs, "fox", "crop_fox_none_emerald_glaze.png"), "翡翠螢光釉面", "橙耳配綠身 (未同步)")
], "detail_fox_ear_colors.png", "【靈尾狐】雷達耳未隨塗裝同步換色（瑕疵3：各塗裝均殘留曜橙耳）")

make_ear_strip([
    (os.path.join(base_proofs, "lion", "crop_lion_none_brass_gold.png"), "黃銅原金 (基準)", "黃金鬃毛配黃金身"),
    (os.path.join(base_proofs, "lion", "crop_lion_none_ivory_stock.png"), "原廠象牙白", "黃金鬃毛配象牙身"),
    (os.path.join(base_proofs, "lion", "crop_lion_none_midnight_navy.png"), "午夜深藍烤漆", "黃金鬃毛配深藍身")
], "detail_lion_mane_colors.png", "【烈鬃獅】鍍金鬃毛未隨塗裝換色（各塗裝均為黃銅鬃毛）")

make_ear_strip([
    (os.path.join(base_proofs, "boar", "crop_boar_none_brass_gold.png"), "黃銅原金", "鐵灰鉚釘頭罩"),
    (os.path.join(base_proofs, "boar", "crop_boar_none_ivory_stock.png"), "原廠象牙白", "鐵灰鉚釘頭罩"),
    (os.path.join(base_proofs, "boar", "crop_boar_none_molten_crimson.png"), "赤焰熔爐", "鐵灰頭罩配赤焰身")
], "detail_boar_cowl_colors.png", "【鋼牙豕】鉚釘頭罩未隨塗裝換色（各塗裝均為生鐵灰頭罩）")

make_ear_strip([
    (os.path.join(base_proofs, "tiger", "crop_tiger_none_ember_orange.png"), "原廠餘燼橙紅", "橙紅虎耳配橙紅身"),
    (os.path.join(base_proofs, "tiger", "crop_tiger_none_volcano_black.png"), "鍛爐淬火曜黑", "橙紅虎耳配黑身"),
    (os.path.join(base_proofs, "tiger", "crop_tiger_none_ivory_stock.png"), "原廠象牙白", "橙紅虎耳配白身")
], "detail_tiger_ear_colors.png", "【烈焰虎】虎耳／頭部機關未隨塗裝換色（黑／白塗裝殘留橙紅耳）")

make_ear_strip([
    (os.path.join(base_proofs, "penguin", "crop_penguin_none_penguin_navy.png"), "原廠深海鍍鈦藍", "深海藍頭配深藍身"),
    (os.path.join(base_proofs, "penguin", "crop_penguin_none_polar_frost.png"), "極光冰川銀白", "深海藍頭配銀白身"),
    (os.path.join(base_proofs, "penguin", "crop_penguin_none_ivory_stock.png"), "原廠象牙白", "深海藍頭配象牙身")
], "detail_penguin_head_colors.png", "【蒸氣企鵝】頭部機關未隨塗裝換色（銀白／象牙塗裝殘留深海藍頭）")
