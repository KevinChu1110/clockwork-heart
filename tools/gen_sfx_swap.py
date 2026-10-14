#!/usr/bin/env python3
"""
合成 swap.wav（換欄那一拍的「金屬卡榫」）。

2026-10（issue #32）起，swap 跟 hit／slash／break／warn／wind 一起改由
`tools/gen_sfx_clockwork.py` 合成（同一套響度正規化：M-max −20 LUFS、true peak ≤ −1 dBTP）。
這支只是相容入口，保留舊用法：

  python3 tools/gen_sfx_swap.py            # 寫 game/assets/audio/sfx/swap.wav
  python3 tools/gen_sfx_swap.py --out x.wav
跑完要 `godot --path game --headless --import` 一次。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_sfx_clockwork as gc  # noqa: E402

OUT = gc.SFX_DIR / "swap.wav"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    x = gc.render("swap")
    gc.write_wav(Path(a.out), x)
    x16, _ = gc.read_wav(Path(a.out))
    print("wrote", a.out, gc.report("swap", x16))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
