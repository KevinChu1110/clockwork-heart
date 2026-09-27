from PIL import Image

img = Image.open('game/assets/sprites/player/showcase/hedgehog_idle_hd.png')
# Crop the region around x=0..100, y=500..800
crop1 = img.crop((0, 520, 150, 780))
crop1.save('proofs/hedgehog_left_edge_before.png')

# Also check right edge: BBox X was 0..799
# Let's inspect x=780..800
crop2 = img.crop((700, 500, 800, 800))
crop2.save('proofs/hedgehog_right_edge.png')
print("Saved crops.")
