# balance_data · #75 推薦等級重估的原始資料

> 分析用資料，**不是專案程式、不在 CI**。對應文件：`docs/BALANCE.md` §6.1～§6.3（Refs #75）。

## 檔案

| 檔案 | 內容 |
|---|---|
| `sweep_75_raw.csv` | 全部勝場數。欄位：`series, boss_or_mode, level, wins, runs, seed_base, extra` |
| `sweep_75.gd.txt` | 掃描腳本（`extends SceneTree`）。用法見下。副檔名加 `.txt` 是為了不被 Godot 當成專案腳本載入 |

## series 對照

| series | 戰鬥規則 | 程式 |
|---|---|---|
| `prob_974_on` | 機率彈開（PR #17 `auto_react()`）＋ 974a00f2 邏輯（＝現行 main 與 PR #43 head） | PR #43 head `fdd9ca4b` |
| `prob_974_off` | 機率彈開，**把 974a00f2 對 `battle_sim.gd` 的修改整份反向套用**（`git apply -R`） | 同上 + 反向 patch，僅 scratch |
| `force_974_on` | 舊的必彈開（`try_react()`）＋ 974a00f2 | `fdd9ca4b` |
| `force_974_off` | 必彈開，無 974a00f2 | 同 `prob_974_off` |
| `prob_974_component_off_no_spd／no_prd／no_ret／all` | 機率彈開，只關掉 974a00f2 的一項：1 號槽 +1 速／暴擊累積（PRD）／最後一擊必過載／三項全關。用環境變數在 scratch 副本裡開關 | `fdd9ca4b` + scratch 修改 |
| `confirm_prob_974_on` | 在選定等級用獨立 seed（9000+）加跑 400 場 | `fdd9ca4b` |
| `world_modes_prob_974_on` | 非 Boss 出征關卡與巨偶（無機芯），每級 100 場 | `fdd9ca4b` |
| `colossus_white_core／blue_core／purple_core` | 停擺巨偶，機芯模型照抄矩陣測試，每級 150 場 | `fdd9ca4b` |
| `loadout_lv30_prob_974_on` | Lv30 加閃避／速度／機芯的配置模擬（`extra` 欄寫配置），每格 200 場 | `fdd9ca4b` |

玩家模型一律是 `test_boss_curve._stats()`（白板劍流派、一路鍛造、閃避 0），除非 `extra`／series 另有說明。
各 Boss 的進戰防禦加成同 `test_boss_curve` 的 `CURVE`；`loadout` 系列對部分 Boss 的加成與 `CURVE` 一致（falcon 2、boar 3、demon 4、wrath 3、chrono 2、statue 3）。

## 重跑

```bash
# 1. 檢出 PR #43 head 到 scratch worktree，先匯入一次資源
git worktree add --detach /workspace/wt/scratch-75 fdd9ca4b
cd /workspace/wt/scratch-75/game && godot --headless --path . --import
# 2. 把 sweep_75.gd.txt 複製成 game/scripts/battle/sweep_75b.gd，然後：
# 參數：boss 起始級 結束級 場數 seed 推薦級(0=不帶低於推薦係數) 閃避加成 速度加成 必彈開(1/0) [防禦加成 [機芯階]]
godot --headless --path . -s res://scripts/battle/sweep_75b.gd -- boar 30 30 200 7000 0 0 0 0
# 輸出：SWEEP,boss,level,wins,runs
```

## 誤差

每格 200 場時，勝率 50% 附近的標準誤差約 ±3.5 個百分點；100 場約 ±5；150 場約 ±4。
