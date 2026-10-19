#!/usr/bin/env python3
import os

p = "/opt/side/bravesoul-game/game/scripts/art/test_maple_paperdoll_macaque.gd"
if os.path.exists(p):
    os.remove(p)
    print("Removed test_maple_paperdoll_macaque.gd")
