# 《發條之心》30 秒短影音實機素材清單與索引（REC-01～REC-04）

> **主題**：戰魂收斂與戰鬥手感全面升級（內部代號：`mk-shorts`）  
> **制定依據**：`docs/marketing/SHORTS_SOUL_BATTLE_POLISH_30S.md` 第四節與第五節  
> **產出日期**：2026-09-08  
> **錄製執行**：側案·程式 阿宏（sideworker）  
> **規範標準**：嚴格遵守 `references/review.md` 第 10～19 條、第 12 條（全片 9:16 直式 1080×1920）、第 19e 條（逐條 ls 驗證）。

---

## 一、實機錄製素材總表（對齊分鏡表秒數與內容）

| 素材編號 | 對應鏡次 | 規定秒數 | 實錄秒數 | 畫幅比例與格式 | 畫面核心內容與操作序列驗證 |
|---|---|---|---|---|---|
| **REC-01** | Shot 2 | **4.5s** | **4.50s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **右手拇指操作熱區（ThumbPad HUD）**<br>荒路殘兵戰鬥，展示右側 ThumbPad（攻擊、換武、鎖定、技能、暫停）。小白單手持長劍連續 3 次普攻揮斬，點擊 ThumbSwitch 順暢切換巨錘（武器圖示即時更換），點擊 ThumbLock 目標指示器切換。 |
| **REC-02** | Shot 3 | **8.0s** | **8.00s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **視覺換血與 0.15s 打擊停頓**<br>守衛巨獸雷歐戰鬥，展示線性平滑插畫感、`outline.gdshader` 深暖褐粗描邊、`foot_shadow.gdshader` 獨立層落地柔化橢圓軟影。普攻斬擊命中觸發精確 0.15s Hitstop 打擊停頓與金色跳字爆散。 |
| **REC-03** | Shot 4 | **5.0s** | **5.00s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **聚魂殿四階封靈罐與首屏透明保底**<br>聚魂殿介面，無任何系統 Emoji。首屏上方清楚展示「虔誠度 60/100 · 再 4 抽得碎片」透明保底進度條，中央綠→藍→紫→橙四階發條封靈罐，點擊抽魂觸發金光迸裂開光動態。 |
| **REC-04** | Shot 5 | **6.5s** | **6.50s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **怒氣超轉速過載（Overdrive）與部位 BREAK**<br>雷歐戰鬥怒氣值累積滿 100%，觸發「暴怒覺醒 / 齒輪過載」，小白以 +25% 攻速展開高速狂暴連斬，重擊打碎雷歐「獅衛重盾」防禦部位，彈出金色「BREAK！」字樣與零件崩飛。 |

- **實機素材累計時長**：`4.5s + 8.0s + 5.0s + 6.5s = 24.0s`（加上 Shot 1 概念圖 3.0s 與 Shot 6 品牌點題卡 3.0s，剛好 30.0s 嚴絲合縫）。

---

## 二、素材交付檔案清單與存放路徑

所有素材已妥善存放於當前 Kanban Task Workspace 以及專案目錄中，供後續合成使用：

### 1. 9:16 直式影片素材（1080×1920，主要合成素材）
| 素材編號 | Workspace 路徑 | 專案交付路徑 (`docs/marketing/shots/`) | 檔案大小 | SHA256 (首8碼) |
|---|---|---|---|---|
| **REC-01** | `rec01_thumb_pad_9x16.mp4` | `docs/marketing/shots/rec01_thumb_pad_9x16.mp4` | 436 KB | `18e4a17e` |
| **REC-02** | `rec02_battle_polish_9x16.mp4` | `docs/marketing/shots/rec02_battle_polish_9x16.mp4` | 486 KB | `9034b6c6` |
| **REC-03** | `rec03_soul_pity_9x16.mp4` | `docs/marketing/shots/rec03_soul_pity_9x16.mp4` | 201 KB | `07185f9e` |
| **REC-04** | `rec04_overdrive_break_9x16.mp4` | `docs/marketing/shots/rec04_overdrive_break_9x16.mp4` | 410 KB | `446cf8e5` |

### 2. 9:16 直式特寫裁切版影片素材（1080×1920，備用特寫剪輯）
| 素材編號 | Workspace 路徑 | 專案交付路徑 (`docs/marketing/shots/`) | 檔案大小 | SHA256 (首8碼) |
|---|---|---|---|---|
| **REC-01** | `rec01_thumb_pad_9x16_crop.mp4` | `docs/marketing/shots/rec01_thumb_pad_9x16_crop.mp4` | 434 KB | `cdab4c6f` |
| **REC-02** | `rec02_battle_polish_9x16_crop.mp4` | `docs/marketing/shots/rec02_battle_polish_9x16_crop.mp4` | 554 KB | `82f7dcfd` |
| **REC-03** | `rec03_soul_pity_9x16_crop.mp4` | `docs/marketing/shots/rec03_soul_pity_9x16_crop.mp4` | 249 KB | `a1c1401a` |
| **REC-04** | `rec04_overdrive_break_9x16_crop.mp4` | `docs/marketing/shots/rec04_overdrive_break_9x16_crop.mp4` | 445 KB | `a077a8e9` |

