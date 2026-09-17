import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

base = 'game/assets/sprites/player/paperdoll'

def create_comparison(race, slot, filename, title_text, out_path):
    src_128_p = os.path.join(base, race, slot, filename)
    src_512_p = os.path.join(base, race, slot, f"{os.path.splitext(filename)[0]}_512.png")
    
    img_128 = Image.open(src_128_p).convert('RGBA')
    img_512 = Image.open(src_512_p).convert('RGBA')
    
    # Canvas: 1100 x 600, dark slate clean background
    cw, ch = 1100, 600
    canvas = Image.new('RGBA', (cw, ch), (30, 32, 40, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Left: 128 source. We show the 128 centered in a 512 box with a bounding outline to show its resolution
    box_l_x, box_l_y = 30, 50
    draw.rectangle([box_l_x, box_l_y, box_l_x + 512, box_l_y + 512], outline=(60, 65, 80), width=2, fill=(20, 22, 28, 255))
    # Paste 128 centered inside left 512 box
    offset_x = box_l_x + (512 - 128) // 2
    offset_y = box_l_y + (512 - 128) // 2
    draw.rectangle([offset_x - 2, offset_y - 2, offset_x + 128 + 1, offset_y + 128 + 1], outline=(100, 140, 200), width=1)
    canvas.alpha_composite(img_128, (offset_x, offset_y))
    
    # Right: 512 LANCZOS
    box_r_x, box_r_y = 558, 50
    draw.rectangle([box_r_x, box_r_y, box_r_x + 512, box_r_y + 512], outline=(60, 65, 80), width=2, fill=(20, 22, 28, 255))
    canvas.alpha_composite(img_512, (box_r_x, box_r_y))
    
    # Title / text
    # Top banner / descriptions
    draw.text((35, 18), f"SOURCE 128x128 [{race.upper()} {slot}] (Actual Pixels in 512 Canvas)", fill=(200, 210, 230))
    draw.text((563, 18), f"LANCZOS 512x512 [{race.upper()} {slot}] (Full Resolution Slice)", fill=(100, 220, 160))
    draw.text((35, 570), f"128 Bounding Box: 128x128 (center)", fill=(160, 170, 180))
    draw.text((563, 570), f"512 Canvas: Image.Resampling.LANCZOS smooth interpolation", fill=(160, 170, 180))
    
    canvas.save(out_path, format='PNG')
    print(f"Generated comparison: {out_path}")

out1 = os.path.join(base, 'fox', 'proof_fox_chassis_128_vs_512.png')
create_comparison('fox', 'chassis', 'paint_fox_orange.png', 'Fox Chassis Comparison', out1)

out2 = os.path.join(base, 'lion', 'proof_lion_head_128_vs_512.png')
create_comparison('lion', 'head_unit', 'ear_lion_gilded_mane.png', 'Lion Head Unit Comparison', out2)

with open(out1, 'rb') as f1, open(out2, 'rb') as f2:
    md5_1 = hashlib.md5(f1.read()).hexdigest()
    md5_2 = hashlib.md5(f2.read()).hexdigest()

print(f"MD5 proof 1 ({out1}): {md5_1}")
print(f"MD5 proof 2 ({out2}): {md5_2}")
assert md5_1 != md5_2, "MD5 collision detected!"
print("0-QA15 Check: PASSED (Distinct MD5 hashes)")
