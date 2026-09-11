from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png")
pix = im.load()
bbox = im.getbbox()
print("wpn_spring_claws bbox:", bbox)
count = 0
for y in range(im.height):
    for x in range(im.width):
        if pix[x, y][3] > 0:
            count += 1
print("Non-transparent pixels:", count)

# Look at left gauntlet claw blades (cx=30, cy=78..102)
print("=== Claw blades on left gauntlet (x: 20..42, y: 78..102) ===")
for y in range(78, 102):
    xs = [x for x in range(20, 42) if pix[x, y][3] > 10]
    if xs:
        print(f"y={y}: xs={xs}, width={len(xs)}")
