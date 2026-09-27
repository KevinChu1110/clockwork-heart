import os
import glob
from PIL import Image

for f in sorted(glob.glob("tools/build_official_assets_*.py")):
    race = f.replace("tools/build_official_assets_", "").replace(".py", "")
    with open(f, "r") as fp:
        code = fp.read()
    if "showcase_hd" in code or "sh_scale" in code or "SHOWCASE" in code:
        # extract lines around sh_scale
        lines = code.splitlines()
        for i, l in enumerate(lines):
            if "sh_scale =" in l or "scale_showcase" in l or "SHOWCASE_DIR" in l:
                print(f"[{race}] line {i}: {l.strip()}")
                for j in range(max(0, i-2), min(len(lines), i+12)):
                    if any(k in lines[j] for k in ["sh_scale", "scale", "sc_w", "sc_h", "paste", "showcase_hd", "resize"]):
                        print(f"   {lines[j].strip()}")
                break
