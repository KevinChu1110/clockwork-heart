import os
from PIL import Image, ImageDraw, ImageFont

base_dir = "/opt/side/bravesoul-game"
review_dir = os.path.join(base_dir, "proofs/eight_races_paperdoll_review")
fix_dir = os.path.join(base_dir, "proofs/neckline_fix")

try:
    font_path = "/opt/side/bravesoul-game/game/assets/fonts/jf-openhuninn-2.1.ttf"
    font_title = ImageFont.truetype(font_path, 18)
    font_header = ImageFont.truetype(font_path, 15)
    font_sub = ImageFont.truetype(font_path, 12)
except Exception:
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_sub = ImageFont.load_default()

def make_side_by_side_review():
    # 1. Bear Neckline In-Game Comparison (Before vs Fixed vs Overalls)
    # Crop to chest/neck area: (30, 50, 220, 260) from 250x420 crop
    bear_before = os.path.join(review_dir, "bear/crop_bear_berserker_cuirass_bear_amber.png")
    bear_after = os.path.join(fix_dir, "crop_bear_berserker_cuirass_bear_amber_fixed.png")
    bear_overalls = os.path.join(review_dir, "bear/crop_bear_ironclad_overalls_bear_amber.png")
    
    # 2. Penguin Neckline In-Game Comparison (Before vs Fixed vs Navigator)
    pen_before = os.path.join(review_dir, "penguin/crop_penguin_abyssal_diver_cuirass_penguin_navy.png")
    pen_after = os.path.join(fix_dir, "crop_penguin_abyssal_diver_cuirass_penguin_navy_fixed.png")
    pen_nav = os.path.join(review_dir, "penguin/crop_penguin_navigator_harness_penguin_navy.png")
    
    # 3. Tiger Ember Tunic (Passing Baseline)
    tiger_ember = os.path.join(review_dir, "tiger/crop_tiger_ember_tunic_ember_orange.png")

    # Let's generate a 3-column strip for Bear
    def make_strip(images_info, out_path, title):
        n = len(images_info)
        w, h = 220, 260
        strip = Image.new("RGB", (n * w + 20, h + 60), (245, 245, 240))
        draw = ImageDraw.Draw(strip)
        draw.text((15, 10), title, fill=(30, 20, 40), font=font_title)
        
        for i, (p, label, sub, color) in enumerate(images_info):
            x = 10 + i * w
            y = 45
            draw.rectangle([x, y, x + w - 6, y + h - 6], fill=(255, 255, 255), outline=(200, 190, 180))
            if os.path.exists(p):
                im = Image.open(p).convert("RGB")
                cropped = im.crop((25, 45, 225, 265))
                im_resized = cropped.resize((w - 10, h - 45), Image.Resampling.LANCZOS)
                strip.paste(im_resized, (x + 2, y + 2))
            draw.text((x + (w - 6) // 2, y + h - 36), label, fill=color, font=font_header, anchor="mt")
            draw.text((x + (w - 6) // 2, y + h - 18), sub, fill=(100, 95, 110), font=font_sub, anchor="mt")
        
        strip.save(out_path)
        print(f"Saved strip: {out_path}")

    # Bear Strip
    make_strip([
        (bear_before, "修復前 (筆直橫切)", "var=0.00 / 嚴重不合格", (190, 40, 40)),
        (bear_after, "修復後 (自然 U 型微弧)", "var=3.60 / 順應下巴曲線", (30, 130, 40)),
        (bear_overalls, "基準對照 (工作吊帶甲)", "var=1.10 / 已過審標準件", (40, 70, 160))
    ], os.path.join(fix_dir, "proof_bear_neckline_fixed_comparison.png"), "【玄軸熊】狂戰戰鎧領口修復實機對照（修復前 vs 修復後 vs 吊帶甲）")

    # Penguin Strip
    make_strip([
        (pen_before, "修復前 (筆直橫切)", "var=0.00 / 嚴重不合格", (190, 40, 40)),
        (pen_after, "修復後 (自然 U 型微弧)", "var=3.33 / 配合鳥喙下巴", (30, 130, 40)),
        (pen_nav, "基準對照 (導航員大衣)", "var=241.37 / 已過審標準件", (40, 70, 160))
    ], os.path.join(fix_dir, "proof_penguin_neckline_fixed_comparison.png"), "【蒸氣企鵝】淵海機關鎧領口修復實機對照（修復前 vs 修復後 vs 導航大衣）")

    # Three-Way Comparison: Fixed Bear vs Passed Tiger vs Fixed Penguin
    make_strip([
        (bear_after, "玄軸熊·狂戰破陣機關戰鎧", "修復後 (var=3.60, span=6)", (30, 130, 40)),
        (tiger_ember, "烈焰虎·餘燼工匠淬火戰褂", "已過審基準 (var=2.57, span=5)", (40, 70, 160)),
        (pen_after, "蒸氣企鵝·淵海深潛機關鎧", "修復後 (var=3.33, span=6)", (30, 130, 40))
    ], os.path.join(fix_dir, "proof_neckline_natural_curve_baseline_compare.png"), "【領口曲線自然度並排比對】修復後玄軸熊／蒸氣企鵝 vs 已過審烈焰虎基準")

make_side_by_side_review()
