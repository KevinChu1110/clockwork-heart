# 驗收查核表 (CHECKLIST) · ColossusLimitDialog 停擺巨偶限制彈窗新增前往戰力與前往鍛造快捷果凍按鈕 (t_5944b82b)

## 驗收項目逐項檢查

- [x] **按鈕規格與樣式**：
  - [x] 底部並列三顆果凍按鈕：`ConfirmButton`（確定）、`BtnGoPowerStat`（前往戰力）、`BtnGoForge`（前往鍛造）。
  - [x] 按鈕尺寸均為 `160x52px`，寬度 `>= 120px`、高度 `52px`，滿足 `>= 48px` 手機端熱區。
  - [x] 多巴胺色盤搭配：
    - `ConfirmButton`: 金黃色盤 `#FFD028`、邊框深藍紫 `#1F1A3A`、文字深藍紫 `#1F1A3A`、果凍厚底 `5px`、圓角 `18px`、字級 `18px`。
    - `BtnGoPowerStat`: 天藍色盤 `#38A0FF`、邊框深藍紫 `#1F1A3A`、文字深藍紫 `#1F1A3A`、果凍厚底 `5px`、圓角 `18px`、字級 `18px`。
    - `BtnGoForge`: 暖橘色盤 `#FFA010`、邊框深藍紫 `#1F1A3A`、文字深藍紫 `#1F1A3A`、果凍厚底 `5px`、圓角 `18px`、字級 `18px`。
  - [x] 100% 零系統 Emoji。
- [x] **點擊聯動與訊號**：
  - [x] 點擊 `BtnGoPowerStat`：發射 `power_stat_requested` 與 `closed` 訊號，安全關閉 `ColossusLimitDialog`（`queue_free` 無遮罩殘留），連動開啟 `PowerStatDialog`。
  - [x] 點擊 `BtnGoForge`：發射 `forge_requested` 與 `closed` 訊號，安全關閉 `ColossusLimitDialog`（`queue_free` 無遮罩殘留），連動開啟天宮鐵匠 `ForgeDialog`。
  - [x] 點擊 `ConfirmButton`：發射 `confirmed` 與 `closed` 訊號，安全關閉 `ColossusLimitDialog`。
- [x] **介面存取器與大廳方法**：
  - [x] `MobileLobby.show_colossus_limit_dialog() -> Control`
  - [x] `MobileLobby.get_colossus_limit_dialog() -> Control`
- [x] **六語系在地化 (i18n)**：
  - [x] `zh_TW`: 確定 / 前往戰力 / 前往鍛造
  - [x] `en`: OK / Go to Stats / Go to Forge
  - [x] `ja`: 確認 / 戦力詳細へ / 鍛造へ進む
  - [x] `ko`: 확인 / 전투력으로 이동 / 단조로 이동
  - [x] `es`: Aceptar / Ir a Estadísticas / Ir a Forja
  - [x] `zh_CN`: 确定 / 前往战力 / 前往锻造
  - [x] `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 均已更新且完全對齊。
  - [x] 支援動態語系即時切換更新。
- [x] **測試與存證**：
  - [x] 單元與整合測試 `test_colossus_limit_shortcuts.gd` 全部 PASS（`TEST_COLOSSUS_LIMIT_SHORTCUTS_OK`）。
  - [x] 8 張 OpenGL3 實機截圖完整產出且 SHA256 唯一無重複。
  - [x] Vision 視覺複檢通過，按鈕居中排版合理、無破圖穿模、無遮罩殘留、文字對比清晰。

## 截圖清單與 SHA256 存證

| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_colossus_limit_three_buttons_zh_TW.png` | 繁中 (zh_TW) 停擺巨偶限制彈窗三顆果凍按鈕（確定、前往戰力、前往鍛造） | 1280x720 | `46ed2e7aa6d181b847df41dd06848d8e634c9e251aa318bc787647cec74c1c31` |
| `proof_02_colossus_limit_en.png` | 英文 (en) 停擺巨偶限制彈窗三按鈕即時語系切換 (OK / Go to Stats / Go to Forge) | 1280x720 | `c43574d1685b89640ec91097f23f7d6b953d22942773901794d3e99f2099d771` |
| `proof_03_colossus_limit_ja.png` | 日文 (ja) 停擺巨偶限制彈窗三按鈕即時語系切換 (確認 / 戦力詳細へ / 鍛造へ進む) | 1280x720 | `4602597561d1950793e1acfbc3bcda70ebe705bc664c2558b9938fe9a7bb6129` |
| `proof_04_colossus_limit_ko.png` | 韓文 (ko) 停擺巨偶限制彈窗三按鈕即時語系切換 (확인 / 전투력으로 이동 / 단조로 이동) | 1280x720 | `38fb11cb8586c2223ecca246d4d4687ce9c541e4d79c075eb2a759e20f58222d` |
| `proof_05_colossus_limit_es.png` | 西班牙文 (es) 停擺巨偶限制彈窗三按鈕即時語系切換 (Aceptar / Ir a Estadísticas / Ir a Forja) | 1280x720 | `c2e72bd2bc5c3f36711a9b4670483beb24a6154a700461e9f093b1b4eb53a0a3` |
| `proof_06_colossus_limit_zh_CN.png` | 簡中 (zh_CN) 停擺巨偶限制彈窗三按鈕即時語系切換 (确定 / 前往战力 / 前往锻造) | 1280x720 | `72fda614edfde607311a6ceaa1b440c2d62d7e6ea6a5fefdcadbf6376138da9f` |
| `proof_07_click_go_power_stat_opens_power_stat_dialog.png` | 點擊『前往戰力』後安全關閉限制彈窗並連動開啟 PowerStatDialog 戰力屬性總覽 | 1280x720 | `227b97a90af5bf75cc74ef775e5046db5f0f8f5466122bfb72d7b3447cd9f74b` |
| `proof_08_click_go_forge_opens_forge_dialog.png` | 點擊『前往鍛造』後安全關閉限制彈窗並連動開啟天宮鐵匠 ForgeDialog | 1280x720 | `ada0cff385a89574f79cebb2c454f6aab2ed4c8333b8a5ff4ad515bfa2f2c348` |
