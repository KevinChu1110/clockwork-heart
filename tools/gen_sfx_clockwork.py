#!/usr/bin/env python3
"""
發條之心 · 戰鬥自動回饋音效合成（免費、可重產）。issue #32

只用 numpy 合成，固定亂數種子，重跑結果逐位元相同。不用任何付費生成服務。
規格：docs/CLOCKWORK_ART_MUSIC_BRIEF.md §5；清單與響度規格：game/assets/audio/MANIFEST.md。
世界是「發條八音盒＋輕管弦」：聲音材料只用黃銅、錫皮、玻璃鐘、棘輪、彈簧、木質機身，
不要肉擊、爆炸、電子嗶聲。

每個 key 一個 synth_<key>()；全部走同一個收尾：
  1. 頭 0 起、尾 fade-out（一次性，不循環）
  2. 以「最大瞬時響度 M-max」（BS.1770 K-weighting，400 ms 視窗，檔尾補 1 秒靜音）正規化到目標
  3. true peak（4× 超取樣）超過上限就用前視限幅器壓，保證 ≤ −1 dBTP（內部留 0.3 dB 餘裕）

用法
  python3 tools/gen_sfx_clockwork.py              # 重產全部（swap hit slash break warn wind）
  python3 tools/gen_sfx_clockwork.py hit slash    # 只重產指定的
  python3 tools/gen_sfx_clockwork.py --measure    # 量 sfx/ 下現有檔，不寫檔
  python3 tools/gen_sfx_clockwork.py --out-dir /tmp/x
寫完要 `godot --path game --headless --import` 一次（只 commit 對應的 .wav.import）。
"""
from __future__ import annotations

import argparse
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SFX_DIR = ROOT / "game" / "assets" / "audio" / "sfx"
SR = 44100
TP_CEIL_DBTP = -1.3     # 內部上限；交付規格是 ≤ −1 dBTP
# M-max 目標（LUFS）。分層理由見 MANIFEST.md「響度規格」
TARGET_M = {
    "swap": -20.0, "break": -20.0, "warn": -20.0,   # 事件 cue
    "hit": -23.0, "slash": -23.0,                   # 頻繁回饋，和跳字同一瞬間
    "wind": -21.0,                                  # 戰前上鏈
}
# true peak 上限（dBTP）。交付規格全部 ≤ −1；hit／slash 和跳字同一瞬間、又最常響，
# 峰值再壓到 −4（和舊 hit 占位的峰值一樣），讓瞬態不會「啪」一下蓋過跳字
TP_CEIL = {"hit": -4.0, "slash": -4.0}
SEEDS = {"swap": 1110, "hit": 3201, "slash": 3202, "break": 3203, "warn": 3204, "wind": 3205}


# ───────────────────────── 基本元件 ─────────────────────────

def _t(dur: float) -> np.ndarray:
    return np.arange(int(round(SR * dur))) / SR


def place(buf: np.ndarray, x: np.ndarray, t0: float, gain: float = 1.0) -> None:
    """把 x 疊到 buf 的 t0 秒處（超出尾巴就截掉）"""
    i = int(round(t0 * SR))
    if i >= len(buf):
        return
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += gain * x[:n]


def modes(dur: float, partials: list[tuple[float, float, float]], rng: np.random.Generator,
          attack: float = 0.0004) -> np.ndarray:
    """非諧波金屬共振：partials = [(頻率 Hz, 振幅, 衰減 τ 秒)]，每個分音隨機相位"""
    t = _t(dur)
    x = np.zeros_like(t)
    for f, a, tau in partials:
        if f >= SR * 0.45:
            continue
        ph = rng.uniform(0, 2 * np.pi)
        x += a * np.sin(2 * np.pi * f * t + ph) * np.exp(-t / tau)
    if attack > 0:
        na = max(1, int(attack * SR))
        x[:na] *= np.linspace(0, 1, na)
    return x


def noise_burst(dur: float, rng: np.random.Generator, tau: float | None = None) -> np.ndarray:
    n = max(1, int(round(dur * SR)))
    x = rng.uniform(-1, 1, n)
    if tau is None:
        return x * np.linspace(1, 0, n)
    return x * np.exp(-np.arange(n) / SR / tau)


def sweep_sine(dur: float, f0: float, f1: float, tau: float, curve: float = 0.04) -> np.ndarray:
    """音高從 f0 指數滑到 f1（時間常數 curve 秒），振幅 exp 衰減"""
    t = _t(dur)
    f = f1 + (f0 - f1) * np.exp(-t / curve)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / tau)


