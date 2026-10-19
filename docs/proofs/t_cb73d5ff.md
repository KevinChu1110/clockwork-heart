# 任務驗收存證：t_cb73d5ff

## 任務摘要
- **任務名稱**：🎮 遊戲介面｜大廳聚魂殿堂底欄新增『前往心法』快捷果凍按鈕聯動 SkillDialog
- **卡號**：`t_cb73d5ff`
- **執行人**：阿宏 (sideworker)
- **分支**：`agent/20261019-soul-hall-skill-shortcut-t_cb73d5ff`

---

## 驗收重點與規格檢驗
1. **按鈕規格樣式**：
   - 按鈕名稱：`BtnGoSkill`，位於 `MobileLobby` 大廳聚魂殿堂分頁（`_build_soul_hall_tab`）底部操作列 (`bot_h`)。
   - 尺寸與熱區：`custom_minimum_size` 為 `(140, 52)`，高度 >= 50px，寬度 >= 48px，完全符合行動端防誤觸與觸控熱區規範。
   - 樣式規範：多巴胺天藍底色 `#38A0FF`、深藍紫描邊 `#1F1A3A`（寬 2px）、果凍厚底 5px、圓角 18px、字級 16px 開源粉圓體、100% 零系統 Emoji、零特殊字元圖示。
2. **點擊連動與訊號發射**：
   - 點擊 `BtnGoSkill` 播放 UI 音效並發射 `skill_requested` 訊號。
   - 調用 `open_skill_dialog()` 順暢開啟心法招式彈窗 (`SkillDialog`)。
   - 雙向閉環：在 `SkillDialog` 中點擊『前往聚魂』(`BtnGoSoulHall`) 可安全關閉彈窗並切換回聚魂殿堂，無遮罩穿透、無殘留。
3. **公開存取器**：
   - 提供 `get_soul_hall_go_skill_btn()`、`get_btn_soul_go_skill()`、`get_soul_hall_skill_btn()`。
4. **六語系即時在地化切換**：
   - zh_TW: `前往心法`
   - zh_CN: `前往心法`
   - en: `To Skills`
   - ja: `心法へ`
   - ko: `심법으로`
   - es: `A Habilidades`
   - 六語系動態即時切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。
5. **程式穩定度**：
   - 無任何 `SCRIPT ERROR`、`Parse Error`、無遮罩穿透問題。

---

## 實機截圖存證清單 (xvfb-run OpenGL3 真實 Framebuffer 渲染)

| 截圖檔名 | 說明 | 雜湊 (SHA256) |
|---|---|---|
| `proof_01_zh_TW_soul_hall_btn_go_skill.png` | 繁中聚魂殿分頁：底欄展示天藍色立體果凍按鈕『前往心法』(140x52px) | `b3627f01eddb55321ef25178ae9b7dd6a62f3e465d297453446162e26ca5cbf7` |
| `proof_02_zh_TW_skill_dialog_opened.png` | 點擊前往心法：連動開啟 SkillDialog 心法招式彈窗，底部展示『前往聚魂』按鈕 | `0e429507d8f2d9623e047cd7a12ed5cd4ac33de209e02c54d1aec5467ce03112` |
| `proof_03_zh_TW_loop_back_to_soul_hall.png` | 雙向閉環：從心法彈窗點擊『前往聚魂』安全關閉心法彈窗返回聚魂殿堂 | `0622a7badad5d830eaace673d3d4fb513bdd04ff107fc4d134e1d03d95170ca3` |
| `proof_04_zh_CN_soul_hall_skill_btn.png` | 簡中 (zh_CN) 即時切換：前往心法 | `6dced41c37df6fbeb3b7d075574a76bcfe6e2d0039437f6b698d7d1c8070f4d5` |
| `proof_05_en_soul_hall_skill_btn.png` | 英文 (en) 即時切換：To Skills，零 CJK 殘留 | `9d3f89a0e1004c370c07f56ae21422ac508ed6e3ee4811b99b719fd5ed7c677a` |
| `proof_06_ja_soul_hall_skill_btn.png` | 日文 (ja) 即時切換：心法へ | `1f2074c9ca5ef8e92d05bf630dad0bcd7b40ca5bf359d25d436e3037f6144d59` |
| `proof_07_ko_soul_hall_skill_btn.png` | 韓文 (ko) 即時切換：심법으로 | `9df53ac3c946f81ff85f4b3d4c8eb162ae4cdd259ccf397e82a32184349bf659` |
| `proof_08_es_soul_hall_skill_btn.png` | 西班牙文 (es) 即時切換：A Habilidades，零 CJK 殘留 | `369e60f20224868c3537fd938edf21f08f72b271b7e7b8202b94fa887c3bdc52` |

---

## 哨兵結果
`TEST_SOUL_HALL_SKILL_SHORTCUT_OK`
