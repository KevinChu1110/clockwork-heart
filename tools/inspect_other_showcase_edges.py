from PIL import Image

for r in ["owl", "hound", "otter", "raccoon", "pangolin", "fawn", "wolf"]:
    p = f"game/assets/sprites/player/showcase/{r}_idle_hd.png"
    img = Image.open(p)
    # Check left edge pixels
    crop_l = img.crop((0, 300, 50, 700))
    # Count how many rows at x=0 have alpha > 0
    alpha_0 = [img.getpixel((0, y))[3] > 0 for y in range(img.height)]
    alpha_799 = [img.getpixel((799, y))[3] > 0 for y in range(img.height)]
    print(f"{r:10s}: count(x=0 alpha>0) = {sum(alpha_0)}, count(x=799 alpha>0) = {sum(alpha_799)}")
