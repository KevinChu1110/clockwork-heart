# DummySettlementDialog 調整心法快捷按鈕實機截圖與驗收清單 (t_f8bc43d5)

## 驗收項目與依據
- 依據需求：木人樁試招結算數據卡（DummySettlementDialog）底部按鈕列新增『調整心法』快捷按鈕（BtnGoSkills），並連動開啟 SkillDialog。
- 尺寸與熱區規範：尺寸 >= 170x52px，高度 >= 50px，點擊熱區 >= 48px。
- 多巴胺果凍樣式：天藍色底（COLOR_SKY #38A0FF），深藍紫描邊 2px（COLOR_BORDER #1F1A3A），圓角 20px，立體果凍厚底 6px，粉圓體字級 18px（>= 16px）。
- 零系統 Emoji：純淨文字手繪風格，無廉價 Emoji。
- 信號與回調：點擊後發出 `skills_requested` 信號與 `on_skills` 回調，自動呼叫 `queue_free()` 關閉結算彈窗。
- 遊戲連動閉環：BattleView 正確轉發 `skills_requested`；MobileLobby 順暢開啟 SkillDialog，實現試招數據分析與招式心法即時調整。
- 六語系即時切換：支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`。

## 截圖存證清單 (OpenGL3 Framebuffer 真實截圖)
- `proof_01_dummy_settlement_zh_TW.png`: 繁中全景 (1280x720) - 再次試招、調整心法、完成試招三鍵並列
- `crops/crop_01_buttons_zh_TW.png`: 繁中按鈕列特寫 (566x68)
- `proof_02_dummy_settlement_zh_CN.png`: 簡中全景 (1280x720) -「调整心法」
- `crops/crop_02_buttons_zh_CN.png`: 簡中按鈕列特寫 (566x68)
- `proof_03_dummy_settlement_en.png`: 英文全景 (1280x720) - "Adjust Skills"
- `crops/crop_03_buttons_en.png`: 英文按鈕列特寫 (566x68)
- `proof_04_dummy_settlement_ja.png`: 日文全景 (1280x720) -「心法調整」
- `crops/crop_04_buttons_ja.png`: 日文按鈕列特寫 (566x68)
- `proof_05_dummy_settlement_ko.png`: 韓文全景 (1280x720) -「심법 조정」
- `crops/crop_05_buttons_ko.png`: 韓文按鈕列特寫 (566x68)
- `proof_06_dummy_settlement_es.png`: 西班牙文全景 (1280x720) - "Ajustar habilidades"
- `crops/crop_06_buttons_es.png`: 西班牙文按鈕列特寫 (613x68)
- `proof_07_skill_dialog_opened_lobby.png`: 點擊調整心法後由 MobileLobby 開啟 SkillDialog 全景 (1280x720)
- `crops/crop_07_skill_dialog.png`: SkillDialog 彈窗特寫 (760x560)

## 檢查結論
- 實機驗證無破圖、無溢出、無截字，文字清晰，六語系支援完整，連動流程運作順暢。
