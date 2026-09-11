from PIL import Image

im = Image.open('/tmp/perfect_ivory_clean2.png').convert('RGBA')
px = im.load()
w, h = im.size

cleaned_count = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if 0 < a < 64:
            nbr_opaque = sum(1 for dx in [-1,0,1] for dy in [-1,0,1] if (dx!=0 or dy!=0) and 0<=x+dx<w and 0<=y+dy<h and px[x+dx, y+dy][3] >= 64)
            if nbr_opaque == 0:
                im.putpixel((x, y), (0, 0, 0, 0))
                cleaned_count += 1

print(f"Cleaned {cleaned_count} faint isolated background pixels.")
im.save('/tmp/perfect_ivory_clean3.png')
