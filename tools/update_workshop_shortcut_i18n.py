import os

path = "/opt/side/bravesoul-game/game/scripts/ui/test_verify_gem_dlg.gd"
if os.path.exists(path):
    os.remove(path)
    print("Removed temporary test script", path)
