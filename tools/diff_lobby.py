from PIL import Image
import numpy as np

before = Image.open("proofs/exploratory_qa_t_e6bc1e6c/proof_crop_lobby_hedgehog.png")
now = Image.open("proofs/test_lobby_crop_now.png")

diff = np.sum(np.abs(np.array(before).astype(int) - np.array(now).astype(int)))
print(f"Difference between before and now: {diff}")
