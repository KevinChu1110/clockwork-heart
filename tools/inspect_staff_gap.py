from PIL import Image

cand = Image.open("/tmp/test_attack_candidate.png").convert("RGBA")
px = cand.load()
assert px is not None

print("Checking pixels between hand and staff tip...")
# Check around x=95..120, y=70..105
for y in range(70, 105):
    line = ""
    for x in range(95, 125):
        p = px[x, y]
        if p[3] > 40:
            line += "#"
        elif p[3] > 0:
            line += "."
        else:
            line += " "
    if "#" in line or "." in line:
        print(f"y={y:2d}: {line}")
