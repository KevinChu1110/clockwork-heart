import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('/opt/side/bravesoul-game/proofs/debug_info_leak_fix', exist_ok=True)

pairs = [
    ("proof_15_market.png", "Town Market (市集)"),
    ("proof_13_dojo.png", "Dojo (道場)"),
    ("proof_24_caravan.png", "Caravan Camp (行商驛站)"),
    ("proof_16_blackflame.png", "Blackflame Scar (黑焰疤)"),
]

for filename, title in pairs:
    before_path = os.path.join('/tmp/before_proofs', filename)
    after_path = os.path.join('/opt/side/bravesoul-game/screenshots', filename)
    if not os.path.exists(before_path) or not os.path.exists(after_path):
        continue
    im_before = Image.open(before_path).convert('RGB')
    im_after = Image.open(after_path).convert('RGB')
    
    w, h = im_before.size
    # Create side-by-side image: width = 2*w, height = h + 60
    comp = Image.new('RGB', (2 * w, h + 60), (30, 30, 35))
    draw = ImageDraw.Draw(comp)
    
    # Draw titles
    # Left: Before, Right: After
    draw.text((20, 18), f"{title} — BEFORE (修復前：尺寸外洩 / 殘留除錯色塊)", fill=(255, 100, 100))
    draw.text((w + 20, 18), f"{title} — AFTER (修復後：尺寸清除 / 移除殘留色塊)", fill=(100, 255, 150))
    
    comp.paste(im_before, (0, 60))
    comp.paste(im_after, (w, 60))
    
    out_file = os.path.join('/opt/side/bravesoul-game/proofs/debug_info_leak_fix', f"compare_{filename}")
    comp.save(out_file)
    print(f"Saved {out_file}")

    # Also make a focused crop of the minimap (top-right 300x300)
    crop_before = im_before.crop((w - 300, 0, w, 280))
    crop_after = im_after.crop((w - 300, 0, w, 280))
    crop_comp = Image.new('RGB', (600, 320), (30, 30, 35))
    crop_draw = ImageDraw.Draw(crop_comp)
    crop_draw.text((20, 10), "MINIMAP BEFORE", fill=(255, 100, 100))
    crop_draw.text((320, 10), "MINIMAP AFTER", fill=(100, 255, 150))
    crop_comp.paste(crop_before, (0, 40))
    crop_comp.paste(crop_after, (300, 40))
    crop_out = os.path.join('/opt/side/bravesoul-game/proofs/debug_info_leak_fix', f"crop_minimap_{filename}")
    crop_comp.save(crop_out)
    print(f"Saved {crop_out}")

# Specifically for market: crop the center / water trough area where gray rectangles were
crop_m_before = Image.open('/tmp/before_proofs/proof_15_market.png').crop((350, 100, 950, 500))
crop_m_after = Image.open('/opt/side/bravesoul-game/screenshots/proof_15_market.png').crop((350, 100, 950, 500))
crop_m_comp = Image.new('RGB', (1200, 440), (30, 30, 35))
cdraw = ImageDraw.Draw(crop_m_comp)
cdraw.text((20, 10), "MARKET BEFORE (中央沙地天秤台 + 上方水槽布攤 殘留灰色半透明矩形除錯塊)", fill=(255, 100, 100))
cdraw.text((620, 10), "MARKET AFTER (完全清除除錯矩形色塊與多餘陰影)", fill=(100, 255, 150))
crop_m_comp.paste(crop_m_before, (0, 40))
crop_m_comp.paste(crop_m_after, (600, 40))
crop_m_comp.save('/opt/side/bravesoul-game/proofs/debug_info_leak_fix/crop_market_entities.png')
print("Saved /opt/side/bravesoul-game/proofs/debug_info_leak_fix/crop_market_entities.png")
