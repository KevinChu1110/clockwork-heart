# W2-B1 · §8 煙測短對白＋cue 觸發序

> Owner：Bingo｜給 Frank 無頭／本機 smoke 掛事件  
> 對齊：W1-B1 cue、Ken W1-K1 常數、Alice 三態、Carol Prompt  
> 目標：玩家走完 **探索→戰鬥→拆部位** 一遍就能「感覺到遊戲」；語音檔可先缺，先播 placeholder / 靜音也行

---

## 0. 煙測範圍（故意極小）

| 做 | 不做 |
|----|------|
| 單一節點「玩具堆邊緣」 | 城鎮／多章／BOSS 雷歐 |
| 1 敵（鏽蝕發條鼠） | 多波、部位 3 全開可只開 1 |
| 小白一句旁白／提示 | 長對話樹 |
| 依節點觸發 `sfx.*` | 真音樂檔（可後補 Carol 生成） |

---

## 1. 觸發序（導演時間軸）

| t | 節點 | 畫面／操作 | 對白（小白／系統） | Cue |
|---|------|------------|-------------------|-----|
| 0 | `E01_enter_node` | 小白落地 | 「……背上一緊。有人上了發條？」 | `sfx.ui.wind_tick` |
| 1 | `E02_wind_spend` | 胸口光＋外圈 −1 | （系統）發條 −1 | `sfx.ui.wind_tick` |
| 2 | `E03_ambient_loop` | 可短走／點 1 調查點 | 「齒輪……還在轉。」 | `sfx.explore.ambient_attic` |
| 3 | `E04_interact_point` | 撿到鬆脫螺絲（可選） | 「黃色的……黃銅？」 | `sfx.explore.interact` |
| 4 | `E05_encounter_shadow` | 敵影靠近 | 「那邊也在響。」 | `sfx.explore.enemy_approach` |
| 5 | `E06_to_battle` | 轉場 | — | `sfx.explore.to_battle` |
| 6 | `B01_battle_start` | 體力 −2；劍出鞘 | 「別擋住路。」 | `sfx.battle.start` |
| 7 | `B02_combat_loop` | 即時互毆；揮擊可扣 `CostStrike` | — | `sfx.battle.swing` / `hit` / `crit` |
| 8 | `B03_part_unlock` | HP≤70% 部位條亮 | 「接縫開了！」 | `sfx.battle.part_unlock` |
| 9 | `B05_part_broken` | 破 `gear_brass` | 「下來！」 | `sfx.battle.part_break` |
| 10 | `B06_enemy_down` | 敵倒 | — | `sfx.battle.enemy_die` |
| 11 | `B07_battle_end` | 勝利短收 | 「還能走。」 | `sfx.battle.win` |
| 12 | `D01_dismantle_start` | 體力 −2；拆解 UI | 「一顆一顆來。」 | `sfx.dismantle.start` |
| 13 | `D02_part_select` | 高亮黃銅齒輪 | — | `sfx.dismantle.select` |
| 14 | `D03_unscrew` | 旋開 | 「……轉開。」 | `sfx.dismantle.unscrew_a`→`_b`（或 Carol 單段 `unscrew`） |
| 15 | `D04_part_extract` | 入袋 `drop_brass_gear` | 「黃銅齒輪，收好。」 | `sfx.dismantle.pop` + `bag_in` |
| 16 | `D05_core_glint` | 若掉 `drop_core_shard` | 「……亮了一下。」 | `sfx.dismantle.core_glint` |
| 17 | `D06_dismantle_complete` | 關 UI／回節點或結算 | 「發條還沒停。」 | `sfx.dismantle.complete` |

---

## 2. 對白字串表（可直接當 `tr` key）

| key | zh-TW |
|-----|-------|
| `s8.e01` | ……背上一緊。有人上了發條？ |
| `s8.e03` | 齒輪……還在轉。 |
| `s8.e04` | 黃色的……黃銅？ |
| `s8.e05` | 那邊也在響。 |
| `s8.b01` | 別擋住路。 |
| `s8.b03` | 接縫開了！ |
| `s8.b05` | 下來！ |
| `s8.b07` | 還能走。 |
| `s8.d01` | 一顆一顆來。 |
| `s8.d03` | ……轉開。 |
| `s8.d04` | 黃銅齒輪，收好。 |
| `s8.d05` | ……亮了一下。 |
| `s8.d06` | 發條還沒停。 |
| `s8.err_stamina` | 發條轉不動了。 |

---

## 3. 煙測驗收（敘事／音）

- [ ] 走完 E→B→D 不卡死，對白 key 都有掛點
- [ ] 缺音檔時節點仍前進（cue 失敗不擋流程）
- [ ] Drop 文案用 Ken `DropName`（黃銅齒輪／發條彈簧／核心碎片）
- [ ] 無藍 mana 用語；體力相關只說「發條」



> **W4 潤色**：見 [`W4_B1_S8_DIALOGUE_POLISH.md`](W4_B1_S8_DIALOGUE_POLISH.md)（以此為準）。
