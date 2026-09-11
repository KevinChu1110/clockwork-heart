from PIL import Image
import numpy as np

im = Image.open('screenshots/proof_battle_macaque_full_screen.png').convert('RGBA')
arr = np.array(im)

# Let's find player_body position: in battle_view, player_body is in player_card or battle view
# Let's inspect differences or find non-background pixels in left half
# Or let's just inspect where player_body is:
# In battle_view.gd: player_body position
# Let's write a script to search for green core pixel (RGB around 30, 200, 180 or similar)
for y in range(100, 600, 5):
    for x in range(100, 600, 5):
        r, g, b, a = arr[y, x]
        if g > 150 and b > 150 and r < 80:
            print(f"Found emerald core near x={x}, y={y}: RGB=({r},{g},{b})")
            break
