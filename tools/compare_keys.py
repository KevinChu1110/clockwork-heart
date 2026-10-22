#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

macaque_key_128 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png")
lion_key = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts/winding_key/key_classic_brass.png")
boar_key = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png")

print("Macaque key 128 bbox:", macaque_key_128.getbbox())
print("Lion key size:", lion_key.size, "bbox:", lion_key.getbbox())
print("Boar key size:", boar_key.size, "bbox:", boar_key.getbbox())
