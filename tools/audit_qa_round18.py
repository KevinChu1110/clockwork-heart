import glob
import os
from PIL import Image

def audit():
    files = sorted(glob.glob('/opt/side/bravesoul-game/proofs/qa_round18/*.png'))
    print(f"Total screenshots: {len(files)}")
    for f in files:
        im = Image.open(f)
        w, h = im.size
        # 取得四角像素確認非全透明貼圖 dump
        corners = [
            im.getpixel((0, 0)),
            im.getpixel((w - 1, 0)),
            im.getpixel((0, h - 1)),
            im.getpixel((w - 1, h - 1))
        ]
        print(f"File: {os.path.basename(f)} | Size: {w}x{h} | Mode: {im.mode} | Corners: {corners[:2]}")

if __name__ == '__main__':
    audit()
