from PIL import Image

hd = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/showcase/lion_idle_hd.png')
bbox = hd.getbbox()
char_crop = hd.crop(bbox)

# scale to (340, 468) using LANCZOS
char_512 = char_crop.resize((340, 468), Image.Resampling.LANCZOS)

canvas_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
canvas_512.paste(char_512, (84, 36), char_512)
canvas_512.save('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/lion_master_512.png')
print("Saved lion_master_512.png with bbox:", canvas_512.getbbox())
