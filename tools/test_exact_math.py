def test_shader(r, g, b, sat=1.22, con=1.12, bri=1.05):
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    # Line 10:
    rf = (rf - 0.5) * con + 0.5
    gf = (gf - 0.5) * con + 0.5
    bf = (bf - 0.5) * con + 0.5
    # Line 11:
    rf *= bri
    gf *= bri
    bf *= bri
    # Line 12:
    luma = rf * 0.2126 + gf * 0.7152 + bf * 0.0722
    # Line 13:
    rf = luma + (rf - luma) * sat
    gf = luma + (gf - luma) * sat
    bf = luma + (bf - luma) * sat
    # Line 14:
    out_r = min(1.0, max(0.0, rf)) * 255.0
    out_g = min(1.0, max(0.0, gf)) * 255.0
    out_b = min(1.0, max(0.0, bf)) * 255.0
    return out_r, out_g, out_b

print("Original: (244, 235, 212), r-b =", 244 - 212)
r, g, b = test_shader(244, 235, 212, sat=1.22, con=1.12, bri=1.05)
print(f"Default Shader (1.22, 1.12, 1.05): ({r:.1f}, {g:.1f}, {b:.1f}), r-b = {r-b:.1f}")
