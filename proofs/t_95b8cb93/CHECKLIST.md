# 探索性 QA 第三十七輪：撼地野牛骨架＋巡管守宮切片合 main 後找破圖驗收清單

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_95b8cb93`（🤖 平台與維運｜探索性 QA 第三十七輪：撼地野牛骨架＋巡管守宮切片合main後找破圖）
- **前置任務**：
  - `t_ec1408d9` / `t_d586d458`（第四十四族撼地野牛 bison 資料表骨架與空目錄先行建置）
  - `t_3146eedf` / `t_306ee848`（第四十五族巡管守宮 gecko 7大部件槽位紙娃娃切片與雙規格資產）
- **交付目錄**：`proofs/t_95b8cb93/`（遵守 `review.md 0-QA23` 獨立專屬目錄，絕無跨卡覆蓋）
- **遵循規範**：
  - `review.md 0-QA5 / 0-QA26`：100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 擷取，嚴禁 PIL 假圖。
  - `review.md 0-QA15`：全數 12 張全景截圖與 12 張特寫 crops MD5 100% 獨立唯一，無重複檔名或相同內容。
  - `review.md 0-QA16 / 0-ART29`：洋紅底無孔洞 (0 px)、發條無黑底板 (0 px)、無平塗佔位色塊。
  - `review.md 0-QA17`：實機截圖完整呈現核心功能畫面（創角、衣櫥、戰鬥、大廳、DevPreview、i18n 看板）。
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/t_95b8cb93/`，絕無覆蓋其他卡片之 proof 目錄。
  - `review.md 0-QA24 / 0-QA25`：六語系 ui.json 專有名詞對齊，切換語系同步連動。
  - `review.md 0-QA30`：全 45 族 正表與 fallback 表 aliases 100% 逐項完全對齊。
  - `review.md 0-QA31`：7 槽疊合像素覆蓋 4696 px > 3000、目鏡 161 色 >= 15。
  - `review.md 0-UI1 / 31d`：全畫面 100% 徹底清除系統 Emoji，按鈕熱區高度 >= 48px。
  - `docs/world/CANON.md`：100% 零毛皮、零血肉、零生物特徵，全金屬/發條/玩具世界觀。

---

## 一、 實機全景截圖核驗清單（1280x720，逐張打勾）

