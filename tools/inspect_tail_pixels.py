#!/usr/bin/env python3
from PIL import Image

orig = Image.open("/tmp/cleaned_paint_ivory_stock.png")
print("(97, 51):", orig.getpixel((97, 51)))
print("(98, 51):", orig.getpixel((98, 51)))
print("(98, 52):", orig.getpixel((98, 52)))
print("(92, 61):", orig.getpixel((92, 61)))
