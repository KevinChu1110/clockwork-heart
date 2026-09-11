import os
import sys
from PIL import Image
from typing import cast

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"

def analyze_pose(p_name):
    path = os.path.join(POSES_DIR, f"{p_name}.png")
    im = Image.open(path).convert("RGBA")
    px = im.load()
    assert px is not None
    
    print(f"=== {p_name.upper()} ===")
    # Find top pixels
    top_pixels = []
    bot_pixels = []
    for y in range(118):
        for x in range(128):
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > 10:
                if not top_pixels or y == top_pixels[0][1]:
                    top_pixels.append((x, y, p))
                elif y < top_pixels[0][1]:
                    top_pixels = [(x, y, p)]
    for y in range(117, -1, -1):
        for x in range(128):
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > 10:
                if not bot_pixels or y == bot_pixels[0][1]:
                    bot_pixels.append((x, y, p))
                elif y > bot_pixels[0][1]:
                    bot_pixels = [(x, y, p)]
                    
    print(f"Top row y={top_pixels[0][1] if top_pixels else None}, count={len(top_pixels)}")
    for x, y, p in top_pixels[:5]:
        print(f"  top: ({x}, {y}) rgba={p}")
    print(f"Bot row y={bot_pixels[0][1] if bot_pixels else None}, count={len(bot_pixels)}")
    for x, y, p in bot_pixels[:5]:
        print(f"  bot: ({x}, {y}) rgba={p}")

analyze_pose("idle")
analyze_pose("telegraph")
analyze_pose("attack")
analyze_pose("recover")
analyze_pose("skill")
analyze_pose("hit")
