from PIL import Image, ImageChops

im_idle = Image.open("/tmp/rabbit_frames/frame_030.png")
im_atk = Image.open("/tmp/rabbit_frames/frame_060.png")
im_hit = Image.open("/tmp/rabbit_frames/frame_072.png")
im_brk = Image.open("/tmp/rabbit_frames/frame_085.png")

diff_atk = ImageChops.difference(im_idle, im_atk)
diff_hit = ImageChops.difference(im_idle, im_hit)
diff_brk = ImageChops.difference(im_idle, im_brk)

print("Idle vs Attack diff bbox:", diff_atk.getbbox())
print("Idle vs Hit diff bbox:", diff_hit.getbbox())
print("Idle vs Break diff bbox:", diff_brk.getbbox())

# 裁剪角色位移對照
c_idle = im_idle.crop((160, 160, 520, 480))
c_atk = im_atk.crop((160, 160, 520, 480))
diff_char = ImageChops.difference(c_idle, c_atk)
print("Character area diff bbox:", diff_char.getbbox())
