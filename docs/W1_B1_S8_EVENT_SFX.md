# W1-B1 · §8 標準場事件節點＋音效 cue

> Owner：Bingo｜對齊 `ART_STANDARD_SCENE_S8`（探索→戰鬥→拆部位）  
> 對接：Ken（發條體力 15／部位破壞數值）、Frank（三系統分檔）、Alice（三態畫面）  
> 風格鎖：多巴胺 Q 金屬發條玩具——齒輪嘀嗒、黃銅彈簧、青綠之心，⛔ 不做科幻機甲／恐怖／pixel UI 音

---

## 0. 變數對接（給 Ken／Frank）

| 變數 | 用途 | 來源假設（可被 Ken JSON 覆寫） |
|------|------|------------------------------|
| `WindStamina` | 發條體力，上限 15 | SYSTEMS / PRODUCT_LOCK |
| `WindCost_Explore` | 進探索節點消耗（E02） | **1**（Ken W1-K1） |
| `WindCost_Battle` | 開戰消耗（B01） | **2**（Ken W1-K1） |
| `WindCost_Dismantle` | 拆部位消耗（D01） | **2**（Ken W1-K1） |
| `PartUnlockHP` | 本體 HP 比例解鎖破部位 | 0.70（COMBAT §6.2） |
| `PartId` | 部位 id：`helm` / `armor` / `boot` / `core` | COMBAT 分型 |

體力不足：擋開戰／拆部位，播 `sfx.ui.wind_empty`，提示「發條轉不動了」。

---

## 1. 流程總覽

```
[Explore] enter → interact* → encounter_gate
    → [Battle] start → loop(hit/crit/skill/part*) → end
    → [Dismantle] start → pick_part → extract → complete
    → 回探索或回城
```

---

## 2. 事件節點表

### A. 探索 `Explore`

| 節點 ID | 觸發 | 劇情節拍（短） | 下一個 |
|---------|------|----------------|--------|
| `E01_enter_node` | 進野外節點 | 小白落地，背鑰輕轉一格 | `E02` |
| `E02_wind_spend` | 扣 `WindCost_Explore` | HUD 發條條閃一下 | `E03` |
| `E03_ambient_loop` | 場景就緒 | 可走動／調查 | `E04` / `E05` |
| `E04_interact_point` | 點調查點 | 短文／撿零件（非戰鬥） | `E03` |
| `E05_encounter_shadow` | 接觸敵影或節點自動遇敵 | 「齒輪聲靠近」預警 0.4s | `E06` |
| `E06_to_battle` | 確認進戰 | 轉場遮罩：青綠光一閃 | `B01` |

### B. 戰鬥 `Battle`

| 節點 ID | 觸發 | 劇情節拍（短） | 下一個 |
|---------|------|----------------|--------|
| `B01_battle_start` | 進戰鬥場景 | 扣 `WindCost_Battle`；佈陣 | `B02` |
| `B02_combat_loop` | tick／狀態機 | 自動互毆＋玩家鎖敵／技／格擋 | 各戰鬥 cue |
| `B03_part_unlock` | 敵本體 HP ≤ `PartUnlockHP` | 部位條亮起；「露出接縫了」 | `B02` |
| `B04_part_focus` | 玩家鎖部位 | 鏡頭微推該部位 | `B02` |
| `B05_part_broken` | 部位 HP≤0 | 彈簧崩開演出；套用 Ken 效果 | `B02` |
| `B06_enemy_down` | 敵死亡 | 倒地、零件鬆動 | `B07` |
| `B07_battle_end` | 勝／敗結算 | 勝→`D01`；敗→回探索（不拆） | `D01` / `E03` |

### C. 拆部位 `Dismantle`

| 節點 ID | 觸發 | 劇情節拍（短） | 下一個 |
|---------|------|----------------|--------|
| `D01_dismantle_start` | 戰鬥勝利後 | 扣 `WindCost_Dismantle`；進入拆解 UI | `D02` |
| `D02_part_select` | 選可拆殘件 | 高亮螺絲／接縫（對齊憲法乾淨烤漆可讀） | `D03` |
| `D03_unscrew` | 確認拆 | 2～3 段旋開節奏 | `D04` |
| `D04_part_extract` | 抽出完成 | 殘片入袋；敘事名給 Ken 掉落表 | `D05` or `D02` |
| `D05_core_glint` | 抽到核心碎片時 | 青綠心一閃（稀有感） | `D06` |
| `D06_dismantle_complete` | 關閉拆解 | 回探索或結算回城 | `E03` / Town |

---

## 3. 音效 cue 表（給 Frank 綁事件）

命名：`sfx.<phase>.<action>`｜優先級對齊 COMBAT §10（P0/P1/P2）

### 共用／UI

| Cue ID | Pri | 感覺描述 | 綁節點 |
|--------|-----|----------|--------|
| `sfx.ui.wind_tick` | P0 | 發條鑰匙短嘀嗒 1 格 | `E02` / 體力變動 |
| `sfx.ui.wind_empty` | P0 | 發條空轉＋悶金屬 | 體力不足擋操作 |
| `sfx.ui.confirm` | P2 | 輕黃銅叮 | UI 確認 |
| `sfx.ui.cancel` | P2 | 軟彈簧回彈 | UI 取消 |

