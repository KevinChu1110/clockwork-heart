# 驗收清單：t_c48032bf 多餘未裝備機芯拆成既有鐵屑

- **任務編號**：`t_c48032bf`
- **負責人**：阿翔（側案·工程師）
- **專案進度 ID**：`bag-core-dismantle`
- **參照規範**：`AGENTS.md` (驗證階梯), `review.md` (0-QA5, 0-QA23, 0-QA24, 0-QA26, 0-QA28, 0-QA29)

---

## 一、實機截圖成果清單 (0-QA5, 0-QA23, 0-QA26)

| 編號 | 檔名 | 語系 | 驗收重點 | 瑕疵數 | 系統 Emoji | 截字溢出 | 判定 |
|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|
| 01 | `proof_dismantle_btn_zh_TW.png` | 繁中 (zh_TW) | 機芯部件背包卡片具備粉紅果凍厚底「拆解」按鈕（高 ≥50px，底邊 5px），色階色票完整，零系統 emoji | 零 | 零 | 無 | **通過 (PASS)** |
| 02 | `proof_dismantle_btn_en.png` | 英文 (en) | 英文大廳背包機芯卡片按鈕顯示為「Dismantle」，100% 零中文 CJK 殘留（0-QA28），零系統 emoji | 零 | 零 | 無 | **通過 (PASS)** |
| 03 | `proof_dismantled_toast_zh_TW.png` | 繁中 (zh_TW) | 點擊「拆解」按鈕即時彈出 Toast 提示「已拆解機芯，獲得 4 鐵屑」，背包扣除該機芯（3張變2張），鐵屑入袋（道具欄出現鐵屑×4） | 零 | 零 | 無 | **通過 (PASS)** |
| 04 | `proof_bag_empty_after_dismantle_zh_TW.png` | 繁中 (zh_TW) | 機芯全數拆解完畢後，CoreBagPanel 正確自動收合隱藏，無多餘留白破版 | 零 | 零 | 無 | **通過 (PASS)** |

---

## 二、色階鐵屑數量寫死對照表驗證

對照精神對齊既有裝備拆解，寫死對照表如下：
- **灰階 (gray)**：回收 1 鐵屑 (`iron_scrap`)
- **白階 (white)**：回收 2 鐵屑 (`iron_scrap`)
- **橘階 (orange)**：回收 3 鐵屑 (`iron_scrap`)
- **藍階 (blue)**：回收 4 鐵屑 (`iron_scrap`)
- **紫階 (purple)**：回收 5 鐵屑 (`iron_scrap`)
- **金階 (gold)**：回收 6 鐵屑 (`iron_scrap`)
- **綠階 (green)**：回收 8 鐵屑 (`iron_scrap`)
- **紅階 (red)**：回收 10 鐵屑 (`iron_scrap`)

安全規範：
- 已裝備槽上的機芯拒絕拆解 (`ok: false`, `reason: "is_equipped"`)，不扣裝備、不給鐵屑。
- 不引入新道具，100% 使用既有 `iron_scrap`。
- 不改動任何戰鬥時間模型（ATB、前搖、格擋窗、攻速）。

---

## 三、六語系 ui.json 對齊檢驗 (0-QA28, 0-QA29)

全 6 語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）鍵值對齊：
1. **拆解按鈕**：
   - `zh_TW`: `"拆解"`
   - `zh_CN`: `"拆解"`
   - `en`: `"Dismantle"`（零中文 CJK）
   - `ja`: `"分解"`（依既定日文用語對齊）
   - `ko`: `"분해"`
   - `es`: `"Desarmar"`
2. **拆解 Toast 提示**：
   - `zh_TW`: `"已拆解機芯，獲得 %d 鐵屑"`
   - `zh_CN`: `"已拆解机芯，获得 %d 铁屑"`
   - `en`: `"Core dismantled, gained %d Scrap Iron"`
   - `ja`: `"コアを分解し、鉄屑を %d 個獲得"`
   - `ko`: `"코어를 분해하여 철 부스러기 %d개 획득"`
   - `es`: `"Núcleo desarmado, obtuviste %d chatarra"`
3. **拒拆安全提示**：
   - `zh_TW`: `"已裝備槽上的機芯不可拆"`
   - `zh_CN`: `"已装备槽上的机芯不可拆"`
   - `en`: `"Equipped core cannot be dismantled"`
   - `ja`: `"装備中のコアは分解できません"`
   - `ko`: `"장착 중인 코어는 분해할 수 없습니다"`
   - `es`: `"No se puede desarmar un núcleo equipado"`

---

## 四、驗證結果

1. **單元測試**：
   - `TEST_FILTER=bag_core_dismantle ./tools/run_tests.sh`: 1/1 PASS（`TEST_BAG_CORE_DISMANTLE_OK`）
   - `TEST_FILTER=core ./tools/run_tests.sh`: 8/8 PASS（機芯相關測試全部通過）
   - `TEST_FILTER=equipment_dismantle ./tools/run_tests.sh`: 1/1 PASS（既有裝備拆解回歸綠燈）
2. **無頭冒煙測試**：
   - `godot --path game --headless --quit-after 3` 0 script error。
3. **實機截圖**：
   - 透過 `xvfb-run` 產生 1280x720 真機 framebuffer png，經 `vision_analyze` 檢查，果凍厚底（5px）、高度 ≥50px、零 emoji、en 零 CJK 殘留、空背包不破版全部符合。
