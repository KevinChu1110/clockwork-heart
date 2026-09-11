from PIL import Image

comp = Image.open("/tmp/test_attack_solid.png")
pix = comp.load()

# Let's see alpha values of pixels across the whole comp
alpha_counts = {}
for y in range(comp.height):
    for x in range(comp.width):
        a = pix[x, y][3]
        alpha_counts[a] = alpha_counts.get(a, 0) + 1

print("Alpha distribution in comp:")
for a in sorted(alpha_counts.keys()):
    if a > 0:
        print(f"  alpha={a}: {alpha_counts[a]}")
