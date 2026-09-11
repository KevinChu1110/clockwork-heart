#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/test_clean_log.png")
# Full LogPanel is at x: 28 to 1252, y: 532 to 668
crop = im.crop((20, 520, 800, 675))
crop.save("/tmp/test_clean_log_full_panel.png")
print("Saved full panel crop.")
