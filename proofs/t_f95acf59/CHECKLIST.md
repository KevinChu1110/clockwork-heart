# 全面回歸驗收證明 · 鐵匠武器更換與木人樁調整心法雙分支合進主線 (t_f95acf59)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成審查驗收並簽核通過）之兩項重要養成與試招閉環功能分支：
1. **`forge-weapon-swap-dialog`（t_7db3e5a2）**：分支 `agent/20261012-forge-weapon-swap-dialog-t_7db3e5a2`（commit `8ac5c320d`）
   - 天宮鐵匠 `ForgeDialog` 武器鍛造區當前槽位標題列新增『更換裝備』天藍色立體果凍按鈕（`BtnSwapWeapon`，尺寸 110x48px，熱區 >= 48px，字級 16px，圓角 18px，厚底 5px，深藍紫描邊 2px，零 Emoji）
   - 點擊按鈕發射 `swap_weapon_requested` 信號，連動開啟武器庫更換裝備彈窗 `WeaponSwapDialog`
   - 換裝完成發出 `weapon_swapped` 後，`ForgeDialog` 原地接收事件並即時刷新槽位裝備、攻擊力數值與三欄槽位標籤，形成鍛造換裝閉環，且換裝後自動關閉 `WeaponSwapDialog`
   - 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換無缺漏，歐美語系零 CJK 殘留
2. **`dummy-settlement-skills`（t_f8bc43d5）**：分支 `agent/20261012-dummy-settlement-skills-t_f8bc43d5`（commit `18335bcc0`）
   - 木人樁試招結算數據卡 `DummySettlementDialog` 底部按鈕列新增『調整心法』天藍色立體果凍按鈕（`BtnGoSkills`，尺寸 170x52px，熱區 >= 48px，字級 18px，厚底 6px，深藍紫描邊 2px，圓角 20px，零 Emoji）
   - 與『再次試招』、『完成試招』形成三大操作按鈕閉環
   - 點擊按鈕發射 `skills_requested` 信號與 `on_skills` 回調，關閉結算彈窗並由大廳 `MobileLobby` 流暢開啟招式心法彈窗 `SkillDialog`，方便玩家依試招數據即時調整招式優先順序與突破升階
   - 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換，歐美語系零 CJK 殘留

由工程師阿宏（`sideworker`）在 `main` 主線執行雙分支無衝突乾淨整併（Merge commits: `fb1faf9aa`, `961663f6f`），執行全套無頭冒煙測試、專屬單元測試、forge / dummy / skill 全套回歸測試、公開官網 live 檢測與素材檢查，並透過 `/root/project_status.py` 同步將兩項目更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **鐵匠更換裝備單元測試** | `godot --path game --headless -s scripts/ui/test_forge_swap_weapon_dialog.gd` | `TEST_FORGE_SWAP_WEAPON_DIALOG_OK`，按鈕規格、信號發射、換裝閉環原地刷新、六語系即時切換全綠 | **PASS** |
| **木人樁調整心法單元測試** | `godot --path game --headless -s scripts/battle/test_dummy_settlement_skills.gd` | `TEST_DUMMY_SETTLEMENT_SKILLS_OK`，按鈕規格、信號連動、大廳開啟 SkillDialog、六語系全綠 | **PASS** |
| **天宮鐵匠系統回歸測試** | `TEST_FILTER=forge ./tools/run_tests.sh` | 12/12 PASS（全部通過） | **PASS** |
| **木人樁系統回歸測試** | `TEST_FILTER=dummy ./tools/run_tests.sh` | 9/9 PASS（全部通過） | **PASS** |
| **招式心法系統回歸測試** | `TEST_FILTER=skill ./tools/run_tests.sh` | 13/13 PASS（全部通過） | **PASS** |
| **素材與代碼關聯檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞 | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表 (proofs/t_f95acf59/)
所有截圖皆以真實 OpenGL3 渲染驅動於 1280×720 解析度下透過真實 Viewport Framebuffer 產生，零 PIL 假圖，15 張 SHA256 各自獨立：

