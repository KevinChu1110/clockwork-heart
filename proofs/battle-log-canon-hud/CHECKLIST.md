# 戰鬥日誌世界觀用詞、英文攻擊鈕折字、日誌收尾標籤修復驗收報告 (battle-log-canon-hud)

任務卡號：`t_14507d4c`
負責人：阿翔（sideworker2）
日期：2026-09-27

---

## 一、修復項目對照與成果

| 項次 | 缺陷描述 | 原狀況 | 修復後 | 驗證證據 |
|---|---|---|---|---|
| 1 | 繁中戰鬥日誌舊武俠/肉身詞 | `敵手筋骨結實（防爆高）——爆擊難進，斧鎚硬砸最實在。` | `敵手金屬板件厚實（防爆高）——爆擊難進，發條重擊最實在。` | 零筋骨、零斧鎚、零肉身詞；含金屬板件、發條；六語系同步對齊，切語系即時刷新 |
| 2 | 英文常態攻擊按鈕單字折行 | 寬度 88px + content margin 44px < 文字 50px，被折成 `Attac` / `k` | 按鈕寬度設為 108px，關閉自動折行（`AUTOWRAP_OFF`），字級 16px，`Attack` 完整同一行 | 高度 72px >= 48px，多巴胺金黃果凍厚底，零 emoji，不截字 |
| 3 | 英文日誌王者斬結算露出 `[/b]` | 方括號 `[The King's Cut]` 被誤解析為非法 BBCode 導致粗體收尾標籤露出；技能名與敵名無空格 | 跳脫方括號為 `[lb]...[rb]`，日誌層加入安全跳脫；技能名與敵名中間加入空格分隔 | 日誌結尾 100% 零 `[/b]` 露出，`[The King's Cut] Rampant Clockwork Lion deals 65 damage` |

---

## 二、實機截圖存檔 (proofs/battle-log-canon-hud/)

- `proof_01_zh_parry_failure_kings_cut.png`：繁中 (zh_TW) 實機戰鬥受王者斬畫面
  - 日誌第 1 行：`敵手金屬板件厚實（防爆高）——爆擊難進，發條重擊最實在。`
  - 日誌第 4 行：`【王者斬】 失控發條獅 造成 65 傷害`
  - 右下角按鈕：多巴胺金黃「攻擊」按鈕（高 72px，無 emoji）
- `proof_02_en_parry_failure_kings_cut.png`：英文 (en) 實機戰鬥受王者斬畫面
  - 日誌第 1 行：`Sturdy metal plates (high crit guard) — crits struggle; windup strikes hit hardest.`
  - 日誌第 4 行：`[The King's Cut] Rampant Clockwork Lion deals 65 damage`（零 `[/b]`，有空格）
  - 右下角按鈕：多巴胺金黃「Attack」按鈕（完整單字在同一行，高 72px，無 emoji）

---

## 三、驗收清單

- [x] **0-QA5 / 0-QA26**：走 `xvfb-run -a godot` 從 Viewport Framebuffer 截取，非 PIL 繪製，無空圖、無 0-byte。
- [x] **0-QA27**：六語系 enemy.json 與 ui.json 一致，停擺巨偶名冊無分流。
- [x] **0-QA28**：玩家可見字 100% 走翻譯層（六語系 `ui.json` 同步落地）。
- [x] **世界觀符合**：100% 零筋骨、零斧鎚、零肉身詞；金屬板件、發條玩具用語。
- [x] **零系統 Emoji**：介面、按鈕與日誌全域無彩色系統 Emoji。
- [x] **戰鬥秒數未動**：ATB / 前搖 1.85s / 格擋窗 0.85s 完全未更動，`test_colossus_windup_parry.gd` 通過。
