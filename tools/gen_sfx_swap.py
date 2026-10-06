#!/usr/bin/env python3
"""
合成占位音效 swap.wav（換欄那一拍的「金屬卡榫」）。

【占位】這是 numpy 合成的暫用檔，正式版要換成真錄的金屬卡榫／彈簧扣。
規格（docs/CLOCKWORK_ART_MUSIC_BRIEF.md §5）：短、乾淨、≤0.3 秒、一次性不循環。

聲音結構：
  1. 第一下「喀」：極短雜訊瞬態 + 高頻非諧波金屬共振（快衰減）
  2. 約 55ms 後第二下「嗒」：卡榫扣進去，音高略低、帶一點低頻機身
  3. 結尾 15ms 淡出，避免尾巴爆音

用法
  python3 tools/gen_sfx_swap.py            # 寫 game/assets/audio/sfx/swap.wav
  python3 tools/gen_sfx_swap.py --out x.wav
跑完要 `godot --path game --headless --import` 一次。
"""
from __future__ import annotations

import argparse
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "game" / "assets" / "audio" / "sfx" / "swap.wav"
SR = 22050          # 與其他 sfx 一致（22.05k mono 16-bit）
DUR = 0.22          # 秒，規格上限 0.3
PEAK_DBFS = -5.0    # 介於 hit(-4) 與 slash(-8) 之間，不蓋過跳字瞬間


def _click(t: np.ndarray, t0: float, partials: list[tuple[float, float, float]],
           noise_amp: float, rng: np.random.Generator) -> np.ndarray:
    """t0 起的一下金屬敲擊：partials = [(頻率, 振幅, 衰減秒)]"""
    x = np.zeros_like(t)
    tt = t - t0
    on = tt >= 0
    for f, a, tau in partials:
        x[on] += a * np.sin(2 * np.pi * f * tt[on]) * np.exp(-tt[on] / tau)
    # 2.5ms 的雜訊瞬態＝「喀」的那個硬邊
    burst = (tt >= 0) & (tt < 0.0025)
    x[burst] += noise_amp * rng.uniform(-1, 1, burst.sum()) * np.linspace(1, 0, burst.sum())
    return x


def synth() -> np.ndarray:
    rng = np.random.default_rng(1110)  # 固定種子，重跑結果一樣
    n = int(SR * DUR)
    t = np.arange(n) / SR
    x = _click(t, 0.000, [(3150, 0.55, 0.018), (4870, 0.35, 0.012), (7020, 0.20, 0.008),
                          (1720, 0.30, 0.030)], 0.9, rng)
    x += _click(t, 0.055, [(2480, 0.60, 0.028), (3990, 0.30, 0.016), (5610, 0.15, 0.010),
                           (1330, 0.35, 0.040), (190, 0.45, 0.035)], 0.7, rng)
    # 結尾淡出
    fade = int(SR * 0.015)
    x[-fade:] *= np.linspace(1, 0, fade)
    x[0] = 0.0
    peak = np.max(np.abs(x))
    x = x / peak * (10 ** (PEAK_DBFS / 20))
    return x


def write(path: Path, x: np.ndarray) -> None:
    pcm = np.clip(np.round(x * 32767), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    x = synth()
    write(Path(a.out), x)
    print(f"wrote {a.out}  {len(x) / SR:.3f}s  peak {PEAK_DBFS} dBFS（占位）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
