# 驗收證明與常見退回自查報告 (t_a9ea5a87)

- **任務標題**：🎮 遊戲開發｜MapleInventory 探索背包機芯詳情新增『前往校準』快捷按鈕連動天宮鐵匠
- **任務卡號**：t_a9ea5a87
- **分支名稱**：agent/20261012-maple-inventory-calibrate-shortcut-t_a9ea5a87
- **執行人員**：發條之心·工程師 阿翔 (sideworker2)
- **送審對象**：測試／審查員 小婷 (sideqa)

---

## 一、驗收項目與達成狀況

1. **按鈕規格與立體果凍樣式**：
   - 節點名稱：`BtnGoCalibrate`，高度 `52px`（>= 48px），熱區 >= 48px，金黃果凍厚底（`COLOR_GOLD #FFD028`，深藍紫描邊 2px `COLOR_BORDER #1F1A3A`，底邊厚底 5px，圓角 18px）。
   - 字級規格：粉圓體 18px（>= 16px），深藍紫字色 `#1F1A3A`，零系統 Emoji。
   - ✅ 驗證通過（單元測試斷言 PASS，實機渲染比對 PASS）。

2. **按鈕顯示與可用性判斷邏輯**：
   - 未選取物品或選取非機芯物品（裝備、消耗品、素材）時：按鈕隱藏（`visible == false`）。
   - 選取未裝備機芯時：按鈕顯示但置灰禁用（`disabled == true`）。
   - 選取已裝備但剩餘校準次數已滿（<=0）機芯時：按鈕顯示但置灰禁用（`disabled == true`）。
   - 選取已裝備且剩餘校準次數 > 0 機芯時：按鈕顯示且高亮可用（`disabled == false`）。
   - ✅ 驗證通過（覆蓋全部狀態分支）。

3. **信號發射與連動天宮鐵匠閉環**：
   - 點擊 `BtnGoCalibrate` 觸發 `calibrate_requested` 信號發射。
   - 同步關閉探索背包（`_inv.visible == false`）並開啟天宮鐵匠 `ForgeDialog`，形成「背包檢查機芯 → 前往校準 → 鐵匠校準強化」養成跳轉閉環。
   - ✅ 驗證通過（信號捕捉 PASS，ForgeDialog 掛載與實機截圖 PASS）。

4. **六語系即時切換在地化**：
   - 支援六語系即時切換：
     - `zh_TW`: 前往校準
     - `zh_CN`: 前往校准
     - `en`: Calibrate
     - `ja`: 較正へ
     - `ko`: 교정하러 가기
     - `es`: Calibrar
   - 歐美語系零 CJK 殘留、全畫面零系統 Emoji。
   - ✅ 驗證通過（六語系斷言全部 PASS）。

---

## 二、實機截圖存證清單 (proofs/t_a9ea5a87/)

| 截圖檔名 | 解析度 | 驗證重點 | SHA256 (前 16 碼) | Vision 自檢結果 |
|---|---|---|---|---|
| `proof_01_core_equipped_calibratable_zh_tw.png` | 1280x720 | 繁中已裝備機芯，BtnGoCalibrate 高亮可用 | `a668a08a75545dd0` | ✅ 通過（金黃果凍厚底，文字清晰無 Emoji，排版對齊正常） |
| `proof_02_core_unequipped_disabled.png` | 1280x720 | 未裝備機芯，BtnGoCalibrate 置灰禁用 | `1eb902a11337a453` | ✅ 通過（置灰狀態明確，防誤觸保護正常） |
| `proof_03_core_maxed_disabled.png` | 1280x720 | 校準次數已滿機芯，BtnGoCalibrate 置灰禁用 | `737d7ce26457f96b` | ✅ 通過（剩餘 0 次時禁用置灰正常） |
| `proof_04_forge_dialog_opened.png` | 1280x720 | 點擊前往校準後，成功開啟天宮鐵匠 ForgeDialog | `b2ca80129a8229c5` | ✅ 通過（天宮鐵匠彈窗居中開啟，五槽機芯清晰，無破圖無重疊） |
| `proof_05_calibrate_shortcut_zh_CN.png` | 1280x720 | 簡體中文即時切換（前往校准） | `466873715fafe898` | ✅ 通過（字級符合，簡中文字無誤） |
| `proof_06_calibrate_shortcut_en.png` | 1280x720 | 英文即時切換（Calibrate） | `61e87f5d5b7e1cc0` | ✅ 通過（英文字體排版完整，零 CJK 殘留，零 Emoji） |
| `proof_07_calibrate_shortcut_ja.png` | 1280x720 | 日文即時切換（較正へ） | `d3710e4e317636b2` | ✅ 通過（日文文字正常顯示無缺字） |
| `proof_08_calibrate_shortcut_ko.png` | 1280x720 | 韓文即時切換（교정하러 가기） | `61c82b4d81c6e981` | ✅ 通過（韓文文字正常顯示無截斷） |
| `proof_09_calibrate_shortcut_es.png` | 1280x720 | 西班牙文即時切換（Calibrar） | `f0f9e0e37e6cf97c` | ✅ 通過（西班牙文無 CJK 殘留，零 Emoji） |

*備註：9 張截圖 SHA256 均獨立且互異，無重複或黑屏。*

---

## 三、常見審查退回清單逐項自查

對照 `~/.hermes/shared/clock-review-checklist.md`：
1. **驗證截圖存證**：✅ 已自查。時序精準控制等待幀數，確保 Viewport 與語系渲染完成，9 張截圖 SHA256 完全互異，無黑屏無穿模，已使用 Vision 仔細檢視確認。
2. **單元測試穩定度**：✅ 已自查。無頭測試包含 `DisplayServer.get_name() != "headless"` 防護，`run_tests.sh` 穩定跑綠（17/17 PASS），無 flake。
3. **佈局尺寸與熱區**：✅ 已自查。按鈕高度 52px（>= 48px），熱區 >= 48px，字級 18px（>= 16px），立體厚底 5px，描邊 2px，無 (0,0) 坍塌。
4. **零系統 Emoji**：✅ 已自查。全節點純文字與手繪風格，無 Unicode 系統 Emoji。
5. **程式與邏輯完整**：✅ 已自查。`_get_selected_core_part()` 同步支援 `core_slots` 裝備部件讀取，校準次數與狀態流轉正確。
6. **專案狀態更新**：✅ 已自查。`PROJECTS.json` 已透過 `project_status.py` 更新為「測試中」。
7. **工作區狀態**：✅ 已自查。全部修改完整提交至分支 `agent/20261012-maple-inventory-calibrate-shortcut-t_a9ea5a87`。
8. **clock-check**：✅ 已自查。執行 `/root/bin/clock-check /opt/side/bravesoul-game` 結論：全過（0 missing .import, 0 dead loc keys, 0 old terms）。
