# 《發條之心》三大戰鬥結算與鍛造快捷聯動合併後全站回歸驗收報告 (t_f8f33c24)

- **驗收審查員**：小婷（發條之心·測試 sideqa）
- **關聯任務**：`t_f8f33c24`（🤖 平台與維運｜三大戰鬥結算與鍛造快捷聯動合併後的全站回歸驗收）
- **前置任務**：`t_b50e7e0a`（三大分支乾淨合併至 main：`agent/20261009-defeat-diagnostic-t_39d5fc6c`、`agent/20261009-victory-next-stage-t_a1446e8f`、`agent/20261009-weapon-swap-forge-t_1df92466`）
- **交付存證目錄**：`proofs/t_f8f33c24/`
- **遵循規範**：
  - `review.md` 人因人機工程與多巴胺配色規範：按鈕熱區 >= 48px、立體果凍厚底 >= 5px、圓角 16~24px、零 Emoji、多巴胺鮮亮色盤（金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A、深藍紫描邊 #1F1A3A）。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 連續截圖 SHA256 完全獨立互異，存證對齊驗收項目與完整互動過程。
    - 彈窗與卡片正確佈局尺寸（custom_minimum_size / min_size），避免坍塌或溢出。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_battle_defeat_diagnostic_zh_TW.png` | `BattleDefeatDialog` 戰敗結算彈窗：展示「戰力診斷」卡、三大建議膠囊（武器階數、裝備副詞條、招式調整）及橘黃「前往整頓」立體果凍按鈕（高 52px >= 50px，底邊 5px） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `263970a77d97` | 合格 (PASS) |
| 02 | `proof_02_defeat_to_character_tab_navigated.png` | 點擊「前往整頓」後發射 `gear_up_requested` 信號，正確經由 `main.gd` 導向大廳角色頁（`MobileLobby.Tab.CHARACTER`），三欄武器輪替配置與紙娃娃完整渲染 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `c0e3d8719c0d` | 合格 (PASS) |
| 03 | `proof_03_battle_victory_next_stage_button.png` | `BattleVictoryDialog` 1-1 出征勝利結算彈窗：展示薄荷綠「挑戰下一關」按鈕（`BtnNextStage`，尺寸 200x52px，果凍厚底 5px，與「收下完成」並列） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `e3c554a8d97d` | 合格 (PASS) |
| 04 | `proof_04_battle_victory_final_stage_hidden.png` | `BattleVictoryDialog` 切換至 4-4 末關：自動判斷無後續關卡，`BtnNextStage` 自動平滑隱藏，避免玩家點擊越界 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `713a3a988ee5` | 合格 (PASS) |
| 05 | `proof_05_weapon_swap_dialog_btn_go_forge.png` | `WeaponSwapDialog` 武器更換彈窗底部操作列：天藍色「前往鍛造」立體果凍按鈕（`BtnGoForge`，尺寸 130x48px，厚底 5px，與「關閉」並列） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `c1b058c6d94c` | 合格 (PASS) |
| 06 | `proof_06_weapon_swap_forge_dialog_opened.png` | 點擊「前往鍛造」後發射 `forge_requested` 信號，平滑關閉更換彈窗並連動大廳 `MobileLobby.open_forge()` 開啟天宮鐵匠鍛造彈窗（`ForgeDialog`） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `44b9b9d688ca` | 合格 (PASS) |
| 07 | `proof_07_battle_defeat_diagnostic_en_no_cjk.png` | 英文語系 (en) `BattleDefeatDialog`：標題顯示「Battle Defeat」、診斷卡顯示「Combat Power Diagnostic」、按鈕顯示「Go to Gear Up」，零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `164a60bcd43e` | 合格 (PASS) |
| 08 | `proof_08_battle_victory_next_stage_en_no_cjk.png` | 英文語系 (en) `BattleVictoryDialog`：標題顯示「Battle Victory」、按鈕顯示「Next Stage」，零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `0a3c1067e4cf` | 合格 (PASS) |
| 09 | `proof_09_weapon_swap_forge_ja.png` | 日文語系 (ja) `WeaponSwapDialog`：快捷按鈕顯示「鍛造へ進む」，語義自然且無溢出破版 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `1e589febf850` | 合格 (PASS) |

- **防作弊與真實性校驗**：9 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），對應 9 張特寫裁切圖於 `crops/` 目錄。
- **Vision 視覺複檢**：經 Vision 驗證，所有元素比例正確、無黑屏、無穿模、無截字、無任何違規 Emoji。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **戰力診斷** | 战力诊断 | Combat Power Diagnostic | 戦力診断 | 전투력 진단 | Diagnóstico de Poder |
| **武器階數** | 武器阶数 | Weapon Tier | 武器ランク | 무기 등급 | Rango de Arma |
| **天宮鐵匠鍛造強化** | 天宫铁匠锻造强化 | Forge at Sky Blacksmith | 天宮の鍛冶屋で強化 | 천궁 대장간 단조 강화 | Forjar en Herrería Celestial |
| **裝備副詞條** | 装备副词条 | Equipment Affixes | 装備サブステータス | 장비 보조 옵션 | Afijos de Equipo |
| **調整機芯優化屬性** | 调整机芯优化属性 | Tune Core Stats | コア調整でステータス最適化 | 코어 조정 속성 최적화 | Ajustar Núcleo para Atributos |
| **招式調整** | 招式调整 | Skill Setup | 技の調整 | 기술 조정 | Ajuste de Habilidades |
| **武術館自訂招式順序** | 武术馆自订招式顺序 | Customize Order at Dojo | 武術館で技順をカスタマイズ | 무술관에서 기술 순서 설정 | Personalizar Orden en Dojo |
| **前往整頓** | 前往整顿 | Go to Gear Up | 整備へ進む | 정비하러 가기 | Ir a Prepararse |
| **挑戰下一關** | 挑战下一关 | Next Stage | 次のステージへ | 다음 스테이지 도전 | Siguiente Nivel |
| **前往鍛造** | 前往锻造 | Go to Forge | 鍛造へ進む | 단조로 이동 | Ir a Forja |

---

## 三、 測試套件與審查指令驗證結果

1. **無頭冒煙測試**：
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR，編譯與加載完全正常。
2. **單元與驗收測試套件**：
   - `test_battle_defeat_diagnostic.gd`：`TEST_BATTLE_DEFEAT_DIAGNOSTIC_OK`（通過）
   - `test_battle_defeat_i18n.gd`：`TEST_BATTLE_DEFEAT_I18N_OK`（通過）
   - `test_battle_victory_next_stage.gd`：`TEST_BATTLE_VICTORY_NEXT_STAGE_OK`（通過）
   - `test_weapon_swap_forge_shortcut.gd`：`TEST_WEAPON_SWAP_FORGE_SHORTCUT_OK`（通過）
   - `test_lobby_weapon_swap_dialog.gd`：`TEST_LOBBY_WEAPON_SWAP_DIALOG_OK`（通過）
   - `test_i18n.gd`：`I18N_OK`（1034 keys 全部對齊通過）
3. **全站回歸驗證腳本**：
   - `res://../tools/capture_regression_t_f8f33c24.gd`：`TEST_REGRESSION_T_F8F33C24_OK`（9 張實機截圖存證與 SHA256 檢核全數通過）。
4. **自動化審查檢查器**：
   - `clock-check --live`：`✅ 官網 14 頁都打得開，沒有舊名詞`。