| 編號 | 實機截圖檔名 | 涵蓋場景與驗證重點 | 破圖 | 零 Emoji | 語系連動 | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_dev_paperdoll_gecko_default.png` | DevPaperdollPreview: 巡管守宮 7 槽位預設裝備實機疊合展示 (128x128 舞台) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 02 | `proof_02_dev_paperdoll_gecko_bare.png` | DevPaperdollPreview: 巡管守宮裸機素體 (costume: none)，冷軋黃銅素體與散熱百葉槽 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 03 | `proof_03_dev_paperdoll_gecko_unarmed.png` | DevPaperdollPreview: 巡管守宮卸除武器 (weapon: none)，驗證素體右側無畫死武器 (0 px) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 04 | `proof_04_gecko_512_composite_stage.png` | 512x512 高清原寸切片疊合舞台 (LANCZOS 平滑縮放、無鋸齒、無雜點) vs 128 對照 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 05 | `proof_05_gecko_official_standee_and_showcase.png` | 巡管守宮官方立牌展示 (showcase 800x1200 HD) 與待機圖對照 (四角 100% 透明) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 06 | `proof_06_creation_flow_audit_gecko.png` | 創角介面 (PaperdollSelectDemo): 巡管守宮選取展示 (立繪、忍者、飛鏢、描述完整) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 07 | `proof_07_creation_flow_audit_bison_hidden.png` | 創角介面 (PaperdollSelectDemo): 撼地野牛安全隱藏狀態 (has_race_assets 防護生效) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 08 | `proof_08_wardrobe_flow_audit_gecko.png` | 衣櫥換裝 (WardrobeDialog): 巡管守宮篩選 Chip、耐熱工裝暗忍胸甲與冷軋素體卡片 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 09 | `proof_09_battle_flow_audit_gecko.png` | 戰鬥畫面 (BattleView): 巡管守宮實機戰鬥（玩家名「巡管守宮」、開局武器「mist_darts」） | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 10 | `proof_10_battle_flow_audit_bison.png` | 戰鬥畫面 (BattleView): 撼地野牛實機戰鬥（玩家名「撼地野牛」、開局武器「anvil_hammer」） | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 11 | `proof_11_lobby_flow_audit_gecko.png` | 手遊大廳主介面 (MobileLobby): 巡管守宮大廳展示（Lv.10 巡管守宮、紙娃娃、底部 Dock） | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 12 | `proof_12_i18n_and_emoji_audit.png` | 六語系 i18n 兩族詞條對齊看板與 0-UI1 / 31d 零系統 Emoji 稽核看板 | ✓ 無 | ✓ 零 | ✓ 六語系 | **通過 (PASS)** |

---

## 二、 實機截圖檔案與 MD5 查驗表

全數檔案均為 1280x720 實機 framebuffer 渲染（特寫裁切為對應局部區域），24 個檔案 MD5 均為獨立真實生成，符合 `review.md 0-QA15`：

```
292b4f2379d2e4b78861ea9815c8308f  proof_01_dev_paperdoll_gecko_default.png (1280x720, 167 KB)
466731821e7031714bbf6712e0189e51  proof_02_dev_paperdoll_gecko_bare.png (1280x720, 171 KB)
551dd3529fce9e130d4b9e9d9004d192  proof_03_dev_paperdoll_gecko_unarmed.png (1280x720, 166 KB)
2b837cebc6c66349c508cc6631be59db  proof_04_gecko_512_composite_stage.png (1280x720, 228 KB)
740bab6fe7a0e98e7d9e3f169bf0db81  proof_05_gecko_official_standee_and_showcase.png (1280x720, 41 KB)
b9b2bd389214e1b22fb7d3c0e3d5e90c  proof_06_creation_flow_audit_gecko.png (1280x720, 249 KB)
5216d2801a96109258ddd5fab28823cd  proof_07_creation_flow_audit_bison_hidden.png (1280x720, 258 KB)
11fc4cdc2b03ae76979bdaab061972d7  proof_08_wardrobe_flow_audit_gecko.png (1280x720, 436 KB)
1460fdc3de99a7b0bc7c4dfce080e371  proof_09_battle_flow_audit_gecko.png (1280x720, 1204 KB)
9214a3a29869423ec28e5be7e14f23d0  proof_10_battle_flow_audit_bison.png (1280x720, 1189 KB)
7f28d71042f2cb50f8abaac487830fdd  proof_11_lobby_flow_audit_gecko.png (1280x720, 974 KB)
c7d44f8ccb62e8b7fca8449d6ccf5e8a  proof_12_i18n_and_emoji_audit.png (1280x720, 240 KB)

