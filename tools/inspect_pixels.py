import numpy as np
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/proofs/web_thirteen_races/proof_web_new_races_detail.png")
arr = np.array(im)
print("Min:", arr.min(axis=(0,1)), "Max:", arr.max(axis=(0,1)), "Mean:", arr.mean(axis=(0,1)))
print("Unique colors count approx:", len(np.unique(arr.reshape(-1, arr.shape[2]), axis=0)))
