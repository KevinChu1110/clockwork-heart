import numpy as np

# Let's test the math on the 4 races' idle weapon pixels!
from PIL import Image

races = {
    "rabbit": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png",
        "box": (60, 70, 80, 96),
    },
    "lion": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/idle.png",
        "box": (38, 85, 55, 116),
    },
    "fox": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png",
        "box": (35, 58, 48, 72),
    },
    "boar": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/idle.png",
        "box": (38, 75, 55, 105),
    }
}

# Let's extract source silver pixels for each race:
race_pixels = {}
for rname, rdata in races.items():
    im = Image.open(rdata["file"]).convert("RGBA")
    bx0, by0, bx1, by1 = rdata["box"]
    pts = []
    for y in range(by0, by1 + 1):
        for x in range(bx0, bx1 + 1):
            r, g, b, a = im.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                pts.append((r, g, b))
    race_pixels[rname] = pts
    print(f"{rname}: {len(pts)} weapon silver pixels in source")

# Now let's test different shader configurations:
def run_shader_on_pixels(pixels, sat=1.08, con=1.08, bri=1.03, hl_protect=True):
    silvers = 0
    browns = 0
    outs = []
    for r, g, b in pixels:
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
        # Contrast
        rf = (rf - 0.5) * con + 0.5
        gf = (gf - 0.5) * con + 0.5
        bf = (bf - 0.5) * con + 0.5
        # Brightness
        rf *= bri
        gf *= bri
        bf *= bri
        luma = rf * 0.2126 + gf * 0.7152 + bf * 0.0722
        
        cur_sat = sat
        if hl_protect:
            # smooth rolloff for highlights
            # above luma 0.75, reduce extra saturation
            t = np.clip((luma - 0.70) / (0.95 - 0.70), 0.0, 1.0)
            cur_sat = sat * (1.0 - t) + 1.0 * t
            
        rf = luma + (rf - luma) * cur_sat
        gf = luma + (gf - luma) * cur_sat
        bf = luma + (bf - luma) * cur_sat
        
        out_r = np.clip(rf, 0.0, 1.0) * 255.0
        out_g = np.clip(gf, 0.0, 1.0) * 255.0
        out_b = np.clip(bf, 0.0, 1.0) * 255.0
        outs.append((out_r, out_g, out_b))
        
        if out_r > 185 and out_g > 185 and out_b > 185 and abs(out_r - out_b) < 40:
            silvers += 1
        if out_r - out_b > 50:
            browns += 1
    
    n = len(pixels)
    return silvers / n * 100.0, browns / n * 100.0, np.mean(outs, axis=0)

print("\n--- Testing without highlight protection (pure parameter tuning) ---")
for s in [1.22, 1.10, 1.08, 1.05, 1.02, 1.00]:
    for c in [1.12, 1.08, 1.05]:
        for b in [1.05, 1.03, 1.01]:
            passed = True
            for rname in ["rabbit", "lion", "fox", "boar"]:
                silv_pct, brn_pct, avg_rgb = run_shader_on_pixels(race_pixels[rname], sat=s, con=c, bri=b, hl_protect=False)
                if silv_pct < 70.0 or brn_pct > 15.0:
                    passed = False
                    break
            if passed:
                print(f"PASS pure params: sat={s:.2f}, con={c:.2f}, bri={b:.2f}")
                for rname in ["rabbit", "lion", "fox", "boar"]:
                    s_p, b_p, avg = run_shader_on_pixels(race_pixels[rname], sat=s, con=c, bri=b, hl_protect=False)
                    print(f"  {rname}: silver={s_p:.1f}%, brown={b_p:.1f}%, avg=({avg[0]:.1f}, {avg[1]:.1f}, {avg[2]:.1f})")
                break
        if passed:
            break
    if passed:
        break

print("\n--- Testing with highlight protection ---")
for s in [1.10, 1.08, 1.06]:
    passed = True
    for rname in ["rabbit", "lion", "fox", "boar"]:
        silv_pct, brn_pct, avg_rgb = run_shader_on_pixels(race_pixels[rname], sat=s, con=1.08, bri=1.03, hl_protect=True)
        if silv_pct < 70.0 or brn_pct > 15.0:
            passed = False
            break
    if passed:
        print(f"PASS with hl_protect: sat={s:.2f}, con=1.08, bri=1.03")
        for rname in ["rabbit", "lion", "fox", "boar"]:
            s_p, b_p, avg = run_shader_on_pixels(race_pixels[rname], sat=s, con=1.08, bri=1.03, hl_protect=True)
            print(f"  {rname}: silver={s_p:.1f}%, brown={b_p:.1f}%, avg=({avg[0]:.1f}, {avg[1]:.1f}, {avg[2]:.1f})")
        break
