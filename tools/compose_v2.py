from PIL import Image

f_poses = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
grid = Image.new("RGBA", (128 * 6, 128), (40, 40, 40, 255))

for i, p in enumerate(f_poses):
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/{p}.png")
    print(f"Adding {p}: size={im.size}, bbox={im.getbbox()}")
    grid.paste(im, (i * 128, 0), im)

grid.save("/tmp/fox_poses_v2.png")
print("Saved /tmp/fox_poses_v2.png successfully!")
