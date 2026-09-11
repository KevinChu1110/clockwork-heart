from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png")
# Crop hand and weapon area (x: 80..125, y: 48..75)
crop = im.crop((80, 48, 125, 75))
crop_16x = crop.resize((crop.width * 16, crop.height * 16), Image.Resampling.NEAREST)
out_path = "/opt/side/bravesoul-game/screenshots/proof_battle_macaque_attack_hand_weapon_crop_16x.png"
crop_16x.save(out_path)
print("Saved:", out_path, "size:", crop_16x.size)

# Also check column runs for x=102..124
pix = im.load()
print("=== Column runs in x=102..124 ===")
for x in range(102, 124):
    ys = [y for y in range(128) if pix[x, y][3] > 10]
    runs = []
    if ys:
        cur = [ys[0]]
        for y in ys[1:]:
            if y == cur[-1] + 1:
                cur.append(y)
            else:
                runs.append(cur)
                cur = [y]
        runs.append(cur)
    run_lens = [len(r) for r in runs]
    print(f"x={x}: ys={ys}, runs={run_lens}")
