# Add test at end of craft_macaque_attack_perfect.py
with open("/opt/side/bravesoul-game/tools/craft_macaque_attack_perfect.py", "r") as f:
    text = f.read()

text = text.replace("from sim_attack_screen import test_sim", "print('Finished crafting.')")
with open("/opt/side/bravesoul-game/tools/craft_macaque_attack_perfect.py", "w") as f:
    f.write(text)