### 3. 16:9 原始實機錄影母帶（1280×720，原始無損畫面）
| 素材編號 | Workspace 路徑 | 檔案大小 | SHA256 (首8碼) |
|---|---|---|---|
| **REC-01** | `rec01_thumb_pad_raw_16x9.mp4` | 391 KB | `5cff80ff` |
| **REC-02** | `rec02_battle_polish_raw_16x9.mp4` | 444 KB | `99004307` |
| **REC-03** | `rec03_soul_pity_raw_16x9.mp4` | 171 KB | `cbf116f1` |
| **REC-04** | `rec04_overdrive_break_raw_16x9.mp4` | 369 KB | `f79838cb` |

### 4. 關鍵幀截圖證明（PNG，驗證真實畫面與 UI）
| 素材編號 | Workspace 路徑 | 專案交付路徑 (`docs/marketing/shots/`) | 驗證焦點 |
|---|---|---|---|
| **REC-01** | `rec01_thumb_pad.png` | `docs/marketing/shots/rec01_thumb_pad.png` | 右側 ThumbPad 操作熱區、換武至精鋼重錘日誌 |
| **REC-02** | `rec02_battle_polish.png` | `docs/marketing/shots/rec02_battle_polish.png` | 小白 vs 雷歐、角色粗描邊與落地軟影 |
| **REC-03** | `rec03_soul_pity.png` | `docs/marketing/shots/rec03_soul_pity.png` | 聚魂殿四階封靈罐、60/100 虔誠度首屏保底進度條 |
| **REC-04** | `rec04_overdrive_break.png` | `docs/marketing/shots/rec04_overdrive_break.png` | 怒氣全滿、暴怒覺醒中、部位獅衛重盾破甲擊破 |

---

## 三、review.md 第 19e 條逐項查證清單

依據 `references/review.md` 第 19e 條要求，對分鏡表（第四節、第五節、第七節）提及之所有場景、shader、腳本與品牌資產進行實體 `ls` / `stat` 查驗：

| 檔案路徑 | 類型 | 存在狀態 | 檔案大小 | 查驗結果 |
|---|---|---|---|---|
| `game/scenes/battle/battle.tscn` | 核心戰鬥場景 | 存在 | 8,614 Bytes | ✅ 通過 |
| `game/scenes/main.tscn` | 主遊戲場景 | 存在 | 1,123 Bytes | ✅ 通過 |
| `game/shaders/outline.gdshader` | 角色深色描邊著色器 | 存在 | 1,053 Bytes | ✅ 通過 |
| `game/shaders/foot_shadow.gdshader` | 落地柔化軟影著色器 | 存在 | 517 Bytes | ✅ 通過 |
| `game/scripts/battle/battle_view.gd` | 戰鬥介面與 ThumbPad | 存在 | 118,497 Bytes | ✅ 通過 |
| `game/scripts/battle/test_battle_thumb.gd` | 右手拇指操作測試依據 | 存在 | 8,770 Bytes | ✅ 通過 |
| `game/scripts/dev/capture_battle_polish.gd` | 既有戰鬥換血捕捉腳本 | 存在 | 2,208 Bytes | ✅ 通過 |
| `game/scripts/main.gd` | 主場景邏輯（`_go_soul_panel`） | 存在 | 279,601 Bytes | ✅ 通過 |
| `game/scripts/systems/soul_system.gd` | 戰魂與封靈罐系統邏輯 | 存在 | 36,695 Bytes | ✅ 通過 |
| `branding/logo_cn.png` | 官方中文字標（片尾點題卡） | 存在 | 866,886 Bytes | ✅ 通過 |
| `branding/title_plate.png` | 官方純黑底板（片尾點題卡） | 存在 | 373,881 Bytes | ✅ 通過 |
| `branding/key_visual_main.png` | 官方主視覺資產（Shot 1 參考） | 存在 | 1,862,935 Bytes | ✅ 通過 |

---

## 四、重現與驅動方式說明

本批素材錄製採用既有 Godot 引擎與 Linux Xvfb 虛擬顯示器配合 ffmpeg 擷取：
- 驅動腳本：
  - `game/scripts/dev/capture_rec01_thumb.gd`
  - `game/scripts/dev/capture_rec02_polish.gd`
  - `game/scripts/dev/capture_rec03_soul.gd`
  - `game/scripts/dev/capture_rec04_break.gd`
- 自動批次錄影工具：`/root/record_shorts_recs.sh`
- 執行指令：
  ```bash
  /root/record_shorts_recs.sh
  ```
  即可全自動重新錄製出上述所有 9:16、16:9 及關鍵幀截圖資產。
