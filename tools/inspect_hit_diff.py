from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
hit_img = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/cat/hit.png")
idle_img = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/cat/idle.png")

print("Hit bbox:", hit_img.getbbox())
print("Idle bbox:", idle_img.getbbox())

# Let's inspect where hit_img differs from idle_img
diff = np.abs(np.array(hit_img).astype(int) - np.array(idle_img).astype(int))
print("Diff pixels:", np.sum(np.any(diff > 0, axis=-1)))
ys, xs = np.where(np.any(diff > 0, axis=-1))
print(f"Diff x range: {xs.min()}..{xs.max()}, y range: {ys.min()}..{ys.max()}")

# Let's save a visual diff image
diff_img = Image.fromarray(np.clip(diff * 5, 0, 255).astype(np.uint8))
diff_img.save(f"{REPO_ROOT}/tools/diff_hit_idle.png")
print("Saved diff_hit_idle.png")
