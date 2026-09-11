from PIL import Image

im = Image.open("/root/tmp_workspace/debug_raw_2_5s.png")
# PlayerSlot in 1280x720 is around x: 180~420, y: 220~520
player_crop = im.crop((180, 220, 420, 520))
player_crop.save("/root/tmp_workspace/player_standalone_crop.png")
print("Cropped player to /root/tmp_workspace/player_standalone_crop.png, size:", player_crop.size)
