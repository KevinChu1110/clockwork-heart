from PIL import Image
import numpy as np

base_dir = "game/assets/sprites/player/paperdoll/chameleon"
key_src = Image.open(f"{base_dir}/winding_key/key_chameleon_prismatic_trivane.png").convert("RGBA")
comp_src = Image.open(f"{base_dir}/proof_paperdoll_chameleon_composite.png").convert("RGBA")

# Let's inspect where key pixels connect to chassis
k_arr = np.array(key_src)
print("Key bbox:", key_src.getbbox())
for y in range(key_src.getbbox()[1], key_src.getbbox()[1] + 6):
    print(f"y={y}: row opaque pixels = {np.sum(k_arr[y, :, 3] > 20)}")

# If we shift key down by 2 px:
shifted_key = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
shifted_key.paste(key_src, (0, 2), key_src)
print("Shifted key bbox:", shifted_key.getbbox())
