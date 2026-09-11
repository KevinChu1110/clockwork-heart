from PIL import Image

# Group 1: idle, telegraph, attack
g1_poses = ["idle", "telegraph", "attack"]
g1 = Image.new("RGBA", (128 * 3, 128), (40, 40, 40, 255))
for i, p in enumerate(g1_poses):
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/{p}.png")
    g1.paste(im, (i * 128, 0), im)
g1.save("/tmp/fox_poses_group1.png")

# Group 2: recover, skill, hit
g2_poses = ["recover", "skill", "hit"]
g2 = Image.new("RGBA", (128 * 3, 128), (40, 40, 40, 255))
for i, p in enumerate(g2_poses):
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/{p}.png")
    g2.paste(im, (i * 128, 0), im)
g2.save("/tmp/fox_poses_group2.png")

print("Saved /tmp/fox_poses_group1.png and /tmp/fox_poses_group2.png successfully!")