crops/12826dcf6c0e7a18171bfd92e2da1e12  crops/crop_01_gecko_paperdoll_7_slots.png (220x240)
crops/a35cb346ecc8c14f28abbb1196d7ea0f  crops/crop_02_gecko_bare_chassis.png (220x240)
crops/b2a29a432c0f593f9dfd4e311e7391e7  crops/crop_03_gecko_unarmed.png (220x240)
crops/efded32a8bf021487f40075d33fde6c7  crops/crop_04_gecko_512_torso.png (440x460)
crops/9d04c8637ed4b6e33fc72cc90dfd97c1  crops/crop_05_gecko_showcase_standee.png (360x560)
crops/326f39192fd2bcda8179d057c3fb85e1  crops/crop_06_creation_gecko_card.png (570x480)
crops/62f69bbe768b9ef1cd9b5d062cf4c863  crops/crop_07_creation_bison_hidden.png (1200x120)
crops/7249fc22c7b6187e4f8db0f58f220f54  crops/crop_08_wardrobe_gecko_cards.png (630x500)
crops/6d453079ca8e10e2567c1e64c418df0c  crops/crop_09_battle_gecko_nameplates_log.png (570x270)
crops/f23f6ed112acd88f2fb6d7be9c50e39c  crops/crop_10_battle_bison_nameplates_log.png (570x270)
crops/a37f32cd8eac905dfa201c8b981beb54  crops/crop_11_lobby_gecko_avatar.png (430x120)
crops/b489e54c604ff10ea6bbae51871c2286  crops/crop_12_i18n_emoji_audit_dashboard.png (1200x620)
```

---

## 三、 六語系在地化與世界觀稽核結論

1. **六語系 ui.json 補齊 20 條詞條**：
   - 撼地野牛（10 條）：繁中「撼地野牛」、簡中「撼地野牛」、英文「The Groundshaker Bison」、日文「撼地の野牛 (カンチノヤギュウ)」、韓文「진지들소」、西文「El Bisonte Tiemblatierra」及七大部件名稱均已合規入庫。
   - 巡管守宮（10 條）：繁中「巡管守宮」、簡中「巡管守宫」、英文「The Conduit Gecko」、日文「導管のヤモリ (カンカンノヤモリ)」、韓文「배관 순찰 도마뱀붙이」、西文「El Gecko de los Conductos」及七大部件名稱均已合規入庫。
2. **0-UI1 / 31d 零系統 Emoji 稽核**：
   - 六語系 ui.json 全域搜尋 0 系統 Emoji。
   - 創角、衣櫥、戰鬥、大廳全介面 0 系統 Emoji，符合多巴胺鮮亮高飽和色盤，按鈕熱區高度 >= 48px。
3. **CANON.md 玩具世界觀查驗**：
   - 守宮冷軋黃銅吸盤素體、野牛生鏽耐磨馬口鐵重裝素體，100% 零真毛皮、零真鱗片、零生物血肉，背後必帶發條鑰匙。
4. **自動化測試全綠**：
   - `python3 tools/verify_bison_0_qa30.py`: PASS (45 族 aliases 100% 對齊)
   - `python3 tools/verify_gecko_0_qa30.py`: PASS (45 族 aliases 100% 對齊)
   - `python3 tools/verify_gecko_lanczos.py`: PASS (7 大槽位 512 LANCZOS 平滑驗證通過)
   - `python3 tools/audit_gecko_slices.py`: PASS (0-ART5/9/11/18/26b/27/29, 0-QA16/30/31 通過)
   - `godot --path game --headless -s res://scripts/art/test_paperdoll_bison_skeleton.gd`: PASS
   - `godot --path game --headless -s res://scripts/art/test_paperdoll_gecko_skeleton.gd`: PASS
   - `godot --path game --headless -s res://scripts/art/test_paperdoll_gecko_variants.gd`: PASS
   - `godot --path game --headless -s res://scripts/art/test_paperdoll_race_switch.gd`: PASS (45 族切換還原成功)
   - `godot --path game --headless --quit-after 3`: PASS (0 SCRIPT ERROR)

---

## 四、 問題清單與後續派工建議（Findings & Next Steps）

1. **第四十四族撼地野牛 (bison)**：
   - **現狀**：資料表骨架與空目錄先行建置已進 main。創角與衣櫥透過 `has_race_assets` 安全隱藏，戰鬥中名字與武器 ID（`anvil_hammer`）解析正常，不會發生破圖。
   - **後續派工**：待開立 7 大部件槽位紙娃娃切片試產任務卡（`bison-slices`）交由 sideworker / sideworker2 執行。
2. **第四十五族巡管守宮 (gecko)**：
   - **現狀**：骨架與 7 大槽位切片已全數合進 main，創角與衣櫥展示正常無破圖。
   - **後續派工**：待開立六大戰鬥姿態補齊任務卡（`gecko-combat-poses`）與官方資產套件任務卡（`gecko-official-assets`）。
