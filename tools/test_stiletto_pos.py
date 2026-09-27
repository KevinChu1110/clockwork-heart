from PIL import Image, ImageChops, ImageOps
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat"
body_master = Image.open(f"{BASE_DIR}/proof_paperdoll_cat_composite.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_cat_shadowspring_stiletto.png").convert("RGBA")
wpn_bbox = weapon_src.getbbox()
scepter_raw = weapon_src.crop(wpn_bbox)

def place_stiletto(stiletto_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    b = stiletto_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    bw, bh = b.size
    gx, gy = bw / 2.0, bh / 2.0

    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(b, (int(round(128 - gx)), int(round(128 - gy))))

    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        offset = (nw - canvas_size) // 2
        large = scaled.crop((offset, offset, offset + canvas_size, offset + canvas_size))

    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_center
    out.paste(rotated, (tx - 128, ty - 128), rotated)
    return out

# Check idle alignment
placed = place_stiletto(scepter_raw, deg=0, target_center=(92, 79), scale=1.0)
diff = ImageChops.difference(placed, weapon_src)
bbox = diff.getbbox()
print(f"Diff bbox against original weapon_src: {bbox}")
if bbox is not None:
    diff_arr = np.array(diff)
    print("Diff pixel count:", np.sum(np.any(diff_arr > 0, axis=-1)))
