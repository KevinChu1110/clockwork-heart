#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

def main():
    before_path = "/tmp/proof_wardrobe_filter_all_before.png"
    after_path = "/opt/side/bravesoul-game/screenshots/proof_wardrobe_filter_all.png"
    
    if not os.path.exists(before_path) or not os.path.exists(after_path):
        print("Missing files")
        return
        
    im_before = Image.open(before_path)
    im_after = Image.open(after_path)
    print("Image sizes:", im_before.size, im_after.size)
    
    # Dialog is roughly centered in 1280x720: width 750, height 580 -> x: 265..1015, y: 70..650
    # Right side of wardrobe dialog contains costume and chassis cards grid
    # Let's crop the cards grid area (roughly x: 540..1010, y: 150..620)
    cards_before = im_before.crop((550, 160, 1000, 600))
    cards_after = im_after.crop((550, 160, 1000, 600))
    cards_before.save("/opt/side/bravesoul-game/screenshots/proof_wardrobe_cards_before.png")
    cards_after.save("/opt/side/bravesoul-game/screenshots/proof_wardrobe_cards_after.png")
    
    # Selected card (Nutcracker Guard, first costume card) is around x: 560..670, y: 200..340
    # Unselected card (e.g. second costume card or chassis card) is around x: 670..780, y: 200..340
    sel_before = im_before.crop((560, 200, 675, 345))
    sel_after = im_after.crop((560, 200, 675, 345))
    unsel_before = im_before.crop((675, 200, 790, 345))
    unsel_after = im_after.crop((675, 200, 790, 345))
    
    sel_after.save("/opt/side/bravesoul-game/screenshots/proof_wardrobe_selected_card.png")
    unsel_after.save("/opt/side/bravesoul-game/screenshots/proof_wardrobe_unselected_card.png")
    
    # Filter chips area is around x: 280..980, y: 120..180
    chips_before = im_before.crop((280, 120, 980, 180))
    chips_after = im_after.crop((280, 120, 980, 180))
    chips_after.save("/opt/side/bravesoul-game/screenshots/proof_wardrobe_chips.png")
    
    # Create comparison canvas
    w = 1200
    h = 800
    comp = Image.new("RGB", (w, h), (31, 26, 58))
    draw = ImageDraw.Draw(comp)
    
    # Paste side-by-side: Selected Card (Before vs After), Unselected Card (Before vs After)
    # Scale up cards by 2x for clear inspection of border and shadow
    sel_b_2x = sel_before.resize((sel_before.width * 2, sel_before.height * 2), Image.Resampling.NEAREST)
    sel_a_2x = sel_after.resize((sel_after.width * 2, sel_after.height * 2), Image.Resampling.NEAREST)
    unsel_b_2x = unsel_before.resize((unsel_before.width * 2, unsel_before.height * 2), Image.Resampling.NEAREST)
    unsel_a_2x = unsel_after.resize((unsel_after.width * 2, unsel_after.height * 2), Image.Resampling.NEAREST)
    
    # Row 1: Selected Card (Before: bottom 4px, shadow 4px vs After: bottom 6px, shadow 6px)
    comp.paste(sel_b_2x, (40, 70))
    comp.paste(sel_a_2x, (300, 70))
    
    # Row 1 Right: Unselected Card (Before: bottom 2px, shadow 0px vs After: bottom 3px, shadow 4px)
    comp.paste(unsel_b_2x, (620, 70))
    comp.paste(unsel_a_2x, (880, 70))
    
    # Paste filter chips before vs after at bottom
    comp.paste(chips_before, (40, 430))
    comp.paste(chips_after, (40, 520))
    
    comp_out = "/opt/side/bravesoul-game/screenshots/proof_wardrobe_jelly_comparison.png"
    comp.save(comp_out)
    print("Saved comparison to:", comp_out)

if __name__ == "__main__":
    main()
