import numpy as np
from PIL import Image

def scale2x(image: Image.Image) -> Image.Image:
    im = np.array(image.convert("RGBA"))
    h, w, c = im.shape
    out = np.zeros((h * 2, w * 2, c), dtype=np.uint8)
    
    padded = np.pad(im, ((1, 1), (1, 1), (0, 0)), mode="edge")
    P = padded[1:h+1, 1:w+1]
    A = padded[0:h,   1:w+1]
    B = padded[1:h+1, 2:w+2]
    C = padded[1:h+1, 0:w]
    D = padded[2:h+2, 1:w+1]
    
    def eq(x, y):
        return np.all(x == y, axis=-1)
    
    eq_CA = eq(C, A)
    eq_CD = eq(C, D)
    eq_AB = eq(A, B)
    eq_BD = eq(B, D)
    
    cond1 = eq_CA & ~eq_CD & ~eq_AB
    cond2 = eq_AB & ~eq_CA & ~eq_BD
    cond3 = eq_CD & ~eq_BD & ~eq_CA
    cond4 = eq_BD & ~eq_AB & ~eq_CD
    
    out[0::2, 0::2] = np.where(cond1[:, :, None], A, P)
    out[0::2, 1::2] = np.where(cond2[:, :, None], B, P)
    out[1::2, 0::2] = np.where(cond3[:, :, None], C, P)
    out[1::2, 1::2] = np.where(cond4[:, :, None], D, P)
    
    return Image.fromarray(out)

def build_clean_attack():
    im_128 = Image.open("game/assets/sprites/player/poses/rabbit/attack.png").convert("RGBA")
    
    # Scale 128 -> 256 -> 512 using Scale2x (EPX algorithm)
    im_256 = scale2x(im_128)
    im_512 = scale2x(im_256)
    
    arr = np.array(im_512)
    alpha = arr[:, :, 3]
    
    # Clean up alpha: make character body fully crisp (binary alpha for body, clean gradient for shadow)
    # Character body is y < 470
    # Shadow is y >= 470
    body_mask = np.zeros_like(alpha, dtype=bool)
    body_mask[:470, :] = True
    
    # Clean alpha on body: eliminate low-alpha fuzzy halo (< 60 -> 0, >= 60 -> 255)
    new_alpha = alpha.copy()
    new_alpha[body_mask & (alpha < 60)] = 0
    new_alpha[body_mask & (alpha >= 60)] = 255
    arr[:, :, 3] = new_alpha
    
    clean_im = Image.fromarray(arr)
    clean_im.save("game/assets/sprites/player/poses/rabbit/attack_512.png")
    clean_im.save("game/assets/sprites/player/poses/attack_512.png")
    print("Saved clean attack_512 to rabbit and root poses.")

if __name__ == "__main__":
    build_clean_attack()
