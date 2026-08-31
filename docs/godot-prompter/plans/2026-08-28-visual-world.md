# 探索世界視覺重規劃（GodotPrompter）· 已選 C

> 日期：2026-08-28（改選 C）  
> 技能：`godot-brainstorming` → `player-controller` · `physics-system` · `ai-navigation` · `2d-essentials` · `scene-organization` · `camera-system` · `assets-pipeline` · `godot-testing` · `godot-code-review`  
> 對齊：[docs/ART_2D.md](../../ART_2D.md)（終點本來就是 TileMap + CharacterBody2D）

## 一句話

**C 比較完整。** 地圖、碰撞、尋路、腳踩地、Y 排序都變成引擎節點，不再用「一張 Gemini 油畫 + JSON 多邊形」猜世界。代價是重寫探索層；所以**先翠谷村一條可玩路徑，再擴全圖**，主線不會整段鎖死。

舊方案 A（一直重產底圖）不採用。B（場景當權威、Control 殼留下）是半套：腳仍用自製格子。C 把玩家也換成 `CharacterBody2D`。

---

## 為什麼 C 才叫完整

| 問題 | A/B | C |
|------|-----|---|
| NPC 漂在屋頂 | 靠 walkmask 人工對 | `CollisionShape2D` / tile 物理，腳在碰撞上 |
| 圖有天空 | 測亮度、再產圖 | 天空若不在 TileMap／Decor 裡，就站不到 |
| 點擊尋路 | 自製 `AStarGrid2D` | `NavigationAgent2D` + 烘焙好的 `NavigationPolygon` |
| 誰擋誰 | Control `z_index` 手排 | `y_sort_enabled` 用腳底 Y |
| 編輯器預覽 | 有限 | 開 `.tscn` 就是關卡 |
| 手機點擊移動 | 已有 | 保留：點一下設 `target_position` |

`main.gd` 的互動 id（`maisui`、`exit_east`…）**不變**。換的是世界怎麼站、怎麼走。

---

## 場景樹（一張圖 = 一個 Level）

依 `scene-organization` 的 Level 模式 + `ai-navigation` 的 World 結構：

```
VillageMap (Node2D)                         # 關卡根；無玩法 if
├── Ground (Sprite2D, optional)             # 氛圍底；Nearest；不是碰撞
├── Tiles (TileMapLayer)                    # 地磚；Physics layer = world
├── Walls (TileMapLayer)                    # 實心視覺／碰撞（可與 Tiles 同一 TileSet）
├── Navigation (NavigationRegion2D)
│   └── NavigationPolygon                   # 編輯器烘焙；執行期可 bake(true)
├── Markers (Node2D)
│   ├── Spawn (Marker2D)
│   └── Maisui (Marker2D)                   # 節點名 = catalog 互動 id
├── Decor (Node2D, y_sort_enabled)
│   └── HutA (StaticBody2D)
│       ├── Sprite2D
│       └── CollisionShape2D                # 腳過不去的建築
├── Actors (Node2D, y_sort_enabled)
│   ├── Player (CharacterBody2D instance)
│   └── NpcMaisui (CharacterBody2D or Static + Area2D)
└── Camera2D                                # 跟隨玩家；limit 對齊地圖
```

### 玩家場景（可重用）

```
Player (CharacterBody2D)                    # motion_mode = MOTION_MODE_FLOATING（俯視無重力）
├── Visuals
│   ├── Shadow (Sprite2D)
│   ├── Body (Sprite2D)                     # 紙娃娃底
│   ├── Armor / Weapon / Accessory
│   └── AnimationPlayer 或 現有 pose 切換
├── CollisionShape2D                        # 只包腳底，別包整隻兔子
├── NavigationAgent2D                       # 點擊移動的路
└── InteractArea (Area2D)
    └── CollisionShape2D                    # 靠近自動互動（沿用現有 INTERACT_DIST）
```

移動迴圈只放 `_physics_process`：讀 `NavigationAgent2D.get_next_path_position()` → 設 `velocity` → `move_and_slide()`。點擊：螢幕座標 → 世界座標 → `nav_agent.target_position = ...`。點 NPC：目標設成對方旁邊一格，到了發 `interacted(id)`。

### 信號

| 信號 | 發出 | 接到 | 用途 |
|------|------|------|------|
| `interacted(id)` | Player / ExploreHost | `main.gd` | 與現在一樣 |
| `hint_changed(text)` | ExploreHost | HUD | 靠近提示 |
| `navigation_finished` | NavigationAgent2D | Player | 停步、觸發互動 |
| `body_entered` | InteractArea | Player | 進入互動距離 |

---

## 切換策略（避免一次改爆）

1. **新世界與舊 Control 並存。** `ExploreHost`（新 Node2D 關卡）先只服務 `village`。其他圖仍走現有 `ExploreView`。  
2. **feature 旗標** `explore.native`（或 map_id 白名單）。主線可隨時退回舊殼。  
3. **測試雙軌。** 舊 `test_tap_move.gd` 在舊圖上繼續綠；新 `test_explore_native.gd` 測村：bake 得到路、走到 Marker、發出 `interacted`。  
4. 村穩了再 `town`，再主線圖。未遷移的圖不刪舊 plate。

