from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/rabbit_idle_x3.png").convert("RGBA")
# Let's inspect the sword in rabbit_idle_x3 from (30, 70) to (95, 125)
w, h = idle.size
data = idle.load()

# Print the sword in rabbit_idle_x3
print("=== Sword in rabbit_idle_x3.png ===")
for y in range(70, 125):
    line = ""
    for x in range(34, 92):
        r, g, b, a = data[x, y]
        if a == 0:
            line += " "
        elif (r, g, b) == (44, 28, 22) or (r, g, b) == (34, 20, 16):
            line += "#" # Outline
        elif r > 220 and g > 220 and b > 220:
            line += "W" # White blade highlight
        elif r > 180 and g > 180 and b > 180:
            line += "s" # Silver steel
        elif r > 180 and g > 140 and b < 100:
            line += "G" # Gold
        elif r > 100 and g > 70 and b < 50:
            line += "g" # Dark gold
        elif b > r and b > g:
            line += "B" # Blue / steel shadow
        elif r < 80 and g < 80 and b < 80:
            line += "D" # Dark shadow
        else:
            line += "."
    print(f"y={y:2d}: {line}")
