#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

head = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
# 裁出眼窩周圍 (210, 140, 260, 180)
eye_sock = head.crop((210, 140, 260, 180))
eye_sock.save("/tmp/boar_eye_socket_brass.png")
print("Saved /tmp/boar_eye_socket_brass.png")
