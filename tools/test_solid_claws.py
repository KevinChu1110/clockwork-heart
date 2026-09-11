import os
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"

C_OUTLINE = (35, 22, 18, 255)
C_BRASS_HI = (255, 225, 80, 255)
C_BRASS_MID = (215, 160, 30, 255)
C_BRASS_SHAD = (145, 95, 18, 255)

C_STEEL_SPEC = (255, 255, 250, 255)
C_STEEL_HI = (235, 235, 240, 255)
C_STEEL_MID = (180, 185, 195, 255)
C_STEEL_SHAD = (110, 115, 130, 255)
C_STEEL_DARK = (65, 68, 80, 255)

def craft_attack_pose() -> tuple[Image.Image, Image.Image]:
    base_atk = Image.open("/tmp/attack_base.png").convert("RGBA")
    wep_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    wep_px = wep_layer.load()
    assert wep_px is not None

    # 1. Rear hand at waist (x=28..38, y=68..80) - approved from attempt 2
    draw = ImageDraw.Draw(wep_layer)
    draw.rectangle([28, 69, 37, 78], fill=C_BRASS_MID, outline=C_OUTLINE)
    draw.line([29, 70, 36, 70], fill=C_BRASS_HI)
    draw.line([29, 77, 36, 77], fill=C_BRASS_SHAD)
    draw.polygon([(28, 71), (28, 73), (20, 70)], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw.polygon([(28, 74), (28, 76), (19, 74)], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw.polygon([(28, 77), (28, 79), (20, 78)], fill=C_STEEL_HI, outline=C_OUTLINE)

    # 2. Forward punching gauntlet base (x=84..100, y=52..67)
    draw.rectangle([84, 52, 100, 67], fill=C_BRASS_MID, outline=C_OUTLINE)
    draw.line([85, 53, 99, 53], fill=C_BRASS_HI)
    draw.line([85, 66, 99, 66], fill=C_BRASS_SHAD)
    # Clockwork spring chamber
    draw.rectangle([88, 56, 95, 63], fill=C_STEEL_MID, outline=C_OUTLINE)
    draw.line([91, 57, 91, 62], fill=C_STEEL_SPEC)
    # Brass claw mounting sockets at front of fist
    draw.rectangle([98, 51, 102, 56], fill=C_BRASS_HI, outline=C_OUTLINE)
    draw.rectangle([98, 57, 103, 62], fill=C_BRASS_HI, outline=C_OUTLINE)
    draw.rectangle([98, 63, 102, 68], fill=C_BRASS_HI, outline=C_OUTLINE)

    # 3. Solid Metal Forward Claw Blades (Thick, continuous, highlighted, shaded, tapered)
    # Upper Claw (x=100..120)
    for x in range(100, 107):
        wep_px[x, 52] = C_OUTLINE
        wep_px[x, 53] = C_STEEL_SPEC
        wep_px[x, 54] = C_STEEL_HI
        wep_px[x, 55] = C_OUTLINE
    for x in range(107, 113):
        wep_px[x, 51] = C_OUTLINE
        wep_px[x, 52] = C_STEEL_SPEC
        wep_px[x, 53] = C_STEEL_HI
        wep_px[x, 54] = C_OUTLINE
    for x in range(113, 118):
        wep_px[x, 51] = C_STEEL_SPEC
        wep_px[x, 52] = C_STEEL_HI
        wep_px[x, 53] = C_OUTLINE
    for x in range(118, 121):
        wep_px[x, 51] = C_STEEL_SPEC
        wep_px[x, 52] = C_OUTLINE

    # Middle Claw (x=100..122) - main center thrust blade
    for x in range(100, 107):
        wep_px[x, 57] = C_OUTLINE
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_STEEL_HI
        wep_px[x, 60] = C_STEEL_SHAD
        wep_px[x, 61] = C_OUTLINE
    for x in range(107, 115):
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_STEEL_HI
        wep_px[x, 60] = C_STEEL_SHAD
        wep_px[x, 61] = C_OUTLINE
    for x in range(115, 120):
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_STEEL_HI
        wep_px[x, 60] = C_OUTLINE
    for x in range(120, 123):
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_OUTLINE

    # Lower Claw (x=100..120)
    for x in range(100, 107):
        wep_px[x, 63] = C_OUTLINE
        wep_px[x, 64] = C_STEEL_SPEC
        wep_px[x, 65] = C_STEEL_HI
        wep_px[x, 66] = C_OUTLINE
    for x in range(107, 113):
        wep_px[x, 64] = C_OUTLINE
        wep_px[x, 65] = C_STEEL_SPEC
        wep_px[x, 66] = C_STEEL_HI
        wep_px[x, 67] = C_OUTLINE
    for x in range(113, 118):
        wep_px[x, 65] = C_OUTLINE
        wep_px[x, 66] = C_STEEL_SPEC
        wep_px[x, 67] = C_OUTLINE
    for x in range(118, 121):
        wep_px[x, 66] = C_STEEL_SPEC
        wep_px[x, 67] = C_OUTLINE

    comp = base_atk.copy()
    comp.alpha_composite(wep_layer)
    return comp, wep_layer

if __name__ == "__main__":
    comp, wep = craft_attack_pose()
    comp.save("/tmp/test_attack_solid.png")
    wep.save("/tmp/test_wep_layer.png")
    print("Comp bbox:", comp.getbbox())
    print("Wep bbox:", wep.getbbox())

    comp_px = comp.load()
    assert comp_px is not None
    print("=== Column runs in x=102..124 ===")
    all_runs_ge_2 = True
    for x in range(102, 124):
        ys = [y for y in range(128) if comp_px[x, y][3] > 10]
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
        if any(l < 2 for l in run_lens):
            all_runs_ge_2 = False
        print(f"x={x}: ys={ys}, runs={run_lens}")
    print("All runs >= 2:", all_runs_ge_2)
