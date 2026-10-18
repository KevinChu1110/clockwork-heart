# SkillDialog 心法招式底欄新增『前往儲能庫』快捷果凍按鈕驗收清單 (t_aa09bf27)

## 驗收項目
- [x] 按鈕節點命名：`BtnGoVault`，位於 `SkillDialog` 底部操作按鈕列 (`BottomBar`)
- [x] 按鈕尺寸熱區合規：寬度 140px、高度 50px >= 48px，符合手遊人體工學觸控熱區規範
- [x] 多巴胺果凍厚底規範：金黃底色 `#FFD028`、底邊厚底 5px、圓角 16px、深藍紫描邊 `#1F1A3A`
- [x] 100% 零系統 Emoji：全介面與按鈕文字皆純文字開源粉圓體渲染，無廉價 Unicode Emoji
- [x] 點擊連動：點擊發射 `vault_requested`、`go_vault` 與 `closed` 信號，安全關閉心法招式彈窗（無遮罩殘留）並直通呼起 `ClockworkVaultDialog`
- [x] 雙向閉環：關閉 `ClockworkVaultDialog` 可順暢返回 `SkillDialog` 形成雙向操作閉環
- [x] 存取器提供：提供 `get_go_vault_button()` 與 `get_vault_button()` 存取器
- [x] 底欄排版與滾動防護：BottomBar 支援平滑橫向捲動 (`BottomScroll`)，提供 `scroll_bottom_to_vault()`，多按鈕無擠壓無截斷
- [x] 六語系 i18n 完整支援：
  - 繁體中文 (zh_TW)：前往儲能庫
  - 簡體中文 (zh_CN)：前往储能库
  - 英文 (en)：To Vault
  - 日文 (ja)：貯蔵庫へ
  - 韓文 (ko)：저장고로 이동
  - 西班牙文 (es)：Ir a Bóveda
- [x] 實機截圖完整存證，8 張截圖無黑屏、雜湊全部獨立唯一

## 存證檔案
- `proof_01_zh_TW_skill_dialog_btn_go_vault.png`
- `proof_02_click_btn_go_vault_opens_clockwork_vault_dialog.png`
- `proof_03_loop_back_to_skill_dialog.png`
- `proof_04_zh_CN_skill_dialog_btn_go_vault.png`
- `proof_05_en_skill_dialog_btn_go_vault.png`
- `proof_06_ja_skill_dialog_btn_go_vault.png`
- `proof_07_ko_skill_dialog_btn_go_vault.png`
- `proof_08_es_skill_dialog_btn_go_vault.png`
