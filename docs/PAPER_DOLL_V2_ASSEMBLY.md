# Paper Doll v2 組裝（W6-K3）

權威 JSON：`game/data/ken/w6_k3_paper_doll.json`（Slots／Anim／WeaponClass）。

## 單幀（現行）

路徑：`game/assets/sprites/pack_a/v2/paper_doll/frames/`

| AnimId | 檔 |
|--------|----|
| idle / ready / hit | `oh_idle`／`oh_ready`（單手定稿）／`oh_hit` |
| one_hand_atk_1–3 | `oh_atk_1`–`3` |
| explore_walk | `explore_walk.png` |
| dismantle_pull | `dismantle_pull.png` |

| SlotId | 檔 | 備註 |
|--------|-----|------|
| outfit / helmet / weapon_main | 對應 `*_cream_enamel`／`helmet_default`／`weapon_main_sword_1h` | 可換裝圖 |
| body_base／face／chest_heart／back_key | 暫含於動作幀 | 身份層可用 |
| weapon_off | 無檔 | MVP empty |

舊 `oh_anim_strip*.png`／`explore_dismantle_anims.png` **已退役**。

## 硬規則

| 規則 | 實作 |
|------|------|
| 副手 MVP = empty | Assembler 拒非 `empty` |
| WeaponClass MVP = one_hand | 擋 two_hand／dual_wield／fists |
| 背鑰永在背 | 不可進主／副手；E／B／D 皆可見於動作幀 |
| chest_heart ↔ WindStaminaGlow | JSON `bindsHud`＋View 錨點 |

## 模組

- `paper_doll_frames.gd` — Anim／Slot → 單幀路徑
- `paper_doll_config.gd` — 讀 JSON
- `paper_doll_assembler.gd` — 規則＋`frame_path_for_current()`
- `paper_doll_view.gd` — 顯示
- `test_paper_doll_v2.gd` — headless
