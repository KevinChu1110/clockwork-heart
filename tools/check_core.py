from PIL import Image
import numpy as np

for slot, p in [
    ("chassis", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/penguin/chassis/paint_penguin_navy_512.png"),
    ("head", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_stock_512.png"),
    ("core", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/penguin/optic_core/core_cyan_quartz_512.png"),
    ("abyssal", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/penguin/costume/costume_abyssal_diver_cuirass_512.png"),
]:
    im = Image.open(p)
    arr = np.array(im)
    print(f"{slot}: shape={arr.shape}")
    # check where alpha > 10 in core
    if slot == "core":
        nz = np.nonzero(arr[:, :, 3] > 10)
        # print y ranges
        print("core y range:", nz[0].min(), nz[0].max())
        # print if there is eye part or chest part
        y_vals = nz[0]
        print(f"core has y < 180: {np.any(y_vals < 180)}, y >= 180: {np.any(y_vals >= 180)}")
