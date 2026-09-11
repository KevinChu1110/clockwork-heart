from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")

scale = 200.0 / 128.0
ox = 224.0
oy = 248.0 # 223 + 25

# Let's inspect candidate connected components or regions in idle:
# Where is the blade?
# In wpn_dawn_blade.png, what is its bbox?
wpn = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/weapon/wpn_dawn_blade.png").convert("RGBA")
print("wpn_dawn_blade bbox:", wpn.getbbox())
w_data = wpn.load()
wpn_silver = []
for y in range(wpn.height):
    for x in range(wpn.width):
        r, g, b, a = w_data[x, y]
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            wpn_silver.append((x, y, r, g, b))

print("wpn_silver count in wpn_dawn_blade.png:", len(wpn_silver))

# Now let's check in idle.png: what pixels in the weapon region:
# If we filter idle.png by wpn's bbox or non-zero area:
blade_pixels_in_idle = []
for x, y, _, _, _ in wpn_silver:
    r, g, b, a = idle.getpixel((x, y))
    if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
        blade_pixels_in_idle.append((x, y, r, g, b))

print("blade_pixels_in_idle count:", len(blade_pixels_in_idle))
if blade_pixels_in_idle:
    avg_r = sum(p[2] for p in blade_pixels_in_idle) / len(blade_pixels_in_idle)
    avg_g = sum(p[3] for p in blade_pixels_in_idle) / len(blade_pixels_in_idle)
    avg_b = sum(p[4] for p in blade_pixels_in_idle) / len(blade_pixels_in_idle)
    print(f"Average RGB of blade_pixels_in_idle: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})")