### A. ForgeDialog 天宮鐵匠武器槽更換裝備快捷連動（8 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_forge_dialog_btn_swap_weapon_zh_TW.png` | 繁中天宮鐵匠武器鍛造區當前槽位標題列展示『更換裝備』天藍果凍按鈕 (BtnSwapWeapon, 110x48px) | 1280×720 | `c5a49958d8a326e10b561e552f874a6fce65b6e7e25eba6a1dff8373fd7243b5` |
| `proof_02_weapon_swap_dialog_opened.png` | 點擊『更換裝備』後順暢連動開啟 WeaponSwapDialog 彈窗 | 1280×720 | `b084a09abd01cc1486c2559aebe82f60b1f23929404edbf5980ddee0ef338f39` |
| `proof_03_weapon_swapped_forge_refreshed.png` | 換裝完成後 WeaponSwapDialog 自動關閉且 ForgeDialog 原地刷新武器數值與槽位標籤 | 1280×720 | `74dfbeefe804e8bdf8074ff8f81abde01bf3b7f112aadfc67b0762e508b116be` |
| `proof_04_forge_btn_swap_weapon_zh_CN.png` | 簡中語系 (zh_CN) 下 BtnSwapWeapon 顯示「更换装备」 | 1280×720 | `5d3d356ed19ef35c4c9047fab79453ee26178969ddf78acf3a7983e33731d245` |
| `proof_05_forge_btn_swap_weapon_en.png` | 英文語系 (en) 下 BtnSwapWeapon 顯示「Change Equipment」，零 CJK 殘留 | 1280×720 | `76d6048cff9d9a38f7974bc6240a26afd175904005132a22a00d62c9fc1b427f` |
| `proof_06_forge_btn_swap_weapon_ja.png` | 日文語系 (ja) 下 BtnSwapWeapon 顯示「装備変更」 | 1280×720 | `028adcb32daba4dd586b82970d385afdb60a0a19d1b9fbefa50a152f9db78fb7` |
| `proof_07_forge_btn_swap_weapon_ko.png` | 韓文語系 (ko) 下 BtnSwapWeapon 顯示「장비 교체」 | 1280×720 | `906afedca4ae2ce4ff3650f092cabbe8b3a257afa49a9a0519072b587f8c1ab4` |
| `proof_08_forge_btn_swap_weapon_es.png` | 西班牙文語系 (es) 下 BtnSwapWeapon 顯示「Cambiar equipo」，零 CJK 殘留 | 1280×720 | `da1019b95c762b05c2aeb9930afe184dfa40f25c6db3c53a942ca917dc89e4fe` |

### B. DummySettlementDialog 木人樁試招結算調整心法快捷連動（7 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_09_dummy_settlement_zh_TW.png` | 繁中 DummySettlementDialog 底部按鈕列展示『調整心法』天藍果凍按鈕 (BtnGoSkills, 170x52px) | 1280×720 | `4ff8d58fb03f14435a43e70ebe4c38e1e3fecf1cac92aa27ec5b74229915beb4` |
| `proof_10_dummy_settlement_zh_CN.png` | 簡中語系 (zh_CN) 下 BtnGoSkills 顯示「调整心法」 | 1280×720 | `38c4770e28638151d78a89010ddb1fea42f715fdc295263fb186fdc46717dd89` |
| `proof_11_dummy_settlement_en.png` | 英文語系 (en) 下 BtnGoSkills 顯示「Adjust Skills」，零 CJK 殘留 | 1280×720 | `ef889f66a8e568357aa468911a2b42f5eb4837170d444f5abb41324ae10df266` |
| `proof_12_dummy_settlement_ja.png` | 日文語系 (ja) 下 BtnGoSkills 顯示「心法調整」 | 1280×720 | `9db5edfc7d1df0171245eb2cbca067c0ac342e13807274eaaf7b46c5677b849c` |
| `proof_13_dummy_settlement_ko.png` | 韓文語系 (ko) 下 BtnGoSkills 顯示「심법 조정」 | 1280×720 | `16441ee538a649dcf127f67f66827de06cc2b09cc62774bd8b307faaf5b1e06b` |
| `proof_14_dummy_settlement_es.png` | 西班牙文語系 (es) 下 BtnGoSkills 顯示「Ajustar habilidades」，零 CJK 殘留 | 1280×720 | `197eb90a3d9cc75b1e17cca0efa0ab446ef80e281ce1fe74fa1ef207a935ee56` |
| `proof_15_skill_dialog_opened_lobby.png` | 點擊調整心法後關閉結算彈窗並由大廳流暢開啟 SkillDialog 招式心法彈窗實機全景 | 1280×720 | `4f21ff03e18fc1ae32f2f50a784e47ee361ce2f3e981bc1c0bea02957ed2991f` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證對齊驗收項目與完整互動過程**：共 15 張真實 OpenGL3 實機截圖，涵蓋天宮鐵匠武器槽更換裝備按鈕、WeaponSwapDialog 開啟與換裝原地刷新、木人樁結算調整心法按鈕與連動開啟 SkillDialog，及雙功能六語系完整切換；15 張 SHA256 各自獨立無重複。
- [x] **單元與回歸測試穩定防 flaky**：專屬測試無頭全綠，三大系統回歸測試 34/34 PASS（forge 12/12, dummy 9/9, skill 13/13），時序無競爭。
- [x] **UI 排版與邊界規範**：
  - 鐵匠『更換裝備』按鈕為 110x48px，熱區 >= 48px，字級 16px，圓角 18px，天藍果凍厚底 5px。
  - 木人樁結算『調整心法』按鈕為 170x52px，熱區 >= 48px，字級 18px，圓角 20px，天藍果凍厚底 6px。
  - 全域零系統 Emoji，全面採用粉圓體與高飽和度多巴胺配色。
- [x] **名稱與用詞規範**：各語系鍵值與名詞嚴格對齊既有規範，無舊名詞（霧隱村／今日村莊／白霧村 零殘留）。
- [x] **專案進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `forge-weapon-swap-dialog` 與 `dummy-settlement-skills` 標記為『已上線』。
