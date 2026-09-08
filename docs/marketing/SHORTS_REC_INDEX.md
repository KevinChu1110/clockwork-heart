# 《發條之心》30 秒短影音實機素材清單與索引（REC-01～REC-04）

> **主題**：戰魂收斂與戰鬥手感全面升級（內部代號：`mk-shorts`）  
> **制定依據**：`docs/marketing/SHORTS_SOUL_BATTLE_POLISH_30S.md` 第四節與第五節  
> **產出日期**：2026-09-08  
> **錄製執行**：側案·程式 阿宏（sideworker）  
> **規範標準**：嚴格遵守 `references/review.md` 第 10～19 條、第 12 條（全片 9:16 直式 1080×1920）、第 19e 條（逐條 ls 驗證）、第 19b 條（100% 真實 Godot 錄影）、第 19g 條（逐格抽幀比對確認與索引吻合）、第 19g-1 條（索引跳字回 grep 確認含 emoji 原字串與開圖驗證）。  
> **驗證備忘**：採用檔案握手信號機制（場景與畫面完全渲染穩定後方啟動錄影），徹底根除 Godot 開機 Splash Screen 與滑鼠游標。四段縮圖與影片已全數經由 Vision 開圖查驗，逐項比對特效、跳字、進度條數值與 UI 元素真實無誤，REC-04 實測跳字「暴怒覺醒！」（無系統 emoji）與三連斬擊戰鬥日誌 3 次 17 暴擊傷害、雷歐生命值 420 扣至 369 與畫面 100% 吻合。

---

## 一、實機錄製素材總表（對齊分鏡表秒數與內容）

| 素材編號 | 對應鏡次 | 規定秒數 | 實錄秒數 | 畫幅比例與格式 | 畫面核心內容與操作序列驗證 |
|---|---|---|---|---|---|
| **REC-01** | Shot 2 | **4.5s** | **4.50s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **右手拇指操作熱區（ThumbPad HUD）**<br>荒路殘兵戰鬥，展示右側 ThumbPad（攻擊、換武、鎖定、技能、暫停）。小白單手持長劍連續 3 次普攻揮斬，點擊 ThumbSwitch 順暢切換巨錘（武器圖示即時更換），點擊 ThumbLock 目標指示器切換。 |
| **REC-02** | Shot 3 | **8.0s** | **8.00s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **視覺換血與 0.15s 打擊停頓**<br>守衛巨獸雷歐戰鬥，展示線性平滑插畫感、`outline.gdshader` 深暖褐粗描邊、`foot_shadow.gdshader` 獨立層落地柔化橢圓軟影。普攻斬擊命中觸發精確 0.15s Hitstop 打擊停頓與金色跳字爆散。 |
| **REC-03** | Shot 4 | **5.0s** | **5.00s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **聚魂殿四階封靈罐開光與首屏透明保底**<br>聚魂殿介面，無任何系統 Emoji。首屏上方清楚展示「綠階封靈罐 → 藍階封靈罐 → 紫階封靈罐 → 橙階封靈罐」四階發條封靈罐並列，上方清楚展示「虔誠度 60/100 · 再抽 4 次獲得碎片」透明保底進度條（60% 橘黃進度），點擊抽魂觸發橙階封靈罐金光迸裂、開光浮現月桂冠金色神魂光效。 |
| **REC-04** | Shot 5 | **6.5s** | **6.50s** | **9:16 (1080×1920)**<br>H.264 / 30fps | **怒氣滿額暴怒覺醒與三連斬擊**<br>雷歐戰鬥怒氣值累積滿 100%，怒氣滿額觸發「暴怒覺醒！」橘紅跳字與「暴怒中 · 屬性提升」，小白突刺揮斬對雷歐展開連續 3 次斬擊命中，雷歐生命值自 420 扣減至 369（戰鬥日誌即時結算 3 次 17 點暴擊傷害），獅衛重盾完好在手（無部位破壞演出）。 |

- **實機素材累計時長**：`4.5s + 8.0s + 5.0s + 6.5s = 24.0s`（加上 Shot 1 概念圖 3.0s 與 Shot 6 品牌點題卡 3.0s，剛好 30.0s 嚴絲合縫）。

---

## 二、素材交付檔案清單與存放路徑

所有素材已妥善存放於當前 Kanban Task Workspace 以及專案目錄中，供後續合成使用：

### 1. 9:16 直式影片素材（1080×1920，主要合成素材）
| 素材編號 | Workspace 路徑 | 專案交付路徑 (`docs/marketing/shots/`) | 檔案大小 | SHA256 (首8碼) |
|---|---|---|---|---|
| **REC-01** | `rec01_thumb_pad_9x16.mp4` | `docs/marketing/shots/rec01_thumb_pad_9x16.mp4` | 295 KB | `fdae23dc` |
| **REC-02** | `rec02_battle_polish_9x16.mp4` | `docs/marketing/shots/rec02_battle_polish_9x16.mp4` | 318 KB | `9a49c976` |
| **REC-03** | `rec03_soul_pity_9x16.mp4` | `docs/marketing/shots/rec03_soul_pity_9x16.mp4` | 78 KB | `6a262de7` |
| **REC-04** | `rec04_overdrive_break_9x16.mp4` | `docs/marketing/shots/rec04_overdrive_break_9x16.mp4` | 402 KB | `204487e6` |

