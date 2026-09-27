from PIL import Image

p512 = "game/assets/sprites/player/paperdoll/hedgehog"
curio = Image.open(f"{p512}/back_curio/curio_hedgehog_spring_steel_quill_pack_512.png")
bbox = curio.getbbox()
print("Curio bbox:", bbox)

# Let's crop the leftmost quills of curio: x=40..100, y=150..300
crop_curio = curio.crop((35, 150, 110, 320))
crop_curio.save("proofs/curio_quills_crop.png")
