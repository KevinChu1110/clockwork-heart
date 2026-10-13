# 實機驗收證明 · SkillDialog 底欄新增前往木人樁試招按鈕連動大廳 (t_58757a2f)

## 1. 任務背景與驗收目標
依據看板卡片 `t_58757a2f` 需求與手遊人體工學／多巴胺視覺規範：
1. **SkillDialog 底欄按鈕配置**：在 SkillDialog 底部控制列（關閉按鈕旁）新增『前往木人樁試招』多巴胺立體果凍按鈕（按鈕名稱 `BtnPracticeDummy`，高 50px、熱區 >= 48px、天藍果凍色盤 `#38A0FF`、圓角 18px、底邊厚底 5px）。右側保留既有暖橘（`#FFA010`）『關閉』果凍按鈕（`BtnCloseBottom`），形成底部左右分列佈局。
2. **自定義信號與平滑關閉**：點擊該按鈕時發出 `practice_dummy_requested` 自定義信號，並平滑發出 `closed` 信號呼叫 `queue_free()` 關閉彈窗。
3. **大廳連動切換木人樁**：在 `mobile_lobby.gd` 的 `open_skill_dialog()` 中連接該信號，觸發 `request_battle("training_dummy")`，平滑切換至零消耗木人樁戰鬥場景，讓玩家在大廳能立即實機驗證配招手感。
4. **六語系即時切換**：支援六語系即時在地化切換（`zh_TW: 前往木人樁試招`、`zh_CN: 前往木人桩试招`、`en: Practice at Training Dummy`、`ja: 木人で試技する`、`ko: 목인 연습하기`、`es: Practicar con el muñeco`）。
5. **單元測試與無頭檢驗**：撰寫 `test_skill_dialog_dummy_practice.gd` 達成 0 SCRIPT ERROR，全項通過（`SKILL_DIALOG_DUMMY_PRACTICE_OK`）。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **底欄木人樁試招按鈕單元測試** | `godot --path game --headless -s res://scripts/ui/test_skill_dialog_dummy_practice.gd` | 4/4 項全部通過（`SKILL_DIALOG_DUMMY_PRACTICE_OK`） | **PASS** |
| **招式優先出招膠囊標籤回歸** | `godot --path game --headless -s res://scripts/ui/test_skill_priority_badge.gd` | 4/4 項全部通過（`SKILL_PRIORITY_BADGE_OK`） | **PASS** |
| **武術館試招按鈕回歸測試** | `godot --path game --headless -s res://scripts/ui/test_skill_panel_dummy_btn.gd` | 4/4 項全部通過（`TEST_SKILL_PANEL_DUMMY_BTN_OK`） | **PASS** |
| **素材與匯入狀態檢查** | `/root/bin/clock-check .` | 0 缺 .import、0 斷鏈、0 軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_58757a2f/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 4 張實機全景截圖與 3 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - SkillDialog 底欄『前往木人樁試招』按鈕尺寸：寬 210px、高 50px（>= 50px）、熱區 >= 48px、圓角 18px、底邊厚底 5px。
  - 色盤合規：左側天藍色盤（`COLOR_SKY` #38A0FF），右側保留暖橘色盤（`COLOR_ORANGE` #FFA010），立體陰影層次分明。
  - 排版合規：彈窗底部左右分列，中間透過 `BottomSpacer` 彈性間隔撐開，避免誤觸且兩拇指操作舒適。
- [x] **0-QA24 / 0-QA25（多語系即時切換）**：
  - 繁中（前往木人樁試招）、簡中（前往木人桩试招）、英文（Practice at Training Dummy）、日文（木人で試技する）、韓文（목인 연습하기）、西文（Practicar con el muñeco）切換自如，無 CJK 殘留與重疊。
- [x] **100% 零系統原生 Emoji**：按鈕與介面文字完全使用純淨文字與自製樣式，無系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_skill_dialog_dummy_practice_btn_zh_TW.png` | `f2e822928291b775c291ca495bb0330e52ec37bb83f58a008f4e7aea6c15d595` | `1fb851f3927c81e2ee112a07b54c3e5f` | SkillDialog 底欄左側天藍『前往木人樁試招』與右側暖橘『關閉』果凍按鈕左右分列全景 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_skill_dialog_dummy_btn_en.png` | `4e317f45cc485c6c21002fbfb3f8977f199ddcf8754720829922cf1cd75d90ac` | `2bb8427ee8ea5b504aa56ba52564fcde` | 英文語系（Practice at Training Dummy）即時在地化全景，排版平整無穿模 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_skill_dialog_dummy_btn_ja.png` | `83feaf16c1eebe665f66ca4d43e82eff64cfe05c41f6eab7a65b66804e9c903f` | `20247bd230db4074a75bfd7ada809b44` | 日文語系（木人で試技する）即時在地化全景，新字體漢字合規無截字 | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_lobby_trigger_training_dummy_battle.png` | `f19ddcdd0cc939bf840954ab0210afeba74c608f3b9cbd29d5a90b60818d15be` | `2a49c93ba96e24c42d699638f207037b` | 點擊試招按鈕後平滑關閉彈窗並切換至零消耗木人樁戰鬥場景實機存證 | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/)

| 特寫檔名 | SHA256 | MD5 | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_dummy_btn_zh_TW.png` | `bb762d80d67e6a31317f2d3d568285fb` | `bb762d80d67e6a31317f2d3d568285fb` | 760x100 | SkillDialog 底欄繁中左側天藍試招按鈕與右側暖橘關閉按鈕特寫 | **PASS** |
| `crop_02_dummy_btn_en.png` | `cc30b212227b50254258163844b5024c` | `cc30b212227b50254258163844b5024c` | 760x100 | 底欄英文版『Practice at Training Dummy』按鈕特寫，手遊防誤觸標準 | **PASS** |
| `crop_03_dummy_btn_ja.png` | `82b16c77fa62bcb3ce8b8096fe85d91b` | `82b16c77fa62bcb3ce8b8096fe85d91b` | 760x100 | 底欄日文版『木人で試技する』按鈕特寫，圓角 18px、厚底 5px | **PASS** |
