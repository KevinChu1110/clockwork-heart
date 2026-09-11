from PIL import Image

im128 = Image.open("/tmp/aligned_shadow_comp_navy.png").convert("RGBA")

# 1. Bilinear stretch directly to 210x210 (simulating Godot's current linear filter on 128x128)
stretch_bilinear = im128.resize((210, 210), getattr(Image, 'Resampling', Image).BILINEAR)
stretch_bilinear.save("/tmp/res_stretch_bilinear.png")

# 2. Lanczos 2x upscale to 256x256, then crisp display
lanczos_2x = im128.resize((256, 256), getattr(Image, 'Resampling', Image).LANCZOS)
lanczos_2x.save("/tmp/res_lanczos_2x.png")

# 3. Nearest 2x upscale to 256x256 (pure crisp pixel art presentation)
nearest_2x = im128.resize((256, 256), getattr(Image, 'Resampling', Image).NEAREST)
nearest_2x.save("/tmp/res_nearest_2x.png")

# 4. In wardrobe_dialog: stage panel is 250x360.
# If _preview_rect is 256x256 (or 210x210) displaying the 2x texture with linear filter:
preview_render = lanczos_2x.resize((210, 210), getattr(Image, 'Resampling', Image).BILINEAR)
preview_render.save("/tmp/res_preview_supersampled.png")

print("Saved comparison images!")
