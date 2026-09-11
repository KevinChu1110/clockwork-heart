# Paper Doll v2 組裝（W6-K3）

權威 JSON：`game/data/ken/w6_k3_paper_doll.json`（Slots／Anim／WeaponClass）。

## 硬規則

| 規則 | 實作 |
|------|------|
| 副手 MVP = empty | `PaperDollAssembler.equip("weapon_off", …)` 拒非 `empty` |
| WeaponClass MVP = one_hand | `two_hand`／`dual_wield`／`fists` 被擋 |
| 背鑰永在背 | `back_key` 不可裝進 `weapon_main`／`weapon_off`；探索／戰鬥／拆解皆可見 |
| chest_heart ↔ WindStaminaGlow | JSON `bindsHud`；`PaperDollView.chest_anchor` 給 `ChestGlowHud` |
| 舊電影 3D 皮退役 | §8 改吃 `pack_a/v2/xiaobai_{e03,b02,d02}.png` |

## 模組

- `paper_doll_config.gd` — 讀 JSON
- `paper_doll_assembler.gd` — loadout／相位／Anim 規則
- `paper_doll_view.gd` — 顯示 + 胸口錨點
- `test_paper_doll_v2.gd` — headless

層切單圖未齊前，三相用 Alice 整圖 composite；SlotId 結構已就位。詳見 `PAPER_DOLL_LAYERS.md`／`PAPER_DOLL_SYSTEM.md`。
