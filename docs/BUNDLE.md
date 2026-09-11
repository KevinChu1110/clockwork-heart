# 分包（Product Lock §5.2）

目標不是「整個遊戲永遠 < 50 MB」，是**第一次接觸不要被下載量嚇跑**。
首次必要下載 **50～80 MB**。量測指令：

```
python3 tools/measure_bundle.py
python3 tools/measure_bundle.py --apply-presets   # 把 filter 寫回 game/export_presets.cfg
```

單一真相：`game/data/bundle_manifest.json`。Runtime：`BundlePacks`／`BundleLoader`。

> **W3-F1（2026-09-11）**：core 源資產 **45.29 MB**（was 61.45）；Mac／Android／iOS 用 CORE filter；數字與商店短句見 [`docs/W3_CORE_SIZE.md`](W3_CORE_SIZE.md)。

---

## 量測（2026-09-07）

| 項目 | 大小 | 說明 |
|---|---:|---|
| `web/` 行銷站 | **135.42 MB** | Product Lock 寫的「Web 目錄 135 MB」。**不是遊戲 export**。其中 `web/media` 130.43 MB（預告片／shorts）。瀏覽器只抓點到的檔，但整站部署體積是這個數。⛔ 沒刪行銷片。 |
| 遊戲資產合計（源檔） | ~172 MB | core + chapter + extra |
| **core 首包源資產** | **54.54 MB** | 標題＋大廳＋C0 |
| chapter | 62.01 MB | C1～C6 地圖與 BGM |
| extra | 54.97 MB | wav 占位、Noto 後備字、決鬥插圖、與 webp 重複的 png |

這台沒裝 Godot export templates，**沒有打出 APK／PCK 的實重**。引擎本體經驗值 Android arm64／Linux 約 25–40 MB。

**首包估計 = 54.54 + 引擎 ≈ 80–95 MB。** 對硬上限 80 MB 大約超 **0～15 MB**（視模板）。源資產本身已落在 50–80。

### 玩家第一次拿到什麼（core）

標題 → 大廳（今日村莊／四大殿堂）→ C0 閣樓＋荒路，含：

- 地圖前綴 `village*`／`road*`／`town*`，外加 `barracks_yard`、`sky_kingdom`
- BGM：`title`／`village`／`town`／`road`／`battle`（C0 教學戰走 battle，不是 boss）
- 粉圓體、操作／戰鬥／紙娃娃／C0 用立繪與怪圖
- 標題底圖 `illustrations/title_bg*.png`（不再整包排除 illustrations）

進 C1 以後沒裝 chapter 包：地圖進不去，彈「尚未下載」。

### 之後加區域

未知地圖 id **預設 chapter**。只有 `village`／`road`／`town` 前綴會進首包。測試 `test_bundle.gd` 釘這條。

---

## 三包

| 包 | 誰載 | 內容 |
|---|---|---|
| **core** | 第一次下載。Android／iOS export 用這組 exclude | 上面那條路徑 |
| **chapter** | 進 C1～C6 時。PCK 放執行檔旁 `packs/chapter.pck` 或 `user://packs/` | 其餘地圖底圖＋`wild/mist/dojo/forest/coast/tower/ending/boss` BGM |
| **extra** | 換語系或要後備音源時 | Noto TC/SC/KR、BGM `.wav` 占位、`duel_*.png`、已有 webp 的 png |

桌面 Win／mac／Linux 仍是**完整可玩包**，只拿掉 extra 裡「永遠不該進包」的重複檔（wav、決鬥插圖、重複 png）。Noto 留在桌面包，Linux 才不會豆腐。手機首包不含 Noto；`GameFont` 缺檔就跳過後備。

掛 PCK：`BundleLoader` 開機掃 `packs/*.pck`。今晚沒打出 PCK（缺 export templates）。

---

## 從全量到首包，移出了什麼

相對「全部打進一個包」：

- chapter 地圖＋BGM：**62 MB** 移出手機首包
- extra：**55 MB**（wav 約 26、Noto 約 18、決鬥插圖、4 張重複 png）
- 標題圖改為**保留**（先前 `illustrations/**` 連標題一起被排除）

`web/media` 130 MB 本來就不進遊戲包。

---

## 下一步還能砍（要碰到 80 MB 含引擎）

剩餘最大項都在 core BGM（約 176 kbps mp3）：

| 檔 | 源檔 |
|---|---:|
| `battle.mp3` | 6.91 MB |
| `road.mp3` | 5.40 MB |
| `village.mp3` | 4.29 MB |
| `town.mp3` | 3.76 MB |
| `title.mp3` | 2.72 MB |
| 粉圓體 | 4.68 MB |

把這五首壓到 ~96 kbps 大約再省 **10–15 MB**，含引擎就有機會進 50–80。今晚沒轉碼（音質要 Kevin 點頭）。Boss 圖集整包進 chapter 也能再削，但大廳／C0 可能缺立繪，沒動。

---

## 驗收對照

- Product Lock §5.2：邊界寫清；首包源資產 54.54 MB；含引擎估計 80–95，差額與下一刀寫在上面。
- 標題→大廳→C0：core 地圖與 BGM 都在 allowlist；缺 chapter 不會開不了遊戲。
- review.md 程式 20／21：相關測試 `TEST_FILTER=bundle`；不動戰鬥數值、CANON、`.github/workflows`、`release/`。
