from PIL import Image

screen_crop = Image.open("/tmp/player_drawn_crop_grade_off.png").convert("RGB")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
idle_linear = idle.resize((200, 200), getattr(Image, 'Resampling', Image).BILINEAR)

# In 200x200, where is the blade?
# Source was x in [60, 80], y in [75, 96]
# In 200x200: x in [93, 125], y in [117, 150]
blade_diffs = []
for y in range(117, 150):
    for x in range(93, 125):
        sp = screen_crop.getpixel((x, y))
        ip = idle_linear.getpixel((x, y))
        if ip[3] > 200:
            diff = max(abs(sp[i] - ip[i]) for i in range(3))
            blade_diffs.append((diff, sp, ip[:3], (x, y)))

print(f"Blade pixels tested: {len(blade_diffs)}")
max_b_diff = max(d[0] for d in blade_diffs)
print(f"Max diff in blade area: {max_b_diff}")
# Average RGB in blade area:
s_rgbs = [d[1] for d in blade_diffs]
i_rgbs = [d[2] for d in blade_diffs]
print(f"Screen avg RGB in blade: ({sum(c[0] for c in s_rgbs)/len(s_rgbs):.1f}, {sum(c[1] for c in s_rgbs)/len(s_rgbs):.1f}, {sum(c[2] for c in s_rgbs)/len(s_rgbs):.1f})")
print(f"Idle avg RGB in blade:   ({sum(c[0] for c in i_rgbs)/len(i_rgbs):.1f}, {sum(c[1] for c in i_rgbs)/len(i_rgbs):.1f}, {sum(c[2] for c in i_rgbs)/len(i_rgbs):.1f})")
