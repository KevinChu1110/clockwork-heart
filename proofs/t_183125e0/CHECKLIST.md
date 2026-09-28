# 探索性 QA 第五十輪：撼野牛/破星蜜獾切片/熔鎧犰狳骨架合 main 後找破圖驗收清單

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_183125e0`（🤖 平台與維運｜探索性 QA 第五十輪：撼野牛/破星蜜獾切片/熔鎧犰狳骨架合main後找破圖）
- **前置任務**：
  - `t_27106713` / `t_80f63a7e`（第四十六族破星蜜獾 badger 六大戰鬥姿態補齊）
  - `t_d448e3ab`（第四十九族熔鎧犰狳 armadillo 資料表骨架與空目錄先行建置）
  - `t_1c9ac092` / `t_fc2149af`（第四十四族撼地野牛 bison 切片與六大戰鬥姿態）
- **交付目錄**：`proofs/t_183125e0/`（遵循 `review.md 0-QA23` 獨立專屬目錄，絕無跨卡覆蓋）
- **遵循規範**：
  - `review.md 0-QA5 / 0-QA26`：100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 擷取，嚴禁假圖。
  - `review.md 0-QA15`：全數 12 張全景截圖與 12 張特寫 crops MD5 100% 獨立唯一，無重複檔名或相同內容。
  - `review.md 0-QA16 / 0-ART29`：洋紅底無孔洞 (0 px)、發條鑰匙無黑底板 (0 px)、無平塗佔位色塊。
  - `review.md 0-QA17`：實機截圖完整呈現核心功能畫面（Dev預覽、512原寸、姿態舞台、創角、衣櫥、戰鬥、i18n看板）。
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/t_183125e0/`，絕無覆蓋其他卡片之 proof 目錄。
  - `review.md 0-QA24 / 0-QA25`：六語系 ui.json 專有名詞對齊，切換語系同步連動。
  - `review.md 0-QA30`：全 49 族 正表與 fallback 表 aliases 100% 逐項完全對齊。
  - `review.md 0-QA31`：目鏡與組件色彩豐富度 >= 15 色。
  - `review.md 0-UI1 / 31d`：全畫面 100% 徹底清除系統 Emoji，按鈕熱區高度 >= 48px。
  - `docs/world/CANON.md`：100% 零毛皮、零血肉、零生物特徵，覺醒發條玩具世界觀。

---

## 一、 實機全景截圖核驗清單（1280x720，逐張打勾）

