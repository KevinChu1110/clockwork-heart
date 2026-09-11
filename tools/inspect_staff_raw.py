from PIL import Image

staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
spx = staff_src.load()
assert spx is not None

print("Checking staff_src vertical slices:")
for y in range(35, 128):
    row = [(x, spx[x, y]) for x in range(128) if spx[x, y][3] > 40]
    if row:
        xs = [x for x, p in row]
        print(f"y={y:3d}: x in [{min(xs)}..{max(xs)}], count={len(row)}")
