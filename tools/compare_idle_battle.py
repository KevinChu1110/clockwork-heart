from PIL import Image

fb = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png")
fi = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/fox_idle.png")

combo = Image.new("RGBA", (256, 128), (50, 50, 50, 255))
combo.paste(fi, (0, 0), fi)
combo.paste(fb, (128, 0), fb)
combo.save("/tmp/fox_idle_vs_battle.png")
print("Saved /tmp/fox_idle_vs_battle.png")
