from PIL import Image

m_poses = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
grid = Image.new("RGBA", (128 * 6, 128), (50, 50, 50, 255))

for i, p in enumerate(m_poses):
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/{p}.png")
    grid.paste(im, (i * 128, 0), im)

grid.save("/tmp/macaque_poses_row.png")
print("Saved /tmp/macaque_poses_row.png")
