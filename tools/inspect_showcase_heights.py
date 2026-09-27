from PIL import Image

races = ["cat", "owl", "hound", "otter", "raccoon", "pangolin", "fawn", "wolf", "hedgehog"]
for r in races:
    p = f"game/assets/sprites/player/showcase/{r}_idle_hd.png"
    img = Image.open(p)
    bbox = img.getbbox()
    char_w = bbox[2] - bbox[0]
    char_h = bbox[3] - bbox[1]
    print(f"{r:10s}: total={img.size}, bbox={bbox}, char_size=({char_w}x{char_h}), ground_y={bbox[3]}")
