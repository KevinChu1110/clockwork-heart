from PIL import Image

core = Image.open("game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png").convert("RGBA")
px = core.load()
w, h = core.size

# Clean everything above chest core (y < 70)
for y in range(70):
    for x in range(w):
        px[x, y] = (0, 0, 0, 0)

core.save("game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png")
print("✓ Cleaned macaque optic_core: removed leaked face/crack overlay above y=70")
print(f"  New bbox: {core.getbbox()}")
