from PIL import Image

im = Image.open('/tmp/chassis_zoom.png')
print("chassis_zoom.png size:", im.size, "mode:", im.mode)
