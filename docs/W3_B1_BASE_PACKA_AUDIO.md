# W3-B1 · Base key vs Pack-A 音檔對照

> 對齊 Ken W3-K1／`bundle_manifest.json`｜缺 Pack → 靜音占位不擋 `s8.*` 流程

## Base（主包，僅 ID／字串）

| key | 類型 | Pack-A 檔名建議 |
|-----|------|-----------------|
| `s8.e01`～`s8.d06`、`s8.err_stamina` | 對白字串 | （語音若做）`vo/s8_*.ogg` 另列 Pack-B） |
| `sfx.ui.wind_tick` | cue | `sfx/ui/wind_tick.ogg` |
| `sfx.ui.wind_empty` | cue | `sfx/ui/wind_empty.ogg` |
| `sfx.explore.ambient_attic` | cue | `sfx/explore/ambient_attic.ogg` |
| `sfx.explore.interact` | cue | `sfx/explore/interact.ogg` |
| `sfx.explore.enemy_approach` | cue | `sfx/explore/enemy_approach.ogg` |
| `sfx.explore.to_battle` | cue | `sfx/explore/to_battle.ogg` |
| `sfx.battle.start` | cue | `sfx/battle/start.ogg` |
| `sfx.battle.swing` | cue | `sfx/battle/swing.ogg` |
| `sfx.battle.hit` | cue | `sfx/battle/hit.ogg` |
| `sfx.battle.crit` | cue | `sfx/battle/crit.ogg` |
| `sfx.battle.part_unlock` | cue | `sfx/battle/part_unlock.ogg` |
| `sfx.battle.part_break` | cue | `sfx/battle/part_break.ogg` |
| `sfx.battle.enemy_die` | cue | `sfx/battle/enemy_die.ogg` |
| `sfx.battle.win` | cue | `sfx/battle/win.ogg` |
| `sfx.dismantle.start` | cue | `sfx/dismantle/start.ogg` |
| `sfx.dismantle.unscrew`（或 `_a`/`_b`） | cue | `sfx/dismantle/unscrew.ogg` |
| `sfx.dismantle.core_glint` | cue | `sfx/dismantle/core_glint.ogg` |
| `sfx.dismantle.complete` | cue | `sfx/dismantle/complete.ogg` |

## Pack-A（外掛）

- 上表全部 `.ogg`（可先 P0：wind_tick／battle.start／swing／hit／part_break／dismantle.unscrew／core_glint）
- 探索 ambient loop
- （圖）Alice 三態定稿＋找碴圖——不歸我出，只對齊路徑約定 `art/xiaobai_*`／`art/find_bug_*`

## 狀態

- 對照表：✅ 本檔
- 真音檔：⏳ 等額度／Suno 或 Pack 產線；煙測維持靜音