---

## 實作任務

每項實作前載入標註的技能。

- [x] **C0 契約** — `docs/godot-prompter/specs/explore-native-contract.md`：Marker 名 = 互動 id、`Spawn` 必有、NavigationPolygon 必烘焙、玩家 `MOTION_MODE_FLOATING`、腳底 shape。  
      Skills: `godot-brainstorming`, `scene-organization`

- [x] **C1 匯入** — 像素 Lossless + Nearest；`Snap 2D Transforms to Pixel`。  
      Skills: `assets-pipeline`, `2d-essentials`

- [x] **C2 Player.tscn** — CharacterBody2D + 腳底碰撞 + NavigationAgent2D；點擊設目標；現有紙娃娃貼圖先複用。  
      Skills: `player-controller`, `input-handling`, `ai-navigation`

- [x] **C3 村關卡** — `village.tscn` 補齊 Tiles／Navigation／Markers／Decor。從現有 walkmask 匯出 polygon 當第一版，再在編輯器修。  
      Skills: `2d-essentials`, `ai-navigation`

- [x] **C4 ExploreHost** — 新腳本掛關卡、Camera2D follow、把 `interacted` 接到 `main.gd`。白名單 `village` 走新殼。  
      Skills: `camera-system`, `gdscript-patterns`

- [x] **C5 測試** — `test_explore_native.gd`：bake、尋路、走到 Spawn 外的 Marker、`interacted` 哨兵。舊 tap-move 仍綠。  
      Skills: `godot-testing`

- [x] **C6 騎士堡** — `town.tscn` + 四舖 `town_forge／town_soul／town_gem／town_tutor.tscn`，白名單已含。  
      2026-08-31 重排廣場：29 個實體照建築歸位（左屋鐵匠鋪／中央石屋武術館／右上掛旗木屋聚魂殿／右大屋手藝工坊／東北小徑出城），
      腳點全在 walkmask、彼此 ≥100px；出口一律掛名稱牌（黃箭頭拿掉後沒牌就找不到門）；禮拜堂／馬廄／兵營歸 hut 類只留熱區。
      實機截圖：`godot --path game --script res://scripts/dev/verify_native.gd --resolution 1280x720` → `screenshots/verify_native_*.png`。  
      Skills: `scene-organization`

- [ ] **C7 主線其餘圖** — 按章遷移；catalog 座標改為「無場景時的後備」。  
      Skills: `2d-essentials`

- [ ] **C8 去 AI 味** — 地磚／切片進 Decor；整張 plate 最多當 Ground；色盤量化沿用 `pixelize_env`。  
      Skills: `assets-pipeline`

- [ ] **C9 審查** — `godot-code-review`：移動在 `_physics_process`、沒有 get_parent 鍊、Y 排序、filter Nearest。  
      Skills: `godot-code-review`

---

## 完成定義（村先過，再擴）

村：

1. 開 `village.tscn` 看得到地磚／路、Spawn、麥穗 Marker、已烘焙 Navigation。  
2. 執行期點地面，兔子用 `move_and_slide` 沿導航走，不會穿牆。  
3. 點麥穗會走到旁邊並 `interacted("maisui")`。  
4. `test_explore_native.gd` 印 `EXPLORE_NATIVE_OK`；舊測試套件仍綠。  
5. `godot --path game --headless --quit-after 3` 無 SCRIPT ERROR。

全圖：主線每張圖都有場景，catalog 不再是座標權威。

---

## 踩過的坑（2026-08-31）

- **macOS 開機崩潰**：`project.godot` `window/size/mode=3`（開機全螢幕）＋玩家偏好「視窗」→ DisplaySettings 在第一幀切回視窗，
  AppKit 全螢幕過渡失敗把視窗寬度歸零 → `MTLTextureDescriptor has width of zero` abort。無頭測試不碰 Metal 所以全綠。
  解法：開機 `mode=0`，全螢幕由 DisplaySettings 依偏好套（兩條路徑都驗過）。
- **Godot 編輯器會重寫 `project.godot`**：`[autoload]` 裡的 `##` 中文註解被序列化成亂碼 key，GameFont 變成無名 autoload。
  註解一律用 `;`。
- **騎士堡底圖換 3200×1800 後**，HEAD 的舊座標不能還原；重排用 `tools/check_walkmask.py --grid town` 的格線圖對 UV。

## 風險

- Navigation 沒烘焙 → 人站著不動。村場景進版控前必須 bake。  
- `agent_radius` 太大 → 過不了門。腳底 shape 對齊兔子腳，不要包整身。  
- 第一幀設目標會空路徑 → `await` map ready 或延後一幀。  
- 舊存檔章節／座標仍用 Control 空間；遷移時用 Marker 對齊，不要假設像素 1:1 還能用舊 x,y。
