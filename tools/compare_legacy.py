import numpy as np
from PIL import Image

legacy_128 = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/proof_paperdoll_lion_composite.png')
new_512 = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/lion_maple_test_comp.png')
new_128 = new_512.resize((128, 128), Image.Resampling.LANCZOS)

diff = np.abs(np.array(legacy_128).astype(int) - np.array(new_128).astype(int))
print("Diff max:", diff.max(), "mean:", diff.mean())
# pixels where diff is significant (> 20)
sig_diff = np.any(diff > 20, axis=2)
print("Significant diff pixels count:", np.sum(sig_diff))

new_128.save('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/lion_maple_128.png')
