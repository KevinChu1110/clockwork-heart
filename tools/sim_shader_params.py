import numpy as np

# Let's take the 276 blade pixels from rabbit
# When grade is OFF: avg RGB is (235, 227, 206)
# If a pixel has RGB (235, 227, 206):
# Let's test different shader parameters:

def shader_sim(rgb, sat, con, bri):
    rgb = (rgb - 0.5) * con + 0.5
    rgb = rgb * bri
    luma = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    rgb = luma + (rgb - luma) * sat
    return np.clip(rgb, 0.0, 1.0) * 255.0

# Typical blade RGBs from idle.png
sample_pixels = [
    (235, 227, 206),
    (240, 230, 210),
    (230, 225, 205),
    (225, 220, 200),
    (245, 238, 218),
    (210, 205, 195),
    (250, 245, 225),
    (238, 232, 212),
]

for sat in [1.22, 1.15, 1.10, 1.08, 1.05, 1.03, 1.00]:
    for con in [1.12, 1.10, 1.08, 1.05]:
        for bri in [1.05, 1.03, 1.02, 1.00]:
            silvers = 0
            browns = 0
            out_rgbs = []
            for p in sample_pixels:
                p_norm = np.array(p) / 255.0
                out = shader_sim(p_norm, sat, con, bri)
                out_rgbs.append(out)
                r, g, b = out
                if r > 185 and g > 185 and b > 185 and abs(r - b) < 40:
                    silvers += 1
                if r - b > 50:
                    browns += 1
            if silvers >= len(sample_pixels) * 0.7 and browns == 0:
                avg = np.mean(out_rgbs, axis=0)
                print(f"sat={sat:.2f}, con={con:.2f}, bri={bri:.2f} -> silver: {silvers}/{len(sample_pixels)}, brown: {browns}, avg RGB: ({avg[0]:.1f}, {avg[1]:.1f}, {avg[2]:.1f})")
                break
        if silvers >= len(sample_pixels) * 0.7 and browns == 0:
            break
