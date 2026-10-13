# 發條之心｜SkillDialog 招式卡片支援熟練度進度條、一鍵突破升階與體悟習得 驗收清單 (t_98ea7703)

## 驗收標準對照

1. **熟練度進度條 (ProgressBar)**
   - [x] 為已習得招式 (is_learned) 增加視覺化薄荷綠多巴胺熟練度進度條 (ProgressBar)。
   - [x] 高度符合規範 (8px高、圓角4px)。
   - [x] 中段展示數值 (如 15/30、30/30) 與當前比例。
   - [x] 單元測試 `test_skill_dialog_upgrade.gd` 驗證進度條百分比計算 100% 精確。

2. **暖橘立體果凍『突破升階』按鈕**
   - [x] 當熟練度滿且 `can_level_up(sid)` 為真時（未達 MAX_LV），於卡片右側展示暖橘立體果凍按鈕。
   - [x] 按鈕尺寸合規 (高48px、底邊厚度4px、熱區>=48px)。
   - [x] 點擊調用 `SkillSystem.try_level_up(sid)` 成功提升技能等級，即時扣除熟練度並刷新卡片與優先出招標籤。
   - [x] 單元測試驗證升階後等級提升、熟練度扣除、按鈕自動隱藏。

3. **薄荷綠立體果凍『體悟習得』按鈕**
   - [x] 當招式未習得但已達解鎖條件 (`is_unlocked(sid) and not is_learned(sid)`) 時，提供薄荷綠果凍按鈕。
   - [x] 按鈕尺寸合規 (高48px、底邊厚度4px、熱區>=48px)。
   - [x] 點擊調用 `SkillSystem.try_unlock(sid)` 習得招式並即時刷新為已習得狀態，生成熟練度進度條。
   - [x] 單元測試驗證點擊後招式即時轉為已習得。

4. **『Lv.MAX · 極階』金色標籤**
   - [x] 當招式達到滿級 (`slv >= MAX_LV`) 時，展示金色膠囊標籤『Lv.MAX · 極階』。
   - [x] 右側不出現多餘突破按鈕。

5. **六語系即時切換**
   - [x] 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換，走 ContentLoc / `_t()`。
   - [x] 語系詞條完整對齊，切換語系時按鈕與標籤無穿框、無重疊。

6. **驗收測試與代碼品質**
   - [x] 單元測試 `test_skill_dialog_upgrade.gd` 全數通過 (`SKILL_DIALOG_UPGRADE_TEST_OK`)。
   - [x] 迴歸測試 `test_skill_priority_badge`, `test_lobby_skill_dialog_btn`, `test_skill_i18n` 全數綠燈 (10/10 PASS)。
   - [x] 全介面 0 系統 Emoji、字級 >= 14px、0 SCRIPT ERROR。
   - [x] `clock-check` 自動檢查全過（✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞）。

## 實機存證截圖清單 (SHA256 驗證全數獨立不重複)

- `proof_01_skill_progress_half.png`: 熟練度進度條半滿 (15/30, 8px 薄荷綠條)
  - SHA256: `32b5e224a619477f905061a339736d241257c5902b161f7d0eddf8db13941f18`
- `proof_02_skill_upgrade_button.png`: 滿熟練度 (30/30) 觸發暖橘立體果凍『突破升階』按鈕 (高48px、底邊厚度4px)
  - SHA256: `c323e50f768bdae86c2b45df02c80be01146748aaf0476c20a2e7a8f1a32391b`
- `proof_03_skill_max_tier_badge.png`: 滿級招式展示『Lv.MAX · 極階』金色標籤 (無突破按鈕)
  - SHA256: `2fbd71ef1cf94574a97dc33c1642e729e28ac8e992faaaf73fcbc74bca7ba1b4`
- `proof_04_skill_upgrade_en.png`: 英文語系 (Breakthrough / Comprehend / Lv.MAX · Mastered) 即時對齊截圖
  - SHA256: `f4583aae18a2934111fb46ffc12023292c0a90edbf3ec5edbd5e567233267482`
- `proof_05_skill_unlock_button.png`: 滾動至槍系起手技 (一線突刺)，完整展示薄荷綠立體果凍『體悟習得』按鈕
  - SHA256: `66e9af743c58f1f7f75844ada056711fb10e21661f6376c980232669966c891b`
