from PIL import Image

busts = [
    "game/assets/sprites/portraits/porcelain_panda.png",
    "game/assets/sprites/portraits/colossus_elephant.png",
    "game/assets/sprites/portraits/spring_frog.png",
    "game/assets/sprites/portraits/emerald_fawn.png",
    "game/assets/sprites/portraits/xuanji_tortoise.png",
    "game/assets/sprites/portraits/dune_pangolin.png"
]

for b in busts:
    p = f"/opt/side/bravesoul-game/{b}"
    im = Image.open(p)
    bbox = im.getbbox()
    print(f"{b:50s}: size={im.size}, bbox={bbox}, w={bbox[2]-bbox[0]}, h={bbox[3]-bbox[1]}")
