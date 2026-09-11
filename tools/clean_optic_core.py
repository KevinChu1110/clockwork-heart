from PIL import Image

core = Image.open("game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png").convert("RGBA")
px = core.load()
w, h = core.size

# In optic_core, the legitimate parts are:
# 1. Chest energy emerald: y >= 70
# 2. Eye sensor jewels: green optic lenses
# Let's inspect all pixels with y < 70
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a > 0 and y < 70:
            # Check if this pixel is an eye lens (green/emerald, g > r and g > b)
            is_green_lens = (g > 60 and g > r * 1.2 and g > b * 1.1)
            is_eye_frame = (max(r, g, b) < 60 and 46 <= x <= 55 and 41 <= y <= 51)
            is_eye_highlight = (r > 200 and g > 200 and b > 200 and 46 <= x <= 55 and 41 <= y <= 51)
            
            # If it's skin/chassis color (r > 100, r > g), it's LEAKED chassis slice in optic_core!
            is_leaked_skin = (r >= 100 and r >= g and not is_green_lens)
            if is_leaked_skin:
                print(f"Leaked skin pixel in optic_core at ({x}, {y}): {(r, g, b, a)}")
                px[x, y] = (0, 0, 0, 0)
            elif y < 51 and not (45 <= x <= 56):
                # Outside left eye area
                print(f"Stray pixel in optic_core at ({x}, {y}): {(r, g, b, a)}")
                px[x, y] = (0, 0, 0, 0)

core.save("/tmp/clean_optic_core.png")
