# Art Pivot v2 — 紙娃娃系統分解（開發用）

目標：裝備可換、動作依武器類型分表，方便之後做動畫／組裝，不混在單一檔。

身份鎖（不動）：米白殼、青綠胸口心、黃銅**背鑰**、手機貼紙賽璐璐；禁電影 3D／藍 mana 條／頭上螺旋槳。

MVP 先實裝：**單手劍**全套動作；雙手／遠程先留 Slot＋動作名，資產可占位。

---

## 1. 裝備槽 Equipment Slots（由下到上 draw order）

| z | SlotId | 中文 | 說明 | MVP |
|---|--------|------|------|-----|
| 0 | `body_base` | 身體底 | 膚／殼色、四肢錨點 | ✅ |
| 1 | `outfit` | 套服 | 整套衣服／盔甲外觀（可蓋身） | ✅ 基礎米白殼當預設 outfit |
| 2 | `helmet` | 頭盔 | 頭／耳飾上層（可藏耳或露耳） | ✅ 預設空＝露金屬立耳 |
| 3 | `face` | 臉 | 眼／頰／嘴（表情可換） | ✅ |
| 4 | `chest_heart` | 胸口心 | 青綠心，HUD 錨點，通常不被 outfit 全蓋 | ✅ 必掛 |
| 5 | `back_key` | 背鑰 | 黃銅發條鑰，**永遠在背** | ✅ 必掛 |
| 6 | `weapon_main` | 主手武器 | 單手／雙手／遠程依 WeaponClass 切 | ✅ 單手劍 |
| 7 | `weapon_off` | 副手 | 僅單手類需要時（盾／空） | ⬜ 可空 |
| 8 | `vfx` | 特效層 | 糖果屑、受擊閃 | ✅ part_break |

**規則**
- `helmet` 與 `ears`：若頭盔 `hideEars=true` 則不畫立耳；否則 ears 併入 `body_base` 或獨立子層 `ears`（建議 `body_base` 內建耳，頭盔可選 hide）。
- 換裝只換對應 Slot 圖層，不重繪整隻角色。
- 背鑰、胸口心為**身份層**，換裝不可刪掉（可換 skin／外框）。

---

## 2. 武器類型 WeaponClass

| WeaponClass | 說明 | 使用槽 | MVP |
|-------------|------|--------|-----|
| `one_hand` | 單手武器（劍等） | `weapon_main`＋可選 `weapon_off` | ✅ |
| `two_hand` | 雙手武器 | 只 `weapon_main`（佔雙腕） | ⬜ 占位 |
| `ranged` | 遠程（弓／槍等） | `weapon_main` | ⬜ 占位 |

---

## 3. 動作表 AnimSet（依武器類型拆開）

每個 `WeaponClass` 各有一套 AnimClip；**不要**把單手／雙手／遠程混成同一條動畫檔。

### 3.1 共用（全 WeaponClass 都要）

| AnimId | 中文 | 說明 |
|--------|------|------|
| `idle` | 待機 | 呼吸／微動 |
| `ready` | 準備 | 進戰架勢、高亮 B 相 |
| `hit` | 受擊 | 短後仰＋可選糖果屑 |

### 3.2 單手 `one_hand`（MVP 必做）

| AnimId | 中文 | 說明 |
|--------|------|------|
| `one_hand_atk_1` | 單手攻擊1 | 第一段（揮擊） |
| `one_hand_atk_2` | 單手攻擊2 | 第二段 |
| `one_hand_atk_3` | 單手攻擊3 | 第三段／收招 |
| `one_hand_idle` | （可＝idle） | 單手持武待機；可共用 `idle`＋握持偏移 |
| `one_hand_ready` | （可＝ready） | 單手準備 |

### 3.3 雙手 `two_hand`（先留名）

| AnimId | 中文 |
|--------|------|
| `two_hand_atk_1` | 雙手攻擊1 |
| `two_hand_atk_2` | 雙手攻擊2 |
| `two_hand_atk_3` | 雙手攻擊3 |

＋共用 `idle`／`ready`／`hit`（雙手握持偏移不同檔）

### 3.4 遠程 `ranged`（先留名）

| AnimId | 中文 |
|--------|------|
| `ranged_atk_1` | 遠程攻擊1 |
| `ranged_atk_2` | 遠程攻擊2 |
| `ranged_atk_3` | 遠程攻擊3 |

＋共用 `idle`／`ready`／`hit`

### 3.5 非戰鬥相（與武器無關，可共用）

| AnimId | 中文 | 對 §8 |
|--------|------|-------|
| `explore_walk` | 探索走 | E03 |
| `dismantle_pull` | 拆零件拉 | D02（手部；背鑰仍在） |

---

## 4. 檔案／組裝建議（給 Frank）

```
res://art/paper_doll/
  layers/
    body_base/
    outfit/
    helmet/
    face/
    chest_heart/
    back_key/
    weapon_main/
      one_hand/
      two_hand/
      ranged/
    weapon_off/
    vfx/
  anim/
    shared/          # idle, ready, hit, explore_walk, dismantle_pull
    one_hand/        # atk_1, atk_2, atk_3
    two_hand/
    ranged/
```

組裝偽邏輯：
1. 讀 `EquipmentLoadout`（各 SlotId → asset_id）
2. 讀 `WeaponClass` → 選對應 AnimSet
3. 播 clip 時只置換該 WeaponClass 資料夾內的圖幀／骨骼偏移
4. `chest_heart` 位置輸出給 HUD（Ken 的胸口光錨點）

---

## 5. JSON 草案（給 Ken 定 SlotId／AnimId）

```json
{
  "id": "paper_doll_v2",
  "slots": [
    "body_base", "outfit", "helmet", "face",
    "chest_heart", "back_key", "weapon_main", "weapon_off", "vfx"
  ],
  "weaponClasses": ["one_hand", "two_hand", "ranged"],
  "anim": {
    "shared": ["idle", "ready", "hit", "explore_walk", "dismantle_pull"],
    "one_hand": ["atk_1", "atk_2", "atk_3"],
    "two_hand": ["atk_1", "atk_2", "atk_3"],
    "ranged": ["atk_1", "atk_2", "atk_3"]
  },
  "mvp": {
    "weaponClass": "one_hand",
    "requiredLayers": ["body_base", "chest_heart", "back_key", "weapon_main"],
    "optionalLayers": ["outfit", "helmet", "face", "weapon_off", "vfx"]
  }
}
```

---

## 6. 現有資產對照

| 檔 | 用途 |
|----|------|
| `v2/xiaobai_e03.png` | explore 參考（無武器） |
| `v2/xiaobai_b02.png` | one_hand ready／atk 參考 |
| `v2/xiaobai_d02.png` | dismantle_pull 參考 |
| `v2/style_pivot_xiaobai_v1.png` | 風格＋層示意 |

下一刀美術：出 `one_hand` 的 idle／ready／hit／atk_1–3 六格條；頭盔／套服各 1 套示例。
