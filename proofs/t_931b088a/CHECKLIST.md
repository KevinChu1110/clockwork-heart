# 驗收自查清單 · PowerStatDialog 戰力屬性總覽新增稱號卡片與前往稱號牆快捷按鈕 (t_931b088a)

## 任務基本資訊
- **卡號**：`t_931b088a`
- **負責人**：阿翔（`sideworker2`）
- **工作分支**：`agent/20261013-power-stat-title-shortcut-t_931b088a`
- **審查員**：小婷（`sideqa`）

---

## 驗收規範自查項目

### 1. 卡片規格與多巴胺視覺
- [x] **卡片識別**：節點名稱為 `TitleCard`，在 `power_stat_dialog.gd` 中緊接於機芯部件卡片（`_build_core_parts_card`）之後。
- [x] **標題列與膠囊**：
  - 標題列標題為「佩戴稱號」（`TitleCardTitleLabel`），文字字級 14px 加粗深藍紫字（`COLOR_TEXT_DARK`）。
  - 當前佩戴稱號名稱膠囊（`TitleCapsule` + `TitleNameLabel`），金黃底板 `COLOR_CARD_GOLD`、圓角 10px、底邊 3px，預設未佩戴時顯示「初出茅廬」，更換稱號即時連動。
  - 卡片下方附有灰色提示說明（`TitleDescLabel`）：「佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下」。
- [x] **快捷按鈕**：
  - 按鈕節點名稱為 `BtnGoTitleWall`，操作列提供天藍色盤 `#38A0FF`（`COLOR_SKY`）立體果凍按鈕。
  - 尺寸熱區：`custom_minimum_size` 設定為寬 110px、高 48px（滿足高度 >= 48px 手機端人因規格）。
  - 樣式：圓角 16px，底邊厚底 4px，字級 14px，深藍紫描邊 `#1F1A3A`（`COLOR_BORDER`），奶油白高亮字帶深色描邊。
- [x] **零系統 Emoji**：按鈕、標題、膠囊與說明文字無任何原生 Emoji。

### 2. 點擊連動與功能閉環
- [x] **訊號發射**：提供 `title_wall_requested` 訊號與 `get_go_title_wall_button()` 存取器。
- [x] **點擊連動**：點擊 `BtnGoTitleWall` 發射 `title_wall_requested` 訊號並安全關閉 `PowerStatDialog`。
- [x] **大廳直通**：`MobileLobby.open_power_stat_dialog()` 監聽 `title_wall_requested` 訊號，連動開啟 `TitleWallDialog`（`MobileLobby.open_title_wall_dialog()`），完成屬性總覽至稱號牆閉環。

### 3. 六語系 i18n 完整支援
- [x] **字典完整性**：於 `game/data/i18n/content/<lang>/ui.json` 與 `game/data/i18n/<lang>.json` 補齊六語系鍵值：
  - `power_stat.title_card`:
    - `zh_TW`: `佩戴稱號`
    - `zh_CN`: `佩戴称号`
    - `en`: `Equipped Title`
    - `ja`: `称号`
    - `ko`: `칭호`
    - `es`: `Título Equipado`
  - `power_stat.btn_go_title_wall`:
    - `zh_TW`: `前往稱號`
    - `zh_CN`: `前往称号`
    - `en`: `Go to Titles`
    - `ja`: `称号一覧へ`
    - `ko`: `칭호로 이동`
    - `es`: `Ir a Títulos`
  - `power_stat.title_desc`:
    - `zh_TW`: `佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下`
    - `zh_CN`: `佩戴称号展现专属荣耀，前往称号墙可自由切换或卸下`
    - `en`: `Equip titles to showcase glory. Visit titles to switch or unequip.`
    - `ja`: `称号を身につけて栄誉を示そう。称号一覧で変更・解除できます。`
    - `ko`: `칭호를 착용하여 영광을 드러내세요. 칭호 벽에서 변경하거나 해제할 수 있습니다.`
    - `es`: `Equipa títulos para mostrar tu gloria. Ve a títulos para cambiar o desequipar.`
- [x] **即時切換**：`Loc.locale_changed` / `ContentLoc` 在語系變更時即時刷新標題、膠囊、說明與按鈕文字。

---

## 審查常見退回自查（對照 checklist）
- **實機截圖與 UI 排版**：✅ 已於 1280x720 橫屏環境實機渲染，按鈕高度 48px、文字 14px，排版留白充足無切字或遮蔽，滾動至底部卡片完整顯示。
- **點擊熱區**：✅ BtnGoTitleWall 寬 110px、高 48px，符合 >= 48px 手機端標準。
- **測試穩定性 (Flaky 防護)**：✅ 測試腳本精準控制幀數，手動推進等待幀保證 UI 與語系渲染完成，無頭與虛擬桌面環境皆綠。
- **無頭測試防護**：✅ 截圖比對防護 `DisplayServer.get_name() != "headless"`，確保 `run_tests.sh` 穩定跑綠。
- **工作區乾淨**：✅ 所有檔案均已 commit 至 `agent/20261013-power-stat-title-shortcut-t_931b088a`，工作區無 untracked 或 modified 檔案。
- **專案狀態**：✅ 已使用 `project_status.py` 將 `power-stat-title-shortcut` 更新為「測試中」。

---

## 實機截圖存證清單 (proofs/t_931b088a/)
| 檔案名稱 | 說明 | SHA256 雜湊 (前 16 碼) |
|---|---|---|
| `proof_01_zh_TW_power_stat_title_card_default.png` | 繁中戰力總覽展示稱號卡片，預設佩戴初出茅廬與天藍前往稱號按鈕 | `636ce10d7456920b` |
| `proof_02_zh_TW_power_stat_title_card_equipped_special.png` | 繁中戰力總覽佩戴特殊稱號，膠囊動態刷新為「以劍抵爪」 | `8ea602f0459206ce` |
| `proof_03_zh_TW_title_wall_opened_from_power_stat.png` | 點擊前往稱號按鈕後關閉屬性總覽，直通連動開啟大廳稱號牆視窗 | `596d93f5b8b6211b` |
| `proof_04_en_power_stat_title_card.png` | 英文語系 Equipped Title、Fledgling Novice 膠囊與 Go to Titles 按鈕 | `fea6fac71a74a61d` |
| `proof_05_ja_power_stat_title_card.png` | 日文語系 称号、駆け出し 膠囊與 称号一覧へ 按鈕 | `1d3df5579b48e735` |
| `proof_06_ko_power_stat_title_card.png` | 韓文語系 칭호、풋내기 모험가 膠囊與 칭호로 이동 按鈕 | `323e10d161d441d9` |

六張截圖雜湊彼此相異，無重複或假存證。
