# 驗收清單：PowerStatDialog 戰力屬性總覽武器卡片新增『前往鍛造』快捷按鈕連動天宮鐵匠 (t_7716e1d4)

## 1. 任務核心驗收標準對齊
- [x] **WeaponLoadoutCard 標題列新增『前往鍛造』果凍按鈕 (BtnGoForge)**：
  - 在 `game/scripts/ui/power_stat_dialog.gd` 之 `WeaponLoadoutCard` 標題列（`t_row`）右側新增「前往鍛造」立體果凍按鈕（`BtnGoForge`）。
  - 熱區尺寸嚴格符合手遊端防誤觸規範（`custom_minimum_size = Vector2(96, 48)`，高度 >= 48px，熱區 >= 48px）。
  - 配色採多巴胺金黃果凍厚底風格（`COLOR_GOLD` `#FFD028`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A` 2px、底部立體厚底 5px、圓角 14px、陰影 4px），文字採深藍紫加粗（14px，>=14px），達成零系統 Emoji。
  - 與下方的寶石卡片『前往工坊』、心法卡片『前往心法』、戰魂卡片『前往聚魂』、機芯卡片『前往校準』形成統一的五大養成跳轉閉環。
- [x] **發出 forge_requested 信號並連動天宮鐵匠 ForgeDialog**：
  - 點擊按鈕後發出 `forge_requested` 信號，同時發出 `closed` 信號並安全釋放關閉戰力總覽彈窗。
  - 大廳 `MobileLobby`（`game/scripts/ui/mobile_lobby.gd`）之 `open_power_stat_dialog()` 監聽 `forge_requested` 並連動呼叫 `open_forge()` 開啟天宮鐵匠彈窗，讓玩家可直接對武器進行強化升階與副詞條鍛造。
- [x] **六語系即時切換多國語言支援**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 六大語系即時切換無缺失。
  - 各語系按鈕文字精確對齊（zh_TW="前往鍛造", zh_CN="前往锻造", en="Go to Forge", ja="鍛造へ進む", ko="단조로 이동", es="Ir a Forja"）。
  - 歐美語系 (en, es) 零 CJK 漢字殘留，全語系零系統 Emoji。
- [x] **專屬單元驗收測試與真實 OpenGL3 實機截圖**：
  - 新增 `game/scripts/ui/test_power_stat_weapon_forge_shortcut.gd` 覆蓋全部按鈕規格、信號發射、六語系切換與大廳連動斷言。
  - 產出 7 張真實 OpenGL3 實機 Framebuffer 截圖至 `proofs/t_7716e1d4/`，SHA256 各自獨立不重複。

---

## 2. 測試與驗證結果
- **專屬單元測試**：
  - `TEST_FILTER=test_power_stat_weapon_forge_shortcut ./tools/run_tests.sh`：1/1 PASS（100% 全綠，TEST_POWER_STAT_WEAPON_FORGE_SHORTCUT_OK，exit code 0）。
- **PowerStatDialog 相關回歸測試**：
  - `TEST_FILTER=test_power_stat ./tools/run_tests.sh`：6/6 PASS（全數通過，無任何回歸破壞）。
- **無頭冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /opt/side/bravesoul-game`
  - 檢查素材 .import、路徑、autoload、多語系 key 與舊名詞全數通過。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_7716e1d4/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下透過真實 Viewport Framebuffer 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_power_stat_weapon_forge_shortcut_zh_tw.png` | 繁中 (zh_TW) 戰力總覽三欄武器卡片與 BtnGoForge 金黃果凍按鈕（96x48px，字級 14px） | `06de6c3d0a5d11aa911c1e0110e28671148a7bed662cec01007a9c5d8e13780b` |
| `proof_02_power_stat_weapon_forge_shortcut_zh_cn.png` | 簡中 (zh_CN) 戰力總覽三欄武器卡片『前往锻造』按鈕展示 | `7b18bae8a5fb1a88f1fca72d0e8122af4162acb1cde7abf7be46daf87e4f58d1` |
| `proof_03_power_stat_weapon_forge_shortcut_en.png` | 英文 (en) 戰力總覽三欄武器卡片『Go to Forge』按鈕展示，零 CJK 殘留 | `5c91f2b350c911fd1ab54229a1eb7558ed1398a258ca95f2bd8e387b2595e78c` |
| `proof_04_power_stat_weapon_forge_shortcut_ja.png` | 日文 (ja) 戰力總覽三欄武器卡片『鍛造へ進む』按鈕展示 | `293f57dcb06b20bf2eef49266560b8fc5cdb2aad54a6dc779ebedc7d9e9accc8` |
| `proof_05_power_stat_weapon_forge_shortcut_ko.png` | 韓文 (ko) 戰力總覽三欄武器卡片『단조로 이동』按鈕展示 | `67fb6678927a24d652324e7c5785e23330fff25bc54cc74c1cf2fd7565d3f685` |
| `proof_06_power_stat_weapon_forge_shortcut_es.png` | 西文 (es) 戰力總覽三欄武器卡片『Ir a Forja』按鈕展示，零 CJK 殘留 | `744c3b2d2776423bd061fed17ebf16395b10bbaa4fa090063de7adbd8ffc7ac5` |
| `proof_07_click_forge_shortcut_opens_forge_dialog.png` | 點擊前往鍛造按鈕後成功連動關閉戰力總覽並開啟天宮鐵匠 ForgeDialog 繁中實機畫面 | `16ae93f5f0b9598d088c6b0229c0ae81b997cf097b8729c2692b2a71174fb8ae` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、簡中、英文、日文、韓文、西文及點擊跳轉天宮鐵匠實機截圖共 7 張，SHA256 皆獨立無重複，排版由 Vision 複檢確認無元素遮擋裁切。
- [x] **單元測試穩定防 flaky**：等待幀數充足（6~8 幀），時序無競爭，無頭測試 6/6 PASS。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：按鈕位於 `WeaponHeaderRow` 標題列右端，彈窗高度調整為 560px，首屏完整容納三槽卡片無遮擋。
- [x] **互動元件佈局尺寸與熱區**：`BtnGoForge` 尺寸為 96x48px，高度 >= 48px，熱區符合手遊防誤觸規範（>= 48px）。
- [x] **字級規範**：字體大小 14px（>=14px），加粗加深藍紫描邊，達成零小字。
- [x] **零系統 Emoji**：按鈕文字與介面全域無系統 Unicode Emoji。
- [x] **名稱與用詞規範**：各語系名稱嚴格對齊既有定義（繁中「前往鍛造」、英文「Go to Forge」），無任何已淘汰用詞。
- [x] **流程與交付**：使用 `project_status.py` 更新專案進度，變更完整 commit 至 `agent/20261012-power-stat-forge-shortcut-t_7716e1d4` 分支。
