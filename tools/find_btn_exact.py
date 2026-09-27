from PIL import Image
import numpy as np

img = Image.open('proofs/shop-sku-i18n/proof_shop_en.png').convert('RGB')
arr = np.array(img)

# Let's find coral pink pixels (#FF5E8A) -> R > 240, G in [70, 120], B in [110, 160]
pink_mask = (arr[:, :, 0] > 230) & (arr[:, :, 1] < 120) & (arr[:, :, 2] > 110) & (arr[:, :, 2] < 170)
ys, xs = np.where(pink_mask)
if len(ys) > 0:
    print(f"Pink button bbox: x=[{xs.min()}, {xs.max()}], y=[{ys.min()}, {ys.max()}]")
    # Crop the pink button exactly!
    btn = img.crop((xs.min() - 5, ys.min() - 5, xs.max() + 5, ys.max() + 5))
    btn.save('/tmp/real_pink_btn.png')
    btn_4x = btn.resize((btn.width * 4, btn.height * 4), Image.Resampling.NEAREST)
    btn_4x.save('/tmp/real_pink_btn_4x.png')
    print("Saved /tmp/real_pink_btn.png and /tmp/real_pink_btn_4x.png")
else:
    print("No pink pixels found")
