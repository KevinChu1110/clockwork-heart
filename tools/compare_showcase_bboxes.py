from PIL import Image

races = ["cat", "owl", "hound", "otter", "raccoon", "pangolin", "fawn", "wolf", "hedgehog"]
for r in races:
    p = f"game/assets/sprites/player/showcase/{r}_idle_hd.png"
    img = Image.open(p)
    bbox = img.getbbox()
    print(f"{r:12s}: size={img.size}, bbox={bbox}, margin_L={bbox[0]}, margin_R={img.size[0]-bbox[2]}, margin_T={bbox[1]}, margin_B={img.size[1]-bbox[3]}")
