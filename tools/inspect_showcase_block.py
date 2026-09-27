import glob

for f in sorted(glob.glob("tools/build_official_assets_*.py")):
    race = f.replace("tools/build_official_assets_", "").replace(".py", "")
    with open(f, "r") as fp:
        lines = fp.readlines()
    for i, line in enumerate(lines):
        if "showcase_hd = " in line:
            print(f"=== {race} ===")
            for k in range(i, min(len(lines), i + 25)):
                print(f"{k+1}: {lines[k].rstrip()}")
