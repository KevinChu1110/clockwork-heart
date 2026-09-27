# 驗收證明 · 探索性 QA：抗性場上提示＋戰鬥日誌＋結算六語系合主線後找破圖 (t_42696b4f)

## 依據規範
- `review.md 0-QA5 / 0-QA26`：Godot ViewportTexture framebuffer 直接擷取（`xvfb-run -a godot --rendering-driver opengl3`），嚴禁 PIL／手繪假圖。
- `review.md 0-QA23`：OUT_DIR 獨立目錄，存證至 `proofs/t_42696b4f/`，不覆蓋其他任務目錄。
- `review.md 0-QA25`：全畫面多語系動態即時切換連動刷新，繁中與英文各一輪查截字與中英混雜。
- `review.md 0-QA27 / 0-QA28`：玩家可見字 100% 走翻譯層，零系統彩色 Emoji，多巴胺鮮亮色盤。
- 舊功能未損壞（大廳主城、四區出征與停擺巨偶、角色換裝衣櫥）。
- 依任務指示：只審不改，鐵匠英文校準日誌若出現中文色階名「藍」，記帳不修（非本單範圍，另開六語系單）。

---

## 實機截圖存證清單 (1280x720)

| 編號 | 實機截圖檔名 | 涵蓋驗證內容 | 破圖 | 零 Emoji | 截字溢出 | 驗證結論 |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_zh_resist_strained_combat.png` | 繁中戰鬥場上抗性吃力提示（`吃力 · 受傷 ×1.2`）、金黃底深藍紫描邊果凍徽章、不擋血條與攻擊鈕 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 02 | `proof_02_zh_resist_overload_combat.png` | 繁中戰鬥場上抗性過載提示（`過載 · 受傷 ×1.5`）、珊瑚粉紅底白字、位置與間距工整 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 03 | `proof_03_en_resist_strained_combat.png` | 英文戰鬥場上抗性吃力提示（`Strained · Dmg ×1.2`）、多巴胺金黃果凍徽章、排版清晰 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 04 | `proof_04_en_resist_overload_combat.png` | 英文戰鬥場上抗性過載提示（`Overload · Dmg ×1.5`）、粉紅底白字、右下角 Attack 單行未折字 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 05 | `proof_05_zh_battle_log_canon.png` | 繁中戰鬥日誌世界觀用詞：相剋提示「金屬板件厚實（防爆高）……發條重擊最實在」，100% 零筋骨／零斧鎚舊武俠肉身詞 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 06 | `proof_06_en_battle_log_attack_btn.png` | 英文戰鬥日誌王者斬結算（`[The King's Cut] Rampant Clockwork Lion deals 65 damage`），零 `[/b]` 標籤露出，技能與敵名有空格分隔；攻擊鈕 `Attack` 寬度 108px 高度 72px 單行不折字 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 07 | `proof_07_zh_victory_core_drop.png` | 繁中勝利結算機芯掉落卡片：「發條發電機 【金階】」、「部位破壞 鐵屑 +2」、「立即裝備」與「收下完成」按鈕 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 08 | `proof_08_en_victory_core_drop.png` | 英文勝利結算機芯掉落卡片：`Mainspring Dynamo [Gold Tier]`、`Part Break Scrap Iron +2`、`EXP +450`、`Equip Now`、`Collect`，100% 零 CJK 中文字元殘留 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 09 | `proof_09_zh_lobby_regression.png` | 舊功能回歸：大廳主城神殿與齒輪背景、主角小白全身立繪動態齒輪光輪、頂部 HUD（能量 15/15、金幣 12,500）、底部 Dock 5 個一級導航入口 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 10 | `proof_10_zh_sortie_regression.png` | 舊功能回歸：出征分頁停擺巨偶模式「今日剩餘: 3/3 次」、三張巨偶挑戰卡片（失控發條獅 Lv12、霧鐘提線人偶 Lv20、黑鏽蒸氣巨象 Lv28）完整展示 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 11 | `proof_11_zh_wardrobe_regression.png` | 舊功能回歸：發條衣櫥紙娃娃全身預覽、外裝服飾與機體塗裝卡片、保存與關閉按鈕，零截字零破圖 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 12 | `proof_12_en_forge_calibration_log.png` | 巡檢存證（記帳不修）：天宮鐵匠英文校準日誌巡檢，綠色訊息文字出現色階名中文「藍」字樣（`Current Tier: 藍 (4 Left)`），記帳留存 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **記帳留存 (LOGGED)** |

---

## 關鍵檢核點落實詳情

### 1. 0-QA5 / 0-QA26（真遊戲畫面 Framebuffer 截圖）
- 截圖全數由 Godot 4.7 引擎透過 `xvfb-run -a godot --rendering-driver opengl3` 於虛擬 X Framebuffer 執行，以 `Viewport.get_texture().get_image()` 儲存，絕無使用 PIL 繪製或手繪假圖。
- 12 張截圖解析度嚴格對齊專案橫屏 1280x720，每張檔案大小介於 150KB 至 1.36MB，畫質清晰完整。

### 2. 抗性場上受傷加深提示（繁中與英文）
- **吃力檔位（差 2 級，×1.2）**：
  - 繁中顯示：`吃力 · 受傷 ×1.2`（金黃底 `#FFD028`、深藍紫描邊 `#1F1A3A`、字級 13px）。
  - 英文顯示：`Strained · Dmg ×1.2`。
- **過載檔位（差 6 級，×1.5）**：
  - 繁中顯示：`過載 · 受傷 ×1.5`（珊瑚粉紅底 `#FF5E8A`、白字、深藍紫描邊）。
  - 英文顯示：`Overload · Dmg ×1.5`。
- **位置與防遮擋檢核**：
  - 提示膠囊徽章掛於左上角 `SideBars/PlayerSide` 最下方（怒氣條正下方），與上方 HP 血條垂直留有足夠安全距離，不擋血條；離右下角攻擊操作按鈕相隔全螢幕寬度，完全不遮擋攻擊與操作按鈕。
  - 純粉圓體文字搭配果凍底板，全域零彩色系統 Emoji。

### 3. 戰鬥日誌世界觀與按鈕折字檢核
- **世界觀修復**：
  - 繁中日誌相剋提示：「敵手金屬板件厚實（防爆高）——爆擊難進，發條重擊最實在。」
  - 100% 徹底清除舊武俠「筋骨」、「斧鎚」等肉身兵器詞彙，全面符合發條玩具與金屬板件之覺醒世界觀設定。
- **英文日誌 BBCode 跳脫**：
  - 巨偶王者斬命中日誌成功跳脫方括號，日誌呈現 `[The King's Cut] Rampant Clockwork Lion deals 65 damage`，100% 零 `[/b]` 標籤洩漏，且技能名稱與敵名中間保留標準空格分隔。
- **英文攻擊鈕不折字**：
  - 常態攻擊按鈕於英文語系下寬度為 108px、高度為 72px（熱區高度遠大於手遊防誤觸標準 48px），設置 `AUTOWRAP_OFF`，文字「Attack」水平置中且維持於單行，無被截字折行成 `Attac` / `k` 的缺陷。

### 4. 勝利結算機芯掉落卡六語系在地化
- **繁中結算卡片**：
  - 標題與副標題：`戰鬥勝利`、`關卡突破！獲得機芯部件`。
  - 機芯卡片：展示金色發條齒輪圖示、名稱「發條發電機 【金階】」、數值「Atk+69 · HP+340」、詞條「可校準 7 次 · 安全彈簧保護不碎裝」。
  - 獎勵清單：戰鬥經驗「EXP +450」、部位破壞「鐵屑 +2」。
  - 操作按鈕：深藍「立即裝備」、金黃「收下完成」。
- **英文結算卡片**：
  - 經由 `vision_analyze` 逐字嚴格稽核，標題 `Victory`、`Stage cleared! Core part looted.`、機芯名稱 `Mainspring Dynamo [Gold Tier]`、屬性 `Atk+69 · HP+340`、機制說明 `Can calibrate 7 times · Safety spring protected`、經驗 `Combat EXP EXP +450`、部位破壞 `Part Break Scrap Iron +2`、按鈕 `Equip Now`、`Collect`。
  - **100% 零 CJK 中文字元殘留**，括號亦已標準西文半形化 `[Gold Tier]`。

### 5. 舊功能回歸檢核
- **大廳主城**：神殿齒輪背景通透手繪感、主角小白動態待機與同心齒輪光輪運轉正常、頂部 HUD 數值（能量 15/15、金幣 12,500）齊全、底部 Dock 五大入口無重複、零 Emoji。
- **四區出征**：四區主線與停擺巨偶子模式切換流暢、停擺巨偶每日 3/3 次數正常遞減、三張巨偶卡片（失控發條獅、霧鐘提線人偶、黑鏽蒸氣巨象）文字與屬性標記無誤。
- **發條衣櫥**：紙娃娃全身即時預覽正常、外裝服飾與機體塗裝多套卡片滑動流暢、還原/隨機/確認換裝按鈕功能無損。

---

## 記帳缺陷存證（已記錄，依指示不於本單修改）

- **發現缺陷**：天宮鐵匠英文介面（`en`）進行機芯校準時，底部日誌訊息中的色階名稱出現中文「藍」字（如截圖 `proof_12_en_forge_calibration_log.png` 所示）：
  `[Mainspring Dynamo] Success +1 tier! Clockwork breakthrough • Current Tier: 藍 (4 Left)`
- **根本原因**：`game/data/i18n/content/en/ui.json` 中僅定義了帶階字之詞條（如 `"藍階": "Blue Tier"`），但缺乏單字色階 key `"藍": "Blue"`；而 `forge_dialog.gd` 在 `_update_calibrate_message` 中直接呼叫 `_t(raw_tnm)`，當 `raw_tnm == "藍"` 時找不到翻譯因此回傳原中文字。
- **處理結論**：依據製作人指示與本卡規範（「鐵匠英文校準日誌若仍出現中文色階名『藍』，記帳不修，另開六語系單；本單只審不改」），此缺陷已於本 CHECKLIST 明確記錄並附實機截圖存證，不整單打回，留待後續六語系專用單修復。
