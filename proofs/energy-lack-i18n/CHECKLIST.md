# 體力不足彈窗六語系即時刷新 驗收清單 (energy-lack-i18n)

## 1. 任務目標
玩家打開體力不足彈窗後再切語系，標題、能量數字、說明、看廣告鈕、稍後再來仍停在開啟當下的語言。本任務完成：
1. 彈窗上所有玩家可見字走 ContentLoc（含 能量不足／當前能量／說明／觀看廣告回復／稍後再來／次數上限／已移除廣告直接領取）。
2. 接 `Loc.locale_changed`，開著彈窗切語系整窗即時刷新。
3. 六語系詞條補齊（`zh_TW` 缺的 key 一併補入 `zh_TW/ui.json`，避免只靠 fallback；頂部 HUD 分鐘單位 `%d分` 補齊六語系）。
4. 廣告發獎數值保持 +3 能量、每日次數上限 3/3 不變。
5. 橫屏寬度 750px（740～760px）、右上關閉按鈕 50x50px（≥50px）、全程零系統 emoji。

## 2. 交付檔案
- **彈窗核心**：`game/scripts/ui/energy_lack_dialog.gd`
  - 增加 `_enter_tree()` / `_exit_tree()` / `_connect_loc_signal()` / `_disconnect_loc_signal()` / `_on_locale_changed()`
  - 增加 `_update_ui_texts()`，更新 `_title_lbl`、`_back_btn` 並呼叫 `_refresh_display()`
  - UI 重構時命名節點 `TitleLbl`, `BackBtn`, `WatchAdBtn`, `EnergyValLabel`, `StatusDetailLabel`, `DescLbl`，防止重複建立
- **大廳頂欄分鐘多語系**：`game/scripts/ui/mobile_lobby.gd`
  - 頂欄能量倒數改走 `_t("%d分")`，消除英文/西文下的 CJK 漢字殘留 `分`
- **六語系詞條補齊**：
  - `game/data/i18n/content/zh_TW/ui.json`（補齊 14 組體力不足彈窗鍵與 `%d分`）
  - `game/data/i18n/content/{zh_CN,en,ja,ko,es}/ui.json`（補齊 `%d分`）
- **具名單元測試**：`game/scripts/ui/test_energy_lack_i18n.gd`
- **實機截圖腳本**：`tools/capture_energy_lack_i18n.gd`
- **實機截圖存證（0-QA23 獨立目錄）**：
  - `proofs/energy-lack-i18n/proof_01_energy_lack_en.png`（英文全景實機，背後大廳同步切換 en，0-QA25）
  - `proofs/energy-lack-i18n/crops/crop_01_energy_lack_en.png`（英文彈窗局部裁切）
  - `proofs/energy-lack-i18n/proof_02_energy_lack_ja.png`（日文全景實機，背後大廳同步切換 ja，0-QA25）
  - `proofs/energy-lack-i18n/crops/crop_02_energy_lack_ja.png`（日文彈窗局部裁切）
  - `proofs/energy-lack-i18n/proof_03_energy_lack_zh_TW.png`（繁中全景基準對照）
  - `proofs/energy-lack-i18n/crops/crop_03_energy_lack_zh_TW.png`（繁中彈窗局部裁切）

## 3. 六語系詞條映射對照表

| Key | zh_TW | zh_CN | en | ja | ko | es |
|---|---|---|---|---|---|---|
| `能量不足` | `能量不足` | `能量不足` | `Insufficient Energy` | `エネルギー不足` | `에너지 부족` | `Energía insuficiente` |
| `當前能量：%d／%d` | `當前能量：%d／%d` | `当前能量：%d／%d` | `Current Energy: %d/%d` | `現在のエネルギー：%d／%d` | `현재 에너지: %d/%d` | `Energía actual: %d/%d` |
| `稍後再來` | `稍後再來` | `稍后再来` | `Come Back Later` | `後で来る` | `나중에 오기` | `Volver más tarde` |
| `觀看廣告回復能量 (+3)  (%d/%d)` | `觀看廣告回復能量 (+3)  (%d/%d)` | `观看广告恢复能量 (+3)  (%d/%d)` | `Watch Ad to Restore Energy (+3)  (%d/%d)` | `広告を見てエネルギー回復 (+3)  (%d/%d)` | `광고 보고 에너지 회복 (+3)  (%d/%d)` | `Ver anuncio y recuperar energía (+3)  (%d/%d)` |
| `已移除廣告，直接領取 (+3)  (%d/%d)` | `已移除廣告，直接領取 (+3)  (%d/%d)` | `已移除广告，直接领取 (+3)  (%d/%d)` | `Ads Removed, Claim Directly (+3)  (%d/%d)` | `広告削除済み、直接受取 (+3)  (%d/%d)` | `광고 제거됨, 즉시 수령 (+3)  (%d/%d)` | `Anuncios eliminados, reclamar directamente (+3)  (%d/%d)` |
| `今日廣告次數已達上限 (0/%d)` | `今日廣告次數已達上限 (0/%d)` | `今日广告次数已达上限 (0/%d)` | `Daily ad limit reached (0/%d)` | `本日の広告上限に達しました (0/%d)` | `오늘 광고 횟수 상한 도달 (0/%d)` | `Límite de anuncios diario alcanzado (0/%d)` |
| `今日領取次數已達上限 (0/%d)` | `今日領取次數已達上限 (0/%d)` | `今日领取次数已达上限 (0/%d)` | `Daily claim limit reached (0/%d)` | `本日の受取上限に達しました (0/%d)` | `오늘 수령 횟수 상한 도달 (0/%d)` | `Límite de reclamos diario alcanzado (0/%d)` |
| `%d分` | `%d分` | `%d分` | `%d min` | `%d分` | `%d분` | `%d min` |

## 4. 驗收規範審核結果 (review.md)

- [x] **0-QA23（獨立 proof 目錄）**：所有實機截圖與裁切圖嚴格存放在 `proofs/energy-lack-i18n/`，無修改或覆蓋其他任務之 proof。
- [x] **0-QA24（日／韓漢字核實、英文與西文無 CJK 殘留）**：
  - 英文全景中，彈窗標題為 `Insufficient Energy`、按鈕為 `Watch Ad to Restore Energy (+3) (3/3)`、`Come Back Later`，頂部 HUD 為 `Energy 2/15 30 min`，零 CJK 漢字殘留。
  - 日文全景中，漢字（エネルギー不足、現在のエネルギー、広告、回復、受取、後で来る、満タン）均核實符合日本語當用漢字標準。
- [x] **0-QA25（彈窗以外同屏同步換語系）**：
  - 實機截圖中，頂部 Header、大廳左側四殿堂、右側裝備與出征、底部 Dock（Cogwheel Hamlet, Hero Gear, Four Regions, Soul Hall, Adventure Bag / ぜんまい新村, キャラ装備, 四区出征, 聚魂殿, 冒險バッグ）均同步切換為該語系，無繁中殘留。
- [x] **零系統 Emoji**：所有介面與按鈕均無系統 emoji。
- [x] **尺寸規範**：橫屏寬度 750px（介於 740～760px），右上關閉按鈕 50x50px（≥50px）。

## 5. 測試執行命令與驗證記錄

```bash
# 1. 無頭冒煙測試（0 SCRIPT ERROR）
godot --path game --headless --quit-after 3

# 2. 具名六語系即時切換單元測試
godot --path game --headless -s res://scripts/ui/test_energy_lack_i18n.gd

# 3. 去廣告既有測試回歸
godot --path game --headless -s res://scripts/systems/test_remove_ads_mock.gd
```
