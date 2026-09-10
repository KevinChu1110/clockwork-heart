import os
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"

# Color palette matching character's metal & outline
C_OUTLINE = (35, 22, 18, 255)
C_OUTLINE_SOFT = (45, 30, 24, 180)
C_OUTLINE_LIGHT = (60, 42, 32, 120)

C_BRASS_HI = (255, 225, 80, 255)
C_BRASS_MID = (215, 160, 30, 255)
C_BRASS_SHAD = (145, 95, 18, 255)
C_BRASS_DARK = (95, 60, 12, 255)

# Multi-layered steel reflections
C_STEEL_SPEC = (255, 255, 250, 255)
C_STEEL_HI = (235, 238, 245, 255)
C_STEEL_MID = (185, 190, 205, 255)
C_STEEL_SHAD = (120, 125, 140, 255)
C_STEEL_DARK = (75, 78, 90, 255)

def build_attack_pose_with_claws() -> tuple[Image.Image, Image.Image]:
    base_atk = Image.open("/tmp/attack_base.png").convert("RGBA")
    wep_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    wep_px = wep_layer.load()
    assert wep_px is not None

    draw_wep = ImageDraw.Draw(wep_layer)

    # 1. Rear hand at waist (x=28..38, y=68..80) - approved
    draw_wep.rectangle([28, 69, 37, 78], fill=C_BRASS_MID, outline=C_OUTLINE)
    draw_wep.line([29, 70, 36, 70], fill=C_BRASS_HI)
    draw_wep.line([29, 77, 36, 77], fill=C_BRASS_SHAD)
    draw_wep.polygon([(28, 71), (28, 73), (20, 70)], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw_wep.polygon([(28, 74), (28, 76), (19, 74)], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw_wep.polygon([(28, 77), (28, 79), (20, 78)], fill=C_STEEL_HI, outline=C_OUTLINE)

    # 2. Forward punching gauntlet base (x=84..101, y=52..67)
    draw_wep.rectangle([84, 52, 100, 67], fill=C_BRASS_MID, outline=C_OUTLINE)
    draw_wep.line([85, 53, 99, 53], fill=C_BRASS_HI)
    draw_wep.line([85, 66, 99, 66], fill=C_BRASS_SHAD)
    # Clockwork spring chamber
    draw_wep.rectangle([88, 56, 95, 63], fill=C_STEEL_MID, outline=C_OUTLINE)
    draw_wep.line([91, 57, 91, 62], fill=C_STEEL_SPEC)
    # Brass claw mounting sockets at front of fist
    draw_wep.rectangle([98, 51, 102, 56], fill=C_BRASS_HI, outline=C_OUTLINE)
    draw_wep.rectangle([98, 57, 103, 62], fill=C_BRASS_HI, outline=C_OUTLINE)
    draw_wep.rectangle([98, 63, 102, 68], fill=C_BRASS_HI, outline=C_OUTLINE)

    # 3. Solid Metal Forward Claw Blades (Rule 0b-6 compliant)
    # -------------------------------------------------------------------------
    # Upper Claw (x=100..120, max tip at 120, height 4px -> 2px)
    for x in range(100, 107):
        wep_px[x, 52] = C_OUTLINE
        wep_px[x, 53] = C_STEEL_SPEC
        wep_px[x, 54] = C_STEEL_HI
        wep_px[x, 55] = C_OUTLINE
    for x in range(107, 114):
        wep_px[x, 51] = C_OUTLINE
        wep_px[x, 52] = C_STEEL_SPEC
        wep_px[x, 53] = C_STEEL_HI
        wep_px[x, 54] = C_OUTLINE
    for x in range(114, 119):
        wep_px[x, 51] = C_STEEL_SPEC
        wep_px[x, 52] = C_STEEL_HI
        wep_px[x, 53] = C_OUTLINE
    for x in range(119, 121):
        wep_px[x, 51] = C_STEEL_SPEC
        wep_px[x, 52] = C_OUTLINE
    # Tapered anti-aliased tip
    wep_px[120, 51] = (245, 248, 255, 200)
    wep_px[120, 52] = (45, 30, 24, 210)
    wep_px[106, 51] = C_OUTLINE_SOFT
    wep_px[113, 50] = C_OUTLINE_LIGHT

    # Middle Claw (x=100..122, max tip at 122, height 5px -> 2px)
    for x in range(100, 107):
        wep_px[x, 57] = C_OUTLINE
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_STEEL_HI
        wep_px[x, 60] = C_STEEL_SHAD
        wep_px[x, 61] = C_OUTLINE
    for x in range(107, 116):
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_STEEL_HI
        wep_px[x, 60] = C_STEEL_SHAD
        wep_px[x, 61] = C_OUTLINE
    for x in range(116, 121):
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_STEEL_HI
        wep_px[x, 60] = C_OUTLINE
    for x in range(121, 123):
        wep_px[x, 58] = C_STEEL_SPEC
        wep_px[x, 59] = C_OUTLINE
    # Tapered anti-aliased tip
    wep_px[122, 58] = (245, 248, 255, 200)
    wep_px[122, 59] = (45, 30, 24, 210)
    wep_px[106, 57] = C_OUTLINE_SOFT
    wep_px[115, 61] = C_OUTLINE_SOFT

    # Lower Claw (x=100..120, max tip at 120, height 4px -> 2px)
    for x in range(100, 107):
        wep_px[x, 63] = C_OUTLINE
        wep_px[x, 64] = C_STEEL_SPEC
        wep_px[x, 65] = C_STEEL_HI
        wep_px[x, 66] = C_OUTLINE
    for x in range(107, 114):
        wep_px[x, 64] = C_OUTLINE
        wep_px[x, 65] = C_STEEL_SPEC
        wep_px[x, 66] = C_STEEL_HI
        wep_px[x, 67] = C_OUTLINE
    for x in range(114, 119):
        wep_px[x, 65] = C_OUTLINE
        wep_px[x, 66] = C_STEEL_SPEC
        wep_px[x, 67] = C_OUTLINE
    for x in range(119, 121):
        wep_px[x, 66] = C_STEEL_SPEC
        wep_px[x, 67] = C_OUTLINE
    # Tapered anti-aliased tip
    wep_px[120, 66] = (245, 248, 255, 200)
    wep_px[120, 67] = (45, 30, 24, 210)
    wep_px[106, 67] = C_OUTLINE_SOFT
    wep_px[113, 68] = C_OUTLINE_LIGHT

    # Composite weapon layer onto base attack pose
    comp = base_atk.copy()
    comp.alpha_composite(wep_layer)
    return comp, wep_layer

if __name__ == "__main__":
    comp, wep = build_attack_pose_with_claws()
    target_path = f"{REPO_ROOT}/game/assets/sprites/player/poses/macaque/attack.png"
    comp.save(target_path)
    print("Successfully saved to:", target_path)
    print("Comp bbox:", comp.getbbox())
    print("Wep bbox:", wep.getbbox())

    comp_px = comp.load()
    assert comp_px is not None
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
    print("All runs >= 2 in x=102..122:", all_runs_ge_2)
