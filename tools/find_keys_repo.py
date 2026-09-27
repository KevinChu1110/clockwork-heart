import os

keys = ["cream", "brass_vest", "scarf_tunic", "worker_apron", "enamel_chip", "spring_coil", "core_shard"]
for root, dirs, files in os.walk("/opt/side/bravesoul-game"):
    if ".git" in root:
        continue
    for file in files:
        if file.endswith((".gd", ".json", ".md", ".tscn")):
            p = os.path.join(root, file)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    txt = f.read()
                    for k in keys:
                        if k in txt:
                            print(f"{k} in {p}")
            except:
                pass