def biquad(x: np.ndarray, b: tuple, a: tuple) -> np.ndarray:
    b0, b1, b2 = b
    _, a1, a2 = a
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for i, xi in enumerate(x):
        yi = b0 * xi + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1, y2, y1 = x1, xi, y1, yi
        y[i] = yi
    return y


def _rbj(kind: str, f0: float, q: float, gain_db: float = 0.0, fs: int = SR) -> tuple[tuple, tuple]:
    """RBJ cookbook biquad，回傳正規化後 (b, a)"""
    w = 2 * np.pi * f0 / fs
    cw, sw = np.cos(w), np.sin(w)
    alpha = sw / (2 * q)
    A = 10 ** (gain_db / 40)
    if kind == "hp":
        b = ((1 + cw) / 2, -(1 + cw), (1 + cw) / 2)
        a = (1 + alpha, -2 * cw, 1 - alpha)
    elif kind == "lp":
        b = ((1 - cw) / 2, 1 - cw, (1 - cw) / 2)
        a = (1 + alpha, -2 * cw, 1 - alpha)
    elif kind == "bp":
        b = (alpha, 0.0, -alpha)
        a = (1 + alpha, -2 * cw, 1 - alpha)
    elif kind == "highshelf":
        sa = 2 * np.sqrt(A) * alpha
        b = (A * ((A + 1) + (A - 1) * cw + sa), -2 * A * ((A - 1) + (A + 1) * cw),
             A * ((A + 1) + (A - 1) * cw - sa))
        a = ((A + 1) - (A - 1) * cw + sa, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - sa)
    else:
        raise ValueError(kind)
    a0 = a[0]
    return tuple(v / a0 for v in b), tuple(v / a0 for v in a)


def filt(x: np.ndarray, kind: str, f0: float, q: float = 0.707) -> np.ndarray:
    b, a = _rbj(kind, f0, q)
    return biquad(x, b, a)


def svf_bandpass_sweep(x: np.ndarray, fc: np.ndarray, q: float) -> np.ndarray:
    """可隨時間掃頻的 state-variable 帶通（Chamberlin，兩倍超取樣內插穩定）"""
    y = np.zeros_like(x)
    low = band = 0.0
    damp = 1.0 / q
    for i, xi in enumerate(x):
        f = 2 * np.sin(np.pi * min(fc[i], SR / 6) / (2 * SR))
        for _ in range(2):  # 兩步內插
            low += f * band
            high = xi - low - damp * band
            band += f * high
        y[i] = band
    return y


def fade_out(x: np.ndarray, dur: float) -> np.ndarray:
    n = min(len(x), int(dur * SR))
    if n > 0:
        x[-n:] *= np.cos(np.linspace(0, np.pi / 2, n)) ** 2
    return x


def soft_sat(x: np.ndarray, drive: float) -> np.ndarray:
    return np.tanh(drive * x) / np.tanh(drive)


# ───────────────────────── 量測（BS.1770） ─────────────────────────

def _k_weight(x: np.ndarray, fs: int) -> np.ndarray:
    # BS.1770 的 K-weighting：+4 dB high shelf @1681.97 Hz ＋ RLB high-pass @38.13 Hz
    # 係數用 pyloudnorm 同款參數換算到任意取樣率
    b1, a1 = _shelf_1770(fs)
    b2, a2 = _hp_1770(fs)
    return biquad(biquad(x, b1, a1), b2, a2)


def _shelf_1770(fs: int) -> tuple[tuple, tuple]:
    G, Q, fc = 3.99984385397, 0.7071752369554193, 1681.9744509555319
    A = 10 ** (G / 40)
    w = 2 * np.pi * fc / fs
    alpha = np.sin(w) / (2 * Q)
    cw = np.cos(w)
    sa = 2 * np.sqrt(A) * alpha
    b = (A * ((A + 1) + (A - 1) * cw + sa), -2 * A * ((A - 1) + (A + 1) * cw),
         A * ((A + 1) + (A - 1) * cw - sa))
    a = ((A + 1) - (A - 1) * cw + sa, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - sa)
    return tuple(v / a[0] for v in b), tuple(v / a[0] for v in a)


