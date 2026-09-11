from PIL import Image

m_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"
claws = Image.open(f"{m_dir}/weapon/wpn_spring_claws.png").convert("RGBA")

# Let's inspect non-transparent pixels in claws
w, h = claws.size
non_zero = []
for y in range(h):
    for x in range(w):
        p = claws.getpixel((x, y))
        if p[3] > 8:
            non_zero.append((x, y, p))

print(f"Total pixels in wpn_spring_claws: {len(non_zero)}")
# cluster them
xs = [p[0] for p in non_zero]
ys = [p[1] for p in non_zero]
print(f"X range: {min(xs)} - {max(xs)}, Y range: {min(ys)} - {max(ys)}")

# Are there two hands?
left_hand = [p for p in non_zero if p[0] < 50]
right_hand = [p for p in non_zero if p[0] >= 50]
print(f"Left cluster: {len(left_hand)} pixels, X: {min(p[0] for p in left_hand) if left_hand else None}..{max(p[0] for p in left_hand) if left_hand else None}")
print(f"Right cluster: {len(right_hand)} pixels, X: {min(p[0] for p in right_hand) if right_hand else None}..{max(p[0] for p in right_hand) if right_hand else None}")
