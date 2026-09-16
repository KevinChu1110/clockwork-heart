#!/usr/bin/env python3
"""
tools/build_penguin_polar_chassis.py
Constructs paint_polar_frost.png and paint_ivory_stock.png for The Steam Penguin chassis.
Delegates to tools/build_all_penguin_chassis.py for 100% CANON and 0-ART18 compliance.
"""

import sys
if "/opt/side/bravesoul-game" not in sys.path:
    sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.build_all_penguin_chassis import main as build_all

if __name__ == "__main__":
    build_all()
