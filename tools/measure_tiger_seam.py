import numpy as np
from PIL import Image

def analyze(path):
    img = Image.open(path).convert('RGBA')
    arr = np.array(img, dtype=np.float32)
    print(f"=== Analyzing {path} ===")
    for y in range(205, 230):
        row1 = arr[y]
        row2 = arr[y+1]
        mask = (row1[:, 3] > 200) & (row2[:, 3] > 200)
        width = int(np.sum(mask))
        if width > 0:
            diff_euc = np.sqrt(np.sum((row1[mask, :3] - row2[mask, :3])**2, axis=-1))
            mean_euc = float(np.mean(diff_euc))
            mean_abs = float(np.mean(np.abs(row1[mask, :3] - row2[mask, :3])))
            print(f"y={y:3d} -> y+1: width={width:3d}, euc={mean_euc:5.2f}, abs={mean_abs:5.2f}")

    print("\nChecking with step 2 (e.g. y vs y+2):")
    for y in range(205, 230, 2):
        row1 = arr[y]
        row2 = arr[y+2]
        mask = (row1[:, 3] > 200) & (row2[:, 3] > 200)
        width = int(np.sum(mask))
        if width > 0:
            diff_euc = np.sqrt(np.sum((row1[mask, :3] - row2[mask, :3])**2, axis=-1))
            mean_euc = float(np.mean(diff_euc))
            mean_abs = float(np.mean(np.abs(row1[mask, :3] - row2[mask, :3])))
            print(f"y={y:3d} -> y+2: width={width:3d}, euc={mean_euc:5.2f}, abs={mean_abs:5.2f}")

if __name__ == '__main__':
    analyze('game/assets/sprites/player/paperdoll/tiger/head_unit/head_ember_tiger_stock_512.png')
