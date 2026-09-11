import os

for f in os.listdir("game/.godot/imported"):
    if "attack.png" in f:
        p = os.path.join("game/.godot/imported", f)
        os.remove(p)
        print("Removed:", p)
