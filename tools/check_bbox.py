from PIL import Image
for i in range(8):
    path = f'/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_0{i}.png'
    im = Image.open(path)
    print(f'frame {i}: bbox = {im.getbbox()}, size = {im.size}')