### 2. 9:16 直式特寫裁切版影片素材（1080×1920，備用特寫剪輯）
| 素材編號 | Workspace 路徑 | 專案交付路徑 (`docs/marketing/shots/`) | 檔案大小 | SHA256 (首8碼) |
|---|---|---|---|---|
| **REC-01** | `rec01_thumb_pad_9x16_crop.mp4` | `docs/marketing/shots/rec01_thumb_pad_9x16_crop.mp4` | 261 KB | `de152cd2` |
| **REC-02** | `rec02_battle_polish_9x16_crop.mp4` | `docs/marketing/shots/rec02_battle_polish_9x16_crop.mp4` | 364 KB | `14a65842` |
| **REC-03** | `rec03_soul_pity_9x16_crop.mp4` | `docs/marketing/shots/rec03_soul_pity_9x16_crop.mp4` | 160 KB | `6545b409` |
| **REC-04** | `rec04_overdrive_break_9x16_crop.mp4` | `docs/marketing/shots/rec04_overdrive_break_9x16_crop.mp4` | 315 KB | `0f158039` |

### 3. 16:9 原始實機錄影母帶（1280×720，原始無損畫面）
| 素材編號 | Workspace 路徑 | 檔案大小 | SHA256 (首8碼) |
|---|---|---|---|
| **REC-01** | `rec01_thumb_pad_raw_16x9.mp4` | 263 KB | `8cf54fe1` |
| **REC-02** | `rec02_battle_polish_raw_16x9.mp4` | 268 KB | `946cbe5b` |
| **REC-03** | `rec03_soul_pity_raw_16x9.mp4` | 55 KB | `8beaf6d9` |
| **REC-04** | `rec04_overdrive_break_raw_16x9.mp4` | 324 KB | `273e643a` |

### 4. 關鍵幀縮圖與截圖證明（PNG，驗證真實畫面與 UI）
| 素材編號 | 9:16 關鍵幀縮圖路徑 | 縮圖大小 | 縮圖 SHA256 (首8碼) | 實機原生截圖路徑 | 驗證焦點 |
|---|---|---|---|---|---|
| **REC-01** | `docs/marketing/shots/rec01_thumb_pad_9x16_thumb.png` | 1,277 KB | `801843f9` | `docs/marketing/shots/rec01_thumb_pad.png` | 右側 ThumbPad 操作熱區、長劍揮斬與切換巨錘（經抽幀驗證無誤） |
| **REC-02** | `docs/marketing/shots/rec02_battle_polish_9x16_thumb.png` | 1,187 KB | `1d297531` | `docs/marketing/shots/rec02_battle_polish.png` | 小白 vs 雷歐、角色粗描邊與落地軟影、0.15s Hitstop 打擊停頓（經抽幀驗證無誤） |
| **REC-03** | `docs/marketing/shots/rec03_soul_pity_9x16_thumb.png` | 304 KB | `2f2e81b0` | `docs/marketing/shots/rec03_soul_pity.png` | 聚魂殿四階封靈罐並列（綠→藍→紫→橙）、虔誠度 60/100 · 再抽 4 次獲得碎片透明保底進度條、開光浮現月桂冠金色神魂光效（經抽幀驗證無誤） |
| **REC-04** | `docs/marketing/shots/rec04_overdrive_break_9x16_thumb.png` | 1,212 KB | `20740e7c` | `docs/marketing/shots/rec04_overdrive_break.png` | 怒氣滿額觸發「暴怒覺醒！」橘紅跳字與「暴怒中 · 屬性提升」＋三連斬擊命中雷歐（日誌連續 3 次 17 暴擊傷害、HP 扣至 369）（經抽幀逐格驗證無誤，無系統 emoji，無部位破壞與盾牌消失） |

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

本批素材錄製採用既有 Godot 引擎與 Linux Xvfb 虛擬顯示器配合 ffmpeg 擷取，並使用檔案握手信號確保場景與畫面完全繪製穩定：
- 驅動腳本：
  - `game/scripts/dev/capture_rec01_thumb.gd`
  - `game/scripts/dev/capture_rec02_polish.gd`
  - `game/scripts/dev/capture_rec03_soul.gd`
  - `game/scripts/dev/capture_rec04_break.gd`
- 自動批次錄影工具：`/root/record_shorts_recs.sh`
- 執行指令：
  ```bash
  /root/record_shorts_recs.sh /opt/side/bravesoul-game/.worktrees/t_6e7da2e3
  ```
  即可全自動重新錄製出上述所有 9:16、16:9 及關鍵幀截圖資產。
