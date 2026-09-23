#!/usr/bin/env python3
import numpy as np
from PIL import Image, ImageDraw

def test_polygon_mask():
    im = Image.open("/tmp/tortoise_lower_body.png").convert("RGBA")
    w, h = im.size
    
    # Create polygon mask for the character's lower body
    # 0 = transparent, 255 = keep
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    
    # The torso upper area is fully kept across all x
    # Upper band: y=0..70
    draw.rectangle([0, 0, w, 70], fill=255)
    
    # Define polygon contours for the 5 limbs and plastron:
    # Foot 1 (x: 50..130, y: 70..152)
    poly_foot1 = [(45, 70), (135, 70), (130, 150), (100, 153), (55, 150), (45, 110)]
    draw.polygon(poly_foot1, fill=255)
    
    # Gap between Foot 1 and Foot 2: plastron bottom around y=85
    draw.rectangle([125, 70, 175, 88], fill=255)
    
    # Foot 2 (Main fore-left foot, x: 165..315, y: 70..163)
    poly_foot2 = [(165, 85), (315, 85), (310, 158), (280, 164), (180, 163), (165, 130)]
    draw.polygon(poly_foot2, fill=255)
    
    # Gap between Foot 2 and Foot 3: plastron bottom around y=95
    draw.rectangle([300, 70, 335, 96], fill=255)
    
    # Foot 3 (Mid-hind foot, x: 325..415, y: 70..158)
    poly_foot3 = [(325, 90), (415, 90), (410, 158), (340, 158), (325, 120)]
    draw.polygon(poly_foot3, fill=255)
    
    # Foot 4 (Raised hand, x: 410..550, elevated above ground, y: 70..115)
    # The space below y > 115 is EMPTY AIR / GROUND SHADOW!
    poly_foot4 = [(410, 70), (550, 70), (550, 115), (410, 115)]
    draw.polygon(poly_foot4, fill=255)
    
    # Foot 5 (Rightmost foot, x: 570..675, y: 70..162)
    poly_foot5 = [(570, 70), (675, 70), (675, 160), (580, 162), (570, 120)]
    draw.polygon(poly_foot5, fill=255)
    
    # Combine polygon mask with color cleanup (remove pure white within the polygon)
    arr = np.array(im)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    # Pure white background
    is_white = (r > 242) & (g > 242) & (b > 242)
    
    m_arr = np.array(mask)
    # Final alpha is 255 inside polygon except where pure white
    final_alpha = np.where((m_arr > 0) & (~is_white), 255, 0).astype(np.uint8)
    
    arr[:, :, 3] = final_alpha
    cleaned = Image.fromarray(arr)
    cleaned.save("/tmp/tortoise_lower_poly.png")
    
    # Magenta test
    mag = Image.new("RGBA", (w, h), (255, 0, 255, 255))
    mag.alpha_composite(cleaned)
    mag.save("/tmp/tortoise_lower_poly_magenta.png")
    print("Saved /tmp/tortoise_lower_poly_magenta.png")

if __name__ == "__main__":
    test_polygon_mask()