def _hp_1770(fs: int) -> tuple[tuple, tuple]:
    Q, fc = 0.5003270373253953, 38.13547087613982
    w = 2 * np.pi * fc / fs
    alpha = np.sin(w) / (2 * Q)
    cw = np.cos(w)
    b = (1.0, -2.0, 1.0)
    a = (1 + alpha, -2 * cw, 1 - alpha)
    return tuple(v / a[0] for v in b), tuple(v / a[0] for v in a)


def m_max(x: np.ndarray, fs: int = SR) -> float:
    """最大瞬時響度（400 ms 視窗、100 ms 步進），檔尾補 1 秒靜音"""
    y = _k_weight(np.concatenate([x, np.zeros(fs)]), fs)
    win, hop = int(0.4 * fs), int(0.1 * fs)
    sq = np.concatenate([[0.0], np.cumsum(y * y)])
    best = 1e-12
    for i in range(0, len(y) - win + 1, hop):
        best = max(best, (sq[i + win] - sq[i]) / win)
    return -0.691 + 10 * np.log10(best)


def true_peak_db(x: np.ndarray, over: int = 4) -> float:
    n = len(x) + 256
    X = np.fft.rfft(np.concatenate([x, np.zeros(256)]))
    y = np.fft.irfft(X, n * over) * over
    return 20 * np.log10(max(np.max(np.abs(y)), np.max(np.abs(x)), 1e-12))


def sample_peak_db(x: np.ndarray) -> float:
    return 20 * np.log10(max(np.max(np.abs(x)), 1e-12))


def limiter(x: np.ndarray, ceil_lin: float, look: float = 0.0015, release: float = 0.03) -> np.ndarray:
    """前視峰值限幅：需要的增益取前視視窗最小值，再用 release 平滑回升"""
    need = np.minimum(1.0, ceil_lin / np.maximum(np.abs(x), 1e-12))
    la = max(1, int(look * SR))
    pad = np.concatenate([need, np.ones(la)])
    # 前視最小值
    m = np.array([pad[i:i + la].min() for i in range(len(x))])
    g = np.empty_like(m)
    cur = 1.0
    rc = np.exp(-1.0 / (release * SR))
    for i, v in enumerate(m):
        cur = v if v < cur else v + (cur - v) * rc
        g[i] = cur
    return x * g


def finish(key: str, x: np.ndarray, fade: float) -> np.ndarray:
    x = x - np.mean(x)
    x[0] = 0.0
    x = fade_out(x, fade)
    target = TARGET_M[key]
    tp_ceil = TP_CEIL.get(key, TP_CEIL_DBTP)
    ceil = 10 ** (tp_ceil / 20)
    for _ in range(10):
        x = x * 10 ** ((target - m_max(x)) / 20)
        if true_peak_db(x) > tp_ceil:
            # 限幅器作用在樣本上，真峰值另外再留一點空間
            x = limiter(x, ceil * 0.94)
        if abs(m_max(x) - target) < 0.15 and true_peak_db(x) <= tp_ceil:
            break
    if true_peak_db(x) > tp_ceil:
        x *= 10 ** ((tp_ceil - true_peak_db(x)) / 20)
    return x


# ───────────────────────── 各音效 ─────────────────────────

def synth_swap(rng: np.random.Generator) -> tuple[np.ndarray, float]:
    """換欄卡榫（0.24 s）：兩下棘輪「喀喀」→ 一聲扣入的「卡」＋機身低頻 → 彈簧細碎回震"""
    dur = 0.24
    out = np.zeros(int(SR * dur))
    # 兩下棘輪（音高一下比一下低一點，像爪子滑過齒）
    for t0, k, g in [(0.000, 1.00, 0.45), (0.032, 0.94, 0.55)]:
        tick = modes(0.03, [(4250 * k, 0.6, 0.0045), (6180 * k, 0.4, 0.0032),
                            (8350 * k, 0.25, 0.0022), (2900 * k, 0.25, 0.006)], rng)
        place(tick, filt(noise_burst(0.0012, rng), "hp", 2500) * 0.9, 0.0)
        place(out, tick, t0, g)
    # 扣入：黃銅卡榫（非諧波）＋機身木盒＋低頻「咚」
    latch = modes(0.15, [(2360, 0.55, 0.026), (3710, 0.38, 0.018), (5490, 0.24, 0.011),
                         (7930, 0.12, 0.007), (1180, 0.30, 0.032), (430, 0.22, 0.040)], rng)
    place(latch, filt(noise_burst(0.0025, rng), "hp", 1400) * 1.1, 0.0)
    place(latch, sweep_sine(0.08, 230, 150, 0.026, 0.015) * 0.55, 0.0)
    place(out, latch, 0.078, 1.0)
    # 彈簧回震：幾顆越來越小的細碎金屬點
    t0 = 0.098
    for i in range(5):
        t0 += rng.uniform(0.010, 0.020)
        f = rng.uniform(5200, 7400)
        grain = modes(0.02, [(f, 1.0, 0.003), (f * 1.53, 0.5, 0.002)], rng)
        place(out, grain, t0, 0.10 * (0.7 ** i))
    return out, 0.02


