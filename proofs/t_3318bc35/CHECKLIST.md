# 聚魂召喚系統（soul_draw）清除特殊符號『✦』殘留與合規對齊 驗收查驗清單 (t_3318bc35)

## 任務目標
1. 清除 `soul_ten_pull_view.gd`、`soul_summon_fx.gd` 與 `soul_result_card_view.gd` 中所有『✦』特殊字型符號裝飾與星星字串。
2. 標題與引導文字改為純淨文本（如『封靈連轉結果』、『發條解鎖 · 聚魂召喚』），星級展示對齊官方品質色階純文字階級。
3. 同步清理與對齊六語系 `ui.json` 及 `<locale>.json` 對應字典項目，確保各語系皆無特殊符號殘留。

## 查驗項目與執行結果

### 1. 程式碼與字典特殊字符清理
- [x] `soul_ten_pull_view.gd`：標題自 `✦ 封靈連轉結果 ✦` 改為純淨文本 `封靈連轉結果`，`TIER_COLORS` 中 `stars` 星星字串全部清空，卡片頂部改為純文字階級 `_t(str(tier_data.get("name", "")))`。
- [x] `soul_summon_fx.gd`：提示文字自 `✦ 發條解鎖 · 聚魂召喚 ✦` 改為純淨文本 `發條解鎖 · 聚魂召喚`，右上角跳過按鈕自 `跳過 >>` 對齊純文字 `跳過`，接入 `ContentLoc` 與 `locale_changed` 信號支援六語系即時切換。
- [x] `soul_result_card_view.gd`：佔位符星級自 `✦ ✦ ✦ ✦ ✦` 改為純文字階級 `傳奇`，掉落卡星級展示自星星字串改為純文字階級（普通/優良/稀有/史詩/傳奇/神話），`TIER_COLORS` 中 `stars` 星星字串全部清空。
- [x] 六語系字典（`game/data/i18n/content/*/ui.json` 與 `game/data/i18n/*.json`）：完全移除 `✦ 封靈連轉結果 ✦`，新增 `封靈連轉結果`、`發條解鎖 · 聚魂召喚` 與品質色階純文字階級字典。全字典檢索 `✦` 結果為 0。

### 2. 實機渲染存證截圖 (1280x720)
| 截圖檔名 | 說明 | 規格與狀態 | SHA256 雜湊值 |
|---|---|---|---|
| `proof_01_soul_draw_idle.png` | 聚魂殿堂抽卡首頁未抽狀態 | 1280x720 PNG | `d3f9e8806e66149f536e49b29e663ec464ecd774896672002e76afa8435f95e0` |
| `proof_02_summon_ritual_burst.png` | 召喚儀式爆散高峰（純淨文本『發條解鎖 · 聚魂召喚』、『跳過』） | 1280x720 PNG | `c1c79eeb9468de7b3d66698f949280b1a0e0ee50189b1b9379126f4e7d0af196` |
| `proof_03_soul_single_pull_result.png` | 單抽結果卡（純文字階級『史詩』、多巴胺果凍色階光框、零星星符號） | 1280x720 PNG | `a5e73792fae27df3545f8ac6138e33a47952f3a153833ae0087f0b29fb882b1a` |
| `proof_04_soul_ten_pull_result.png` | 十連抽結果面板（純淨標題『封靈連轉結果』、各卡頂部純文字階級） | 1280x720 PNG | `5634aab832de61e32f656e46cde5ad6579aa10db8e50cc5f11a562bb0e61c4cd` |

### 3. 無頭測試與合規斷言
- [x] `test_soul_draw_clean_compliance.gd`：新增無頭合規測試，覆蓋六語系標題、提示文字、跳過按鈕、十連抽面板、單抽結果卡之純文字階級與零特殊字符斷言（`TEST_SOUL_DRAW_CLEAN_COMPLIANCE_OK`）。
- [x] `test_soul_draw_i18n.gd`：既有六語系即時切換測試全數通過（`TEST_SOUL_DRAW_I18N_OK`）。
- [x] `./tools/run_tests.sh`（filter=soul）：5 項相關測試全綠（`TESTS PASSED (5/5)`）。
- [x] `godot --path game --headless --quit-after 3`：冒煙測試 0 報錯、0 Script Error。
