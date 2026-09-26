# 武術館兵器架十二流派名稱與說明六語系驗收清單 (t_9d4df0da)

依據 `references/review.md` 規範（0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25）與任務驗收條件：

## 一、驗收總覽
- [x] **0-QA23 獨立目錄**：所有交付截圖與裁切圖嚴格限定於 `proofs/weapon-classes-i18n/`，無修改或覆蓋其他任務之 proof。
- [x] **0-QA24 日韓漢字對齊語系檔**：日文版「武器系統」「現在：流派 未選択 · Lv1」「剣・騎士・剣」等漢字完全對齊 `ja.json` 與 `content/ja/ui.json`。
- [x] **0-QA25 全景與即時連動**：全景實機截圖中彈窗標題、引言說明、狀態行、流派按鈕皆與當前語系完全一致。
- [x] **修復 S/E 問題**：`en/ui.json` 修正 `"劍": "Sword"`（徹底清除單字母 S）；`es/ui.json` 修正 `"劍": "Espada"`。
- [x] **十二流派六語系覆蓋**：`game/data/i18n/content/<locale>/weapon_class.json` 完整補齊 12 流派之 `name`, `title`, `tagline`, `play`, `pros`, `cons`。
- [x] **按鈕格式規範**：en 顯示 `Sword · Knight · Sword`，ja 顯示 `剣・騎士・剣`，不再出現繁中或單字母 S。
- [x] **零系統 Emoji**：介面、按鈕與文本全數無系統 emoji。
- [x] **數值與養成守護**：攻防數值、職業對應、初始武器（starter_weapon）完全不變。官網 `web/data/weapon_classes.json` 未動。

## 二、單元測試驗收 (test_weapon_classes_i18n.gd)
- 執行命令：`godot --path game --headless --script res://scripts/systems/test_weapon_classes_i18n.gd`
- 驗證結果：6 語系全部通過（Exit code 0）。
  - `zh_TW`: 劍·騎士·劍、長槍·騎士·槍、弓·遊俠·弓
  - `zh_CN`: 剑·骑士·剑、长枪·骑士·枪、弓·游侠·弓
  - `en`: Sword · Knight · Sword、Spear · Knight · Spear、Bow · Ranger · Bow（劍確認為 Sword，非 S）
  - `ja`: 剣・騎士・剣、長槍・騎士・槍、弓・レンジャー・弓
  - `ko`: 검·기사·검、창·기사·창、활·레인저·활
  - `es`: Espada · Caballero · Espada、Lanza · Caballero · Lanza、Arco · Guardabosques · Arco
- 無頭冒煙測試：`godot --path game --headless --quit-after 3` 0 錯誤、無 SCRIPT ERROR。

## 三、實機截圖存證
1. `proofs/weapon-classes-i18n/proof_01_weapon_classes_en.png` (1280x720 全景實機，en)
2. `proofs/weapon-classes-i18n/proof_02_weapon_classes_ja.png` (1280x720 全景實機，ja)
3. `proofs/weapon-classes-i18n/crops/crop_01_weapon_classes_en.png` (局部特寫，en)
4. `proofs/weapon-classes-i18n/crops/crop_02_weapon_classes_ja.png` (局部特寫，ja)