def synth_hit(rng: np.random.Generator) -> tuple[np.ndarray, float]:
    """命中（0.16 s）：錫皮玩具被敲——短「咚」機身＋錫片非諧波「噹」＋一點硬邊"""
    dur = 0.16
    out = np.zeros(int(SR * dur))
    body = sweep_sine(dur, 210, 105, 0.040, 0.025)
    tin = modes(dur, [(905, 0.42, 0.030), (1437, 0.34, 0.022), (2215, 0.24, 0.015),
                      (3190, 0.15, 0.010), (4620, 0.08, 0.006)], rng)
    click = filt(noise_burst(0.004, rng, tau=0.0012), "lp", 5000)
    place(out, body, 0.0, 0.85)
    place(out, tin, 0.0005, 0.75)
    place(out, click, 0.0, 0.9)
    return out, 0.025


def synth_slash(rng: np.random.Generator) -> tuple[np.ndarray, float]:
    """斬擊（0.22 s）：黃銅刃劃過——上掃的空氣聲＋細細一聲「鏘」"""
    dur = 0.22
    n = int(SR * dur)
    out = np.zeros(n)
    t = np.arange(n) / SR
    # 空氣聲：白噪經掃頻帶通，中心 1.1 k → 5 k（0～90 ms），振幅 60 ms 到頂後快收
    fc = 1100 + (5000 - 1100) * np.clip(t / 0.09, 0, 1) ** 0.8
    env = np.where(t < 0.06, (t / 0.06) ** 1.5, np.exp(-(t - 0.06) / 0.022))
    whoosh = svf_bandpass_sweep(rng.uniform(-1, 1, n), fc, 2.2) * env
    whoosh /= max(np.max(np.abs(whoosh)), 1e-9)
    place(out, whoosh, 0.0, 0.7)
    # 鏘：細長刃的高分音，成對微失諧產生閃光感
    shing = modes(0.16, [(3400, 0.30, 0.055), (3413, 0.22, 0.050), (5160, 0.22, 0.040),
                         (6880, 0.14, 0.028), (8930, 0.08, 0.018)], rng, attack=0.002)
    place(out, shing, 0.055, 0.9)
    return out, 0.03


SYNTHS = {
    "swap": synth_swap, "hit": synth_hit, "slash": synth_slash,
}


# ───────────────────────── 輸出 ─────────────────────────

def write_wav(path: Path, x: np.ndarray) -> None:
    pcm = np.clip(np.round(x * 32767), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        raw = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float) / 32768
    if ch > 1:
        raw = raw.reshape(-1, ch).mean(axis=1)
    return raw, sr


def render(key: str) -> np.ndarray:
    rng = np.random.default_rng(SEEDS[key])
    x, fade = SYNTHS[key](rng)
    return finish(key, x, fade)


def report(key: str, x: np.ndarray, sr: int = SR) -> str:
    return (f"{key:6s} {len(x) / sr:5.3f}s  M-max {m_max(x, sr):6.1f} LUFS  "
            f"TP {true_peak_db(x):5.1f} dBTP  sample peak {sample_peak_db(x):5.1f} dBFS")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="*", help=f"預設全部：{' '.join(SYNTHS)}")
    ap.add_argument("--out-dir", default=str(SFX_DIR))
    ap.add_argument("--measure", action="store_true", help="只量 sfx/ 下現有檔")
    a = ap.parse_args()
    keys = a.keys or list(SYNTHS)
    for k in keys:
        if k not in SYNTHS:
            ap.error(f"不認得 {k}；可用：{' '.join(SYNTHS)}")
    for k in keys:
        if a.measure:
            x, sr = read_wav(Path(a.out_dir) / f"{k}.wav")
            print(report(k, x, sr))
            continue
        x = render(k)
        out = Path(a.out_dir) / f"{k}.wav"
        write_wav(out, x)
        x16, _ = read_wav(out)
        print("wrote", report(k, x16))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