| 編號 | 實機截圖檔名 | 涵蓋場景與驗證重點 | 破圖 | 零 Emoji | 語系連動 | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_dev_paperdoll_badger_default.png` | DevPaperdollPreview: 破星蜜獾 7 槽位預設切片實機疊合展示 (128x128 舞台) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 02 | `proof_02_dev_paperdoll_badger_bare.png` | DevPaperdollPreview: 破星蜜獾裸機素體 (costume: none)，航天高分子太空素體 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 03 | `proof_03_dev_paperdoll_badger_unarmed.png` | DevPaperdollPreview: 破星蜜獾卸除武器 (weapon: none)，驗證右側素體無內嵌畫死爪刀 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 04 | `proof_04_badger_512_composite_stage.png` | 512x512 高清原寸切片疊合舞台 (LANCZOS 平滑縮放、無鋸齒、無雜點) vs 128 對照 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 05 | `proof_05_dev_paperdoll_bison_default.png` | DevPaperdollPreview: 撼地野牛 7 槽位預設切片實機疊合展示 (128x128 舞台) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 06 | `proof_06_bison_512_composite_stage.png` | 512x512 高清原寸切片疊合舞台 (LANCZOS 平滑縮放、無鋸齒、無雜點) vs 128 對照 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 07 | `proof_07_badger_combat_poses_stage.png` | 破星蜜獾六大戰鬥姿態實機動態對照 (idle/telegraph/attack/recover/skill/hit) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 08 | `proof_08_bison_combat_poses_stage.png` | 撼地野牛六大戰鬥姿態實機動態對照 (idle/telegraph/attack/recover/skill/hit) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 09 | `proof_09_creation_flow_audit_badger_armadillo.png` | 創角介面 (PaperdollSelectDemo): 破星蜜獾解鎖展示與熔鎧犰狳安全隱藏 (has_race_assets 防護) | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 10 | `proof_10_wardrobe_flow_audit_badger.png` | 衣櫥換裝 (WardrobeDialog): 破星蜜獾篩選晶片、EVA 重裝線束胸甲與素體切換展示 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 11 | `proof_11_battle_flow_audit_badger_and_bison.png` | 戰鬥畫面 (BattleView): 破星蜜獾實機戰鬥（玩家名「破星蜜獾」、開局撕裂爪刀）與野牛日誌 | ✓ 無 | ✓ 零 | ✓ 繁中 | **通過 (PASS)** |
| 12 | `proof_12_i18n_and_emoji_audit.png` | 六語系 i18n 49 族詞條對齊看板與 0-UI1 / 31d 零系統 Emoji 稽核看板 | ✓ 無 | ✓ 零 | ✓ 六語系 | **通過 (PASS)** |

---

## 二、 實機截圖檔案與 MD5 查驗表

全數檔案均為 1280x720 實機 framebuffer 渲染（特寫裁切為對應局部區域），24 個檔案 MD5 均為獨立真實生成，符合 `review.md 0-QA15`：

```
cd9038ec5d652c2f40d80706f825062b  proof_01_dev_paperdoll_badger_default.png (1280x720, 164 KB)
1f504d0cdb6b9d5dcd5a39632473c9db  proof_02_dev_paperdoll_badger_bare.png (1280x720, 164 KB)
2fd6604171fbe9d6b65d7e764fe1d907  proof_03_dev_paperdoll_badger_unarmed.png (1280x720, 156 KB)
901421cdfdaf812e8b5008ab411bc2f6  proof_04_badger_512_composite_stage.png (1280x720, 251 KB)
70c25a71be6fbec5d3ec8053cdc7467c  proof_05_dev_paperdoll_bison_default.png (1280x720, 163 KB)
6d5c014ac0e42a58675329aadf4e5621  proof_06_bison_512_composite_stage.png (1280x720, 249 KB)
5daa2bf4a1f0a3fff634cfa831e2639a  proof_07_badger_combat_poses_stage.png (1280x720, 314 KB)
b5fb3593f3d4e8da664abb63fbee734f  proof_08_bison_combat_poses_stage.png (1280x720, 313 KB)
192228cb0bf3844c639642579e05846b  proof_09_creation_flow_audit_badger_armadillo.png (1280x720, 262 KB)
6fdac1db289a04fba90f79899cce913c  proof_10_wardrobe_flow_audit_badger.png (1280x720, 437 KB)
fa1cd6a499fb266da51dbbfec03c6191  proof_11_battle_flow_audit_badger_and_bison.png (1280x720, 1197 KB)
8b85e9dd46fd263e1ed2028ffeafee14  proof_12_i18n_and_emoji_audit.png (1280x720, 229 KB)

