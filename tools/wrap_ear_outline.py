from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
w, h = ear.size
data = ear.load()

OUTLINE = (44, 28, 22, 255) # #2C1C16 deep warm brown
OUTLINE_AA = (44, 28, 22, 180)

# Let's find all transparent pixels adjacent to ear pixels
out_ear = ear.copy()
out_data = out_ear.load()

# Step 1: For any pixel that is on the current edge:
# If it's cyan rim light or ivory or light color:
# Let's see: if we add a 1-pixel outer dark contour to wrap the ears:
new_pixels = {}
for y in range(h):
    for x in range(w):
        if data[x, y][3] == 0:
            # check 8 neighbors
            has_ear_neighbor = False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        if data[nx, ny][3] > 64:
                            has_ear_neighbor = True
                            break
                if has_ear_neighbor:
                    break
            if has_ear_neighbor:
                # Only wrap the upper parts of the ears (y < 65)
                # where the ears project outside the head
                if y < 65:
                    new_pixels[(x, y)] = OUTLINE

for (x, y), col in new_pixels.items():
    out_data[x, y] = col

out_ear.save("/tmp/ear_wrapped.png")

# Now composite on black background and inspect
dark_bg = Image.new("RGBA", (w, h), (7, 6, 10, 255))
dark_bg.alpha_composite(out_ear)
dark_bg.crop((35, 5, 95, 65)).resize((360, 360), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/ear_wrapped_dark.png")

print("Saved ear wrapped successfully!")
