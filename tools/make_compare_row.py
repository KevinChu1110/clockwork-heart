from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/fox/idle.png")
old_hit = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/fox/hit.png")

v1 = Image.open("/tmp/hit_preview/v1_deg-65_h82_55.png")
v2 = Image.open("/tmp/hit_preview/v2_deg-65_h84_58.png")
v4 = Image.open("/tmp/hit_preview/v4_deg-60_h80_55.png")
v6 = Image.open("/tmp/hit_preview/v6_deg-65_h80_52.png")

row = Image.new("RGBA", (128 * 6, 128), (240, 240, 240, 255))
for i, (title, im) in enumerate([
    ("idle", idle),
    ("old_hit", old_hit),
    ("v1_h82_55", v1),
    ("v2_h84_58", v2),
    ("v4_h80_55", v4),
    ("v6_h80_52", v6),
]):
    row.paste(im, (i * 128, 0), im)

row.save("/tmp/fox_hit_compare_row.png")
print("Saved /tmp/fox_hit_compare_row.png")
