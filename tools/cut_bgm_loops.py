#!/usr/bin/env python3
"""
把 Suno 佔位曲裁成 brief 長度的無縫循環 BGM（issue #31 用的那一套，免費、只靠 numpy＋ffmpeg）。

做法（每首）：
  1. 從原曲取「循環起點 ti → 循環終點 tj」一段（兩點的和聲／節奏最像，是另外分析挑的，結果寫死在 CUTS）
  2. ffmpeg rubberband 微調速度（不變調），讓長度剛好等於 brief 秒數
  3. 檔尾 0.35 秒與「循環起點前 0.35 秒」交叉淡化 → 播到檔尾跳回 loop_offset 時，樣本是連續的，不會爆音
  4. 用 FFT 做循環式重取樣把長度修到精確樣本數（修正量 < 3 ms，聽不出音高差）
  5. 線性增益對齊 −16 LUFS；true peak 超過就跑循環式限幅（前後各接一圈再限幅，接縫不受影響）
  6. libmp3lame VBR q3 編成 <cue>.mp3（LAME 標頭帶 gapless 資訊，Godot 的 minimp3 會吃）
  7. 用 ffmpeg loudnorm 量最終 mp3，必要時再修一次增益

title 前段（loop_offset 之前，只播一次）另外疊程式合成的發條上鏈聲。
ending 不循環：取原曲最後一句到自然收尾，速度微調到 16 秒。

用法
  # 原曲：issue #31 之前的 Suno 佔位版（git blob 已寫在 SOURCE_BLOBS），預設從 git 取出
  python3 tools/cut_bgm_loops.py --out /tmp/bgm_cut            # 只輸出到暫存資料夾
  python3 tools/cut_bgm_loops.py --out game/assets/audio/bgm   # 覆蓋遊戲檔（記得同步 loops.json）
  python3 tools/cut_bgm_loops.py --only village,battle --src-dir ~/suno_originals

需求：python3＋numpy、帶 rubberband 濾鏡的 ffmpeg。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SR = 48000
TARGET_LUFS = -16.0
XFADE = 0.35

## issue #31 之前的佔位曲（git blob），原始來源見 game/assets/audio/bgm/SUNO_SOURCES.json
SOURCE_BLOBS = {
    "title": "8197d0953a48be8890e53a1c68745585deca6415",
    "village": "6fb11421cd48eac0cf935315d3014c9e57507529",
    "town": "a47257ba72a82cb6d7c73d358b3bcebbd5c41068",
    "road": "28b0076350cf323d431995a1dbb1dce99f905862",
    "forest": "0bba8a69e8fb0b199eec8f9cca6d3be8cae55a77",
    "battle": "d8b580746d84186bba2e59d3c0d294a719015546",
    "boss": "2e0def0ceec4fcc193fda068d34c452af36f1437",
    "ending": "4baea0f209e80d66dfbef81fe90027d5b834e55b",
}

## ts＝檔頭在原曲的位置、ti／tj＝循環起訖（秒，tj 已做過樣本級對齊）、
## total＝輸出長度、k2＝伸縮後接縫再對齊的樣本數、ceil＝限幅上限 dBTP
CUTS = {
    "title":   dict(ts=0.0,     ti=6.641,   tj=23.6964375,         total=24.0, k2=104, ceil=-1.7, windup=True),
    "village": dict(ts=36.688,  ti=36.688,  tj=80.32475,           total=45.0, k2=-17, ceil=-1.7),
    "town":    dict(ts=41.63,   ti=41.63,   tj=79.12995833333333,  total=40.0, k2=59,  ceil=-1.7),
    "road":    dict(ts=110.09,  ti=110.09,  tj=139.42327083333333, total=30.0, k2=-13, ceil=-1.7),
    "forest":  dict(ts=38.011,  ti=38.011,  tj=80.64964583333334,  total=40.0, k2=136, ceil=-1.7),
    "battle":  dict(ts=181.05,  ti=181.05,  tj=218.44935416666667, total=35.0, k2=32,  ceil=-1.7),
    "boss":    dict(ts=206.658, ti=206.658, tj=245.8066875,        total=40.0, k2=44,  ceil=-1.7),
    ## 不循環：ts → 自然收尾 tend，伸縮成 16 秒，頭 12 ms 淡入、尾 0.6 秒收到 0
    "ending":  dict(ts=255.84, tend=272.2, total=16.0, ceil=-2.4, oneshot=True),
}


def ffmpeg_decode(data_or_path, extra=()) -> np.ndarray:
    args = ["ffmpeg", "-v", "error"]
    inp = None
    if isinstance(data_or_path, (bytes, bytearray)):
        args += ["-i", "pipe:0"]
        inp = bytes(data_or_path)
    else:
        args += ["-i", str(data_or_path)]
    args += list(extra) + ["-f", "f32le", "-ac", "2", "-ar", str(SR), "pipe:1"]
    out = subprocess.run(args, input=inp, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype="<f4").reshape(-1, 2).astype(np.float64)


def ffmpeg_filter(sig: np.ndarray, af: str) -> np.ndarray:
    raw = sig.astype("<f4").tobytes()
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "pipe:0",
         "-af", af, "-f", "f32le", "-ac", "2", "-ar", str(SR), "pipe:1"],
        input=raw, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype="<f4").reshape(-1, 2).astype(np.float64)


def loudnorm_json(path_or_sig) -> dict:
    if isinstance(path_or_sig, np.ndarray):
        args = ["ffmpeg", "-hide_banner", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "pipe:0"]
        inp = path_or_sig.astype("<f4").tobytes()
    else:
        args = ["ffmpeg", "-hide_banner", "-i", str(path_or_sig)]
        inp = None
    p = subprocess.run(args + ["-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       input=inp, capture_output=True)
    s = p.stderr.decode("utf-8", "replace")
    return json.loads(s[s.rfind("{"):s.rfind("}") + 1])


def true_peak_db(sig: np.ndarray, circular: bool) -> float:
    pad = np.vstack([sig[-512:], sig, sig[:512]]) if circular else sig
    n = len(pad)
    F = np.fft.rfft(pad, axis=0)
    G = np.zeros((n * 2 + 1, 2), dtype=complex)
    G[:F.shape[0]] = F
    up = np.fft.irfft(G, n=n * 4, axis=0) * 4
    return float(20 * np.log10(np.abs(up).max() + 1e-12))


def limiter(sig: np.ndarray, ceil_db: float, look=0.005, rel=0.15) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    ceil = 10 ** (ceil_db / 20)
    n = len(sig)
    F = np.fft.rfft(sig, axis=0)
    G = np.zeros((n * 2 + 1, 2), dtype=complex)
    G[:F.shape[0]] = F
    up = np.abs(np.fft.irfft(G, n=n * 4, axis=0) * 4).max(1).reshape(n, 4).max(1)
    need = np.minimum(1.0, ceil / np.maximum(up, 1e-9))
    lk = int(look * SR)
    mn = sliding_window_view(np.concatenate([np.ones(lk), need, np.ones(lk)]), 2 * lk + 1).min(axis=1)
    g = np.empty_like(mn)
    cur, ar = 1.0, np.exp(-1 / (rel * SR))
    for i in range(len(mn)):
        cur = mn[i] if mn[i] < cur else ar * cur + (1 - ar) * mn[i]
        g[i] = cur
    k = np.ones(lk) / lk
    g = np.convolve(np.concatenate([np.full(lk, g[0]), g]), k, "valid")[:n]
    return sig * np.minimum(g, mn)[:, None]


def windup_layer(n: int) -> np.ndarray:
    """發條上鏈：三圈、每圈四下棘輪聲（雜訊激發的共振器），對齊 title 前奏的十六分音符格。"""
    rng = np.random.default_rng(31)

    def click(amp):
        m = int(0.04 * SR)
        t = np.arange(m) / SR
        nz = rng.standard_normal(m) * np.exp(-t / 0.0015)
        out = np.zeros(m)
        for f, q, a in ((3300, 30, 1.0), (6400, 25, 0.6), (1150, 12, 0.5)):
            w = 2 * np.pi * f / SR
            r = np.exp(-w / (2 * q))
            b1, b2 = 2 * r * np.cos(w), -r * r
            yv = np.zeros(m)
            x1 = x2 = 0.0
            for i in range(m):
                v = nz[i] + b1 * x1 + b2 * x2
                yv[i] = v
                x2, x1 = x1, v
            out += a * yv / np.abs(yv).max()
        out += 0.35 * np.sin(2 * np.pi * 420 * t) * np.exp(-t / 0.010)
        out *= np.exp(-t / 0.012)
        return amp * out / np.abs(out).max()

    lay = np.zeros((n, 2))
    for ti, t0 in enumerate((0.70, 1.63, 2.53)):
        for c in range(4):
            cl = click(10 ** ((-19 + (2 if c == 3 else 0) + ti) / 20))
            s = int((t0 + c * 0.155) * SR)
            pan = 0.42 + 0.04 * c
            lay[s:s + len(cl), 0] += cl * np.sqrt(1 - pan)
            lay[s:s + len(cl), 1] += cl * np.sqrt(pan)
    return lay


def stretch(sig: np.ndarray, r: float) -> np.ndarray:
    if abs(r - 1) < 1e-4:
        return sig
    return ffmpeg_filter(sig, f"rubberband=tempo={1 / r:.6f}:transients=mixed:phase=laminar:"
                              "window=standard:pitchq=quality:channels=together")


def intro_samples(n: float) -> int:
    """前奏長度取整到「毫秒」且讓 Godot 換算回樣本時不會少一格。

    loops.json 只寫到毫秒；AudioStreamMP3.loop_offset 是 32 位元 float，
    Godot 用 uint32(sample_rate * offset) 截斷，6.726 會變 322847（少 1 樣本）。
    挑一個鄰近、截斷後剛好整除的毫秒值，跳回去的樣本才完全對得上。
    """
    if n <= 0:
        return 0
    base = int(round(n / (SR / 1000)))
    for d in (0, 1, -1, 2, -2, 3, -3):
        ms = base + d
        if int(float(np.float32(ms / 1000)) * SR) == ms * SR // 1000:
            return ms * SR // 1000
    return base * SR // 1000


def cut_loop(src: np.ndarray, c: dict) -> tuple[np.ndarray, float]:
    ps, pa, pb = (int(round(c[k] * SR)) for k in ("ts", "ti", "tj"))
    r = c["total"] / ((pb - ps) / SR)
    m = int(4.0 * SR)
    es = ps - m
    ex = src[max(0, es):min(len(src), pb + m)]
    if es < 0:
        ex = np.vstack([np.zeros((-es, 2)), ex])
    st = stretch(ex, r)
    N = int(round(c["total"] * SR))
    S = int(round(m * r))
    A = S + intro_samples((pa - ps) * r)
    B = S + N + int(c.get("k2", 0))
    loop = st[A:B].copy()
    xn = int(XFADE * SR)
    w = (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, xn)))[:, None]
    loop[-xn:] = loop[-xn:] * (1 - w) + st[A - xn:A] * w
    lt = N - (A - S)
    if len(loop) != lt:  ## 循環式 FFT 重取樣，週期性不變
        F = np.fft.rfft(loop, axis=0)
        G = np.zeros((lt // 2 + 1, 2), dtype=complex)
        k = min(G.shape[0], F.shape[0])
        G[:k] = F[:k]
        loop = np.fft.irfft(G, n=lt, axis=0) * (lt / len(loop))
    intro = st[S:A]
    y = np.vstack([intro, loop]) if len(intro) else loop
    if c.get("windup"):
        y = y + windup_layer(len(y))
    return y, len(intro) / SR


def cut_oneshot(src: np.ndarray, c: dict) -> np.ndarray:
    pre = int(0.05 * SR)
    seg = src[int(c["ts"] * SR) - pre:int(c["tend"] * SR)]
    r = c["total"] / (len(seg) / SR - 0.05)
    st = stretch(seg, r)
    off = int(round(0.05 * r * SR))
    N = int(c["total"] * SR)
    y = st[off:off + N]
    if len(y) < N:
        y = np.vstack([y, np.zeros((N - len(y), 2))])
    fi, fo = int(0.012 * SR), int(0.6 * SR)
    y[:fi] *= np.linspace(0, 1, fi)[:, None]
    y[-fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    return y


def master(y: np.ndarray, loop_off: float | None, ceil: float, dst: Path) -> dict:
    loop = loop_off is not None
    li = int(round(loop_off * SR)) if loop else 0

    def norm(v):
        return v * 10 ** ((TARGET_LUFS - float(loudnorm_json(v)["input_i"])) / 20)

    y = norm(y)
    for _ in range(5):
        if true_peak_db(y, loop and li == 0) <= ceil:
            break
        if loop:  ## 前後各接一圈再限幅，取中間那圈 → 接縫兩側的增益一致
            body = y[li:]
            p = limiter(np.vstack([y[:li], body, body, body]), ceil - 0.4)
            y = np.vstack([p[:li], p[li + len(body):li + 2 * len(body)]])
        else:
            y = limiter(y, ceil - 0.4)
        y = norm(y)
    j = {}
    for _ in range(4):
        raw = y.astype("<f4").tobytes()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR),
                        "-i", "pipe:0", "-c:a", "libmp3lame", "-q:a", "3", str(dst)],
                       input=raw, check=True)
        j = loudnorm_json(dst)
        i_, tp = float(j["input_i"]), float(j["input_tp"])
        if abs(i_ - TARGET_LUFS) <= 0.2 and tp <= -1.0:
            break
        if tp > -1.0:
            y = y * 10 ** (-0.3 / 20) if loop else limiter(y, ceil - 0.5)
        y = y * 10 ** ((TARGET_LUFS - i_) / 20)
    return j


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True, help="輸出資料夾")
    ap.add_argument("--only", default="", help="逗號分隔 cue")
    ap.add_argument("--src-dir", type=Path, help="原曲資料夾（<cue>.mp3）；不給就從 git blob 取")
    args = ap.parse_args()
    ids = [x.strip() for x in args.only.split(",") if x.strip()] or list(CUTS)
    args.out.mkdir(parents=True, exist_ok=True)
    loops = {}
    for cue in ids:
        c = CUTS[cue]
        if args.src_dir:
            src = ffmpeg_decode(args.src_dir / f"{cue}.mp3")
        else:
            blob = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", SOURCE_BLOBS[cue]],
                                  capture_output=True, check=True).stdout
            src = ffmpeg_decode(blob)
        if c.get("oneshot"):
            y, off = cut_oneshot(src, c), None
        else:
            y, off = cut_loop(src, c)
            loops[cue] = round(off, 3)
        j = master(y, off, c["ceil"], args.out / f"{cue}.mp3")
        print(f"{cue:8s} {len(y) / SR:6.2f}s  loop_offset {off}  I {j['input_i']} LUFS  TP {j['input_tp']} dBTP")
    print("loops.json 應為：", json.dumps(loops))
    return 0


if __name__ == "__main__":
    sys.exit(main())
