from PIL import Image, ImageChops

base_im = Image.open("proofs/combat_feel/tmp_rf/frame_010.png")
for i in range(11, 106):
    cur_im = Image.open(f"proofs/combat_feel/tmp_rf/frame_{i:03d}.png")
    diff = ImageChops.difference(base_im, cur_im)
    b = diff.getbbox()
    if b:
        print(f"Frame {i:03d} changed! bbox={b}")
