# ClockworkVaultDialog 前往心法快捷果凍按鈕驗收清單 (t_64581b7f)

## 驗收項目
- [x] 按鈕節點命名：`BtnGoSkill`，位於 `ClockworkVaultDialog` 底部操作按鈕列 (`foot_box`)
- [x] 按鈕尺寸熱區合規：寬度 102px >= 100px、高度 52px >= 48px，符合手機觸控熱區規範
- [x] 多巴胺果凍厚底規範：珊瑚粉底色 `#FF5E8A`、底邊厚底 5px、圓角 18px、深藍紫描邊 `#1F1A3A`
- [x] 100% 零系統 Emoji：全介面與按鈕文字皆純文字開源粉圓體渲染，無廉價 Unicode Emoji
- [x] 點擊連動：點擊發射 `skill_requested`、`go_skill` 與 `closed` 信號，安全關閉儲能庫彈窗（無遮罩殘留）並直通呼起 `SkillDialog`
- [x] 存取器提供：提供 `get_go_skill_button()` 與 `get_skill_button()` 存取器
- [x] 六語系 i18n 完整支援：
  - 繁體中文 (zh_TW)：前往心法
  - 簡體中文 (zh_CN)：前往心法
  - 英文 (en)：To Skills
  - 日文 (ja)：心法へ
  - 韓文 (ko)：심법으로
  - 西班牙文 (es)：A Habilidades
- [x] 實機截圖完整存證，8 張截圖無黑屏、雜湊全部獨立唯一

## 存證檔案
- `proof_01_zh_TW_clockwork_vault_dialog_btn_go_skill.png`
- `proof_02_click_btn_go_skill_opens_skill_dialog.png`
- `proof_03_loop_back_to_vault.png`
- `proof_04_zh_CN_clockwork_vault_dialog_btn_go_skill.png`
- `proof_05_en_clockwork_vault_dialog_btn_go_skill.png`
- `proof_06_ja_clockwork_vault_dialog_btn_go_skill.png`
- `proof_07_ko_clockwork_vault_dialog_btn_go_skill.png`
- `proof_08_es_clockwork_vault_dialog_btn_go_skill.png`