### 探索

| Cue ID | Pri | 感覺描述 | 綁節點 |
|--------|-----|----------|--------|
| `sfx.explore.foot_toy` | P2 | Q 版金屬腳步（短、乾） | 移動 |
| `sfx.explore.ambient_attic` | P2 | 遠齒輪＋灰塵風（loop） | `E03` |
| `sfx.explore.interact` | P1 | 撥動小齒輪 | `E04` |
| `sfx.explore.enemy_approach` | P0 | 敵影接近：加速嘀嗒 | `E05` |
| `sfx.explore.to_battle` | P0 | 青綠 whoosh＋發條上緊 | `E06` |

### 戰鬥

| Cue ID | Pri | 感覺描述 | 綁節點／事件 |
|--------|-----|----------|--------------|
| `sfx.battle.start` | P0 | 短號角式玩具鼓＋鑰匙上弦 | `B01` / `battle_start` |
| `sfx.battle.swing` | P0 | 輕金屬揮擊 | `attack_swing` |
| `sfx.battle.hit` | P0 | 烤漆撞擊（乾脆） | `hit` |
| `sfx.battle.miss` | P1 | 空氣甩空 | `miss` |
| `sfx.battle.crit` | P1 | 撞擊＋青綠叮 | `crit` |
| `sfx.battle.skill` | P0 | 技能名可配短旋律 | `skill_cast` |
| `sfx.battle.rage_full` | P1 | 背鑰快速連轉 | `rage_changed` 滿 |
| `sfx.battle.part_unlock` | P1 | 接縫「咔」開鎖 | `B03` |
| `sfx.battle.part_break` | P1 | 彈簧崩＋零件落地 | `B05` / `part_broken` |
| `sfx.battle.enemy_die` | P0 | 發條泄力＋倒地悶響 | `B06` / `unit_died` |
| `sfx.battle.win` | P0 | 勝利短樂句（玩具音樂盒感） | `B07` 勝 |
| `sfx.battle.lose` | P0 | 發條停轉下行 | `B07` 敗 |

### 拆部位

| Cue ID | Pri | 感覺描述 | 綁節點 |
|--------|-----|----------|--------|
| `sfx.dismantle.start` | P0 | 工具箱打開（輕） | `D01` |
| `sfx.dismantle.select` | P1 | UI 掃過螺絲高亮 | `D02` |
| `sfx.dismantle.unscrew_a` | P0 | 旋鬆 1 | `D03` 段1 |
| `sfx.dismantle.unscrew_b` | P0 | 旋鬆 2 | `D03` 段2 |
| `sfx.dismantle.pop` | P0 | 零件彈出 | `D04` |
| `sfx.dismantle.core_glint` | P1 | 青綠心玻璃叮（亮） | `D05` |
| `sfx.dismantle.bag_in` | P1 | 入袋輕碰 | `D04` |
| `sfx.dismantle.complete` | P0 | 蓋上盒蓋＋滿足嘀嗒 | `D06` |

---

## 4. BGM 建議（非 cue，給後續）

| 段落 | 方向 |
|------|------|
| 探索 | 溫暖音樂盒＋遠齒輪 pad |
| 戰鬥 | 同調加速、加黃銅打擊；勝再收斂回音樂盒 |
| 拆部位 | 幾乎無 BGM，留手工拆解 SFX 空間 |

---

## 5. 驗收（W1-B1）

- [ ] 三態節點 ID 齊：`E*` / `B*` / `D*`
- [ ] 所有 P0 cue 有唯一 ID，可被 Frank 事件匯流排訂閱
- [ ] 體力扣點節點：`E02` `B01` `D01` 與 Ken `WindStamina=15` 對得上
- [ ] 部位鏈：`B03→B04→B05` 對齊 `PartUnlockHP` 與 `part_broken`
- [ ] 音感描述無科幻／恐怖／8-bit pixel 指向



---

## 6. Ken W1-K1 對齊（2026-09-11）

| Ken | Bingo 掛點 |
|-----|------------|
| `E02_exploreTick` cost 1 | `E02_wind_spend` + `sfx.ui.wind_tick` |
| `B01_combatEnter` cost 2 | `B01_battle_start` |
| `D01_dismantleEnter` cost 2 | `D01_dismantle_start` |
| `B_strike` cost 1 | `sfx.battle.swing` 觸發時另扣（可選） |
| `D_pullPart` cost 1 | `D04_part_extract` |
| `DropId=drop_brass_gear` | `D04` 入袋敘事「黃銅齒輪」 |
| `DropId=drop_spring_coil` | `D04`「發條彈簧」 |
| `DropId=drop_core_shard` | `D05` + `sfx.dismantle.core_glint` |

部位 PartId 改跟 Ken：`gear_brass` / `spring_coil` / `core_shard`（不再用 helm/armor/boot 暫名）。
