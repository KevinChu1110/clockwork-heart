from PIL import Image

races = {
    "rabbit": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png",
    "lion": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/idle.png",
    "fox": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png",
    "boar": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/idle.png",
}

for name, path in races.items():
    img = Image.open(path).convert("RGBA")
    # Let's save a 4x version so we can inspect or check
    img_4x = img.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST)
    img_4x.save(f"/tmp/{name}_idle_preview.png")
    print(f"Saved /tmp/{name}_idle_preview.png")
