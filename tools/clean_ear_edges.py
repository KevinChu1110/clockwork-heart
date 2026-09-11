from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
w, h = ear.size
data = ear.load()

new_ear = ear.copy()
new_data = new_ear.load()

# Dark outline colors from art_direction.md:
# Primary outline: (44, 28, 22)
# AA transition: (54, 38, 30)

for y in range(h):
    for x in range(w):
        r, g, b, a = data[x, y]
        if a > 0:
            touches_alpha0 = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h or data[nx, ny][3] == 0:
                    touches_alpha0 = True
                    break
            if touches_alpha0:
                lum = (r + g + b) / 3
                if lum > 130:
                    # It's a bright pixel directly on the outer border!
                    # Give it a clean dark warm brown outline:
                    new_data[x, y] = (44, 28, 22, min(255, max(180, a)))

new_ear.save("/tmp/clean_ear.png")

# Also composite on black background to compare before and after
dark_bg1 = Image.new("RGBA", (w, h), (7, 6, 10, 255))
dark_bg1.alpha_composite(ear)
dark_bg1.crop((35, 5, 95, 65)).resize((360, 360), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/ear_before_dark.png")

dark_bg2 = Image.new("RGBA", (w, h), (7, 6, 10, 255))
dark_bg2.alpha_composite(new_ear)
dark_bg2.crop((35, 5, 95, 65)).resize((360, 360), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/ear_after_dark.png")

print("Saved ear before and after on dark bg")
