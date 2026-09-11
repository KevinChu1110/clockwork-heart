from PIL import Image

battle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")
print("fox_battle size:", battle_im.size, "bbox:", battle_im.getbbox())

idle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
print("fox_idle size:", idle_im.size, "bbox:", idle_im.getbbox())

# Let's find eye positions in fox_idle vs fox_battle
# Cyan eyes: p[0] < 100, p[1] > 180, p[2] > 180
def find_eyes(im):
    px = im.load()
    assert px is not None
    eyes = []
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[3] > 100 and p[1] > 180 and p[2] > 180 and p[0] < 120:
                eyes.append((x, y))
    return eyes

eyes_idle = find_eyes(idle_im)
eyes_battle = find_eyes(battle_im)
print(f"idle eyes count={len(eyes_idle)}, min_y={min(y for x,y in eyes_idle)}, max_y={max(y for x,y in eyes_idle)}, avg_y={sum(y for x,y in eyes_idle)/len(eyes_idle):.1f}")
print(f"battle eyes count={len(eyes_battle)}, min_y={min(y for x,y in eyes_battle)}, max_y={max(y for x,y in eyes_battle)}, avg_y={sum(y for x,y in eyes_battle)/len(eyes_battle):.1f}")
