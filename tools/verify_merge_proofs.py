import os
import hashlib
from PIL import Image

proof_dir = "/opt/side/bravesoul-game/.worktrees/t_a18260c8/proofs/merge_battle_fox_512"
files = [
    "proof_rabbit_attack_512.png",
    "proof_lion_attack_512.png",
    "proof_fox_lobby_512.png"
]

print("=== 0-QA15 / 0-QA18 檢查 ===")
md5s = {}
for f in files:
    p = os.path.join(proof_dir, f)
    assert os.path.exists(p), f"File missing: {p}"
    with open(p, "rb") as fp:
        data = fp.read()
        m = hashlib.md5(data).hexdigest()
        md5s[f] = m
    im = Image.open(p)
    w, h = im.size
    print(f"[{f}] size={w}x{h}, md5={m}")
    assert (w, h) == (1280, 720), f"Size must be 1280x720, got {w}x{h}"

    # Check 4 corners alpha for 0-QA18
    # RGBA or RGB
    im_rgba = im.convert("RGBA")
    corners = [
        im_rgba.getpixel((0, 0)),
        im_rgba.getpixel((w - 1, 0)),
        im_rgba.getpixel((0, h - 1)),
        im_rgba.getpixel((w - 1, h - 1))
    ]
    transparent_corners = sum(1 for c in corners if c[3] == 0)
    print(f"  -> corners alpha: {[c[3] for c in corners]}, transparent={transparent_corners}/4")
    assert transparent_corners < 4, f"0-QA18 violation: all corners are transparent (likely texture dump)!"

assert len(set(md5s.values())) == 3, "0-QA15 violation: MD5 hashes must be distinct!"
print("✓ 0-QA15 / 0-QA18 驗證通過！三張皆為 1280x720 完整畫面，MD5 互不重複，非貼圖 dump。")

# Crop fox head closeup for 0-ART27 verification
lobby_im = Image.open(os.path.join(proof_dir, "proof_fox_lobby_512.png"))
# In lobby, fox character is centered. Let's crop the head region:
# (520, 160, 760, 400)
head_crop = lobby_im.crop((520, 160, 760, 400))
head_crop_path = os.path.join(proof_dir, "proof_fox_lobby_head_closeup.png")
head_crop.save(head_crop_path)
print(f"✓ 狐族大廳頭部特寫裁切完成: {head_crop_path}")
