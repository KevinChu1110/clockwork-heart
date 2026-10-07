# Boss 部位破壞掉落發光寶箱動效（爆點三落地收尾） 驗收查核表 (t_d514fe7c)

## 一、任務要求與改動項目
- [x] **爆點三規範落地**：依 `docs/CLOCKWORK_HEART_GAME_OVERVIEW.md` 壹.4 爆點三規範，Boss 部位破壞（part_break）觸發時，包含 0.4s 慢動作頓挫與糖果屑，並在受擊破壞處生成彈跳落地的金色發條寶箱動效（Chest Bounce Tween 帶金色流光粒子）。
- [x] **對應部位機芯提示**：擊破特定部位 100% 決定掉落對應部位的機芯，彈出浮字提示掉落對應部位機芯（如 Leo 盔破壞提示【機殼裝甲】、Leo 盾破壞提示【傳動齒輪組】、巨偶尖角破壞提示【發條發電機】）。
- [x] **視覺風格一致**：畫面維持 Q 版玩具像素風格，金色發條寶箱帶背頂發條鑰匙、雙層落地軟陰影、金色流光粒子（CPUParticles2D），零系統 emoji，符合 review.md 19b。
- [x] **六語系對齊（review.md 0-QA27）**：機芯五槽名稱與浮字提示全 6 語系（zh_TW, zh_CN, en, ja, ko, es）完整對齊，零系統 emoji。
- [x] **單元測試與回歸驗證**：專屬測試 `test_boss_part_break_chest_fx.gd` 覆蓋五槽映射、動效元件結構、六語系及戰鬥實例化驗證，`TEST_FILTER=part_break`（3/3）全綠。

## 二、實機 Framebuffer 截圖清單（0-QA23 / 0-QA26）
| 序號 | 檔案路徑 | 驗收重點 | Vision 查驗結果 |
|---|---|---|---|
| 01 | `proofs/t_d514fe7c/proof_01_battle_before_break.png` | Leo 部位破壞前戰鬥狀態（全景橫屏 1280x720，血條與部位鎖定） | **通過 (PASS)** |
| 02 | `proofs/t_d514fe7c/proof_02_battle_part_break_chest_bounce.png` | 部位破壞瞬間寶箱彈起、金色流光粒子噴發與慢動作頓挫 | **通過 (PASS)** |
| 03 | `proofs/t_d514fe7c/proof_03_battle_part_break_chest_landed_core_prompt.png` | 寶箱落地彈跳（Squash & Stretch）與浮字提示【掉落部位機芯：機殼裝甲】 | **通過 (PASS)** |
| 04 | `proofs/t_d514fe7c/proof_04_battle_colossus_part_break_chest.png` | 停擺巨偶部位破壞寶箱掉落與【掉落部位機芯：發條發電機】提示 | **通過 (PASS)** |

## 三、自動化測試通過清單
1. `godot --path game --headless -s res://scripts/battle/test_boss_part_break_chest_fx.gd`：PASS（TEST_BOSS_PART_BREAK_CHEST_FX_OK，0 errors）
2. `TEST_FILTER=part_break ./tools/run_tests.sh`：3/3 全部通過（test_battle_part_break_i18n, test_boss_part_break_chest_fx, test_part_break）
3. `godot --path game --headless -s res://scripts/autoload/test_i18n.gd`：PASS（五語系 content/ui.json 各 3544 個 key 100% 全部對齊）
4. `TEST_FILTER=test_colossus_part_slot_drop ./tools/run_tests.sh`：1/1 全部通過
5. `/root/bin/clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_d514fe7c`：✅ 全過（素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞）
