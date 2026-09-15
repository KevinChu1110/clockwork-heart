import os

workdir = "/opt/side/bravesoul-game"
missing_dest = []
missing_path = []
total = 0

for root, dirs, files in os.walk(os.path.join(workdir, "game")):
    for f in files:
        if f.endswith(".import"):
            total += 1
            full_path = os.path.join(root, f)
            rel = os.path.relpath(full_path, workdir)
            with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                txt = fp.read()
            if "dest_files=" not in txt:
                missing_dest.append(rel)
            if 'type="CompressedTexture2D"' in txt and "path=" not in txt:
                missing_path.append(rel)

print(f"Total .import files: {total}")
print(f"Missing dest_files ({len(missing_dest)}):")
for p in missing_dest:
    print(f"  {p}")

print(f"\nMissing path ({len(missing_path)}):")
for p in missing_path:
    print(f"  {p}")