crops/27ebc59c6910fae0746b339b2306a5ac  crops/crop_01_badger_paperdoll_7_slots.png (220x240)
crops/47b5c247dbb0352159fdfc2682f0b6f8  crops/crop_02_badger_bare_chassis.png (220x240)
crops/3d5e0d6cb5d1e15f2f828475138694ef  crops/crop_03_badger_unarmed.png (220x240)
crops/747ad64e89c343c3ea4801feef2892fb  crops/crop_04_badger_512_torso.png (440x460)
crops/8fca9dc11f88bab7b3a219054aad2042  crops/crop_05_bison_paperdoll_7_slots.png (220x240)
crops/47498f113dfb5324ec759c17b7c57a8f  crops/crop_06_bison_512_torso.png (440x460)
crops/d55c0162e948e52cd7b7394ab726c989  crops/crop_07_badger_attack_and_skill_poses.png (420x340)
crops/39b4abaa6ec53de8c6891815fa24409e  crops/crop_08_bison_attack_and_skill_poses.png (420x340)
crops/666156143278bd621f2c822098cb61ce  crops/crop_09_creation_badger_and_guard.png (570x480)
crops/da87bf386fc2ffab40377d9f7bc3f9e6  crops/crop_10_wardrobe_badger_cards.png (630x500)
crops/6f84f3426e0c5fe41fbd9e25e3757e42  crops/crop_11_battle_badger_combat_log.png (570x270)
crops/a70e2db6df096effb713da283e4bdc38  crops/crop_12_i18n_emoji_audit_summary.png (1200x620)
```

---

## 三、 六語系在地化與世界觀稽核結論

1. **六語系 ui.json 補齊詞條**：
   - 破星蜜獾 (badger)：繁中「破星蜜獾」、簡中「破星蜜獾」、英文「The Starbreaker Honey Badger」、日文「破星の蜜穴熊」、韓文「파성 꿀오소리」、西文「El Tejón Melívoro Rompeestrellas」及七大部件名稱均已合規入庫。
   - 撼地野牛 (bison)：繁中「撼地野牛」、簡中「撼地野牛」、英文「The Groundshaker Bison」、日文「撼地の野牛 (カンチノヤギュウ)」、韓文「진지들소」、西文「El Bisonte Tiemblatierra」及七大部件名稱均已合規入庫。
   - 熔鎧犰狳 (armadillo)：繁中「熔鎧犰狳」、簡中「熔铠犰狳」、英文「The Crucible Armadillo」、日文「溶鎧のアルマジロ」、韓文「용광로 아르마딜로」、西文「El Armadillo del Crisol」及七大槽位佔位名稱均已入庫。
2. **0-UI1 / 31d 零系統 Emoji 稽核**：
   - 六語系 ui.json 全域搜尋 0 系統 Emoji。
   - 創角、衣櫥、戰鬥、舞台全介面 0 系統 Emoji，按鈕熱區高度 >= 48px。
3. **CANON.md 玩具世界觀查驗**：
   - 破星蜜獾高分子耐熱聚合物太空素體、野牛廢土馬口鐵厚重素體、犰狳熔爐鍛鐵素體，100% 零真毛皮、零真生物血肉，背後必帶發條鑰匙。
4. **自動化測試全綠**：
   - `python3 tools/verify_bison_0_qa30.py`: PASS (49 族 aliases 100% 對齊)
   - `python3 tools/verify_badger_0_qa30.py`: PASS (49 族 aliases 100% 對齊)
   - `python3 tools/verify_armadillo_0_qa30.py`: PASS (49 族 aliases 100% 對齊)
   - `python3 tools/verify_badger_poses.py`: PASS (六大姿態邊距、陰影、運動全綠)
   - `godot --path game --headless -s res://scripts/art/test_badger_action_poses.gd`: PASS
   - `godot --path game --headless -s res://scripts/art/test_paperdoll_armadillo_skeleton.gd`: PASS
   - `godot --path game --headless -s res://scripts/art/test_paperdoll_race_switch.gd`: PASS (49 族切換還原成功)
   - `godot --path game --headless --quit-after 3`: PASS (0 SCRIPT ERROR)

---

## 四、 問題清單與後續派工建議（Findings & Next Steps）

1. **第四十六族破星蜜獾 (badger)**：
   - **現狀**：7 大槽位切片與六大戰鬥姿態雙規格貼圖已全數過審合進 main。
   - **後續派工**：待開立官方資產套件任務卡（`badger-official-assets`：官網英雄圖/戰鬥特寫/行走動畫/HUD頭像）。
2. **第四十七族澄心水豚 (capybara)**：
   - **現狀**：骨架已合入 main。切片與六姿態等待後續審查與合入。
3. **第四十八族振律啄木鳥 (woodpecker)**：
   - **現狀**：世界觀提案與資料表骨架先行建置已進 main。
   - **後續派工**：待開立 7 大槽位切片產出單。
4. **第四十九族熔鎧犰狳 (armadillo)**：
   - **現狀**：世界觀提案與資料表骨架先行建置已進 main，開啟第九巡擴充，創角介面受 `has_race_assets` 防護守衛安全隱藏。
   - **後續派工**：待開立 7 大部件槽位切片試產任務卡（`armadillo-slices`）。
