# 探索原生世界契約（C）

互動 id 仍是 `main.gd` 認得的字串。換的是誰擁有座標與碰撞。

## 關卡場景 `scenes/maps/<map_id>.tscn`

| 路徑 | 型別 | 規則 |
|------|------|------|
| `.` | `Node2D` | 可掛 `MapStage`；`map_id` 與檔名一致 |
| `Tiles` | `TileMapLayer` | 地面；有物理圖層 |
| `Navigation` | `NavigationRegion2D` | 必須有已烘焙的 `NavigationPolygon` |
| `Markers/Spawn` | `Marker2D` | 必有；玩家出生 |
| `Markers/<id>` | `Marker2D` | 節點名 = catalog 實體 id（`maisui`、`exit_east`） |
| `Decor` | `Node2D` | `y_sort_enabled = true` |
| `Actors` | `Node2D` | 執行期掛 Player／NPC；`y_sort_enabled = true` |

沒有場景的 map_id：暫時走舊 `ExploreView`。

## 玩家 `scenes/actors/player.tscn`

- 根：`CharacterBody2D`，`motion_mode = MOTION_MODE_FLOATING`（俯視，不要重力）。
- 碰撞只包腳底。
- 子節點 `NavigationAgent2D`：`target_desired_distance` ≈ 互動距離。
- 移動只在 `_physics_process`；點擊只改 `target_position`。

## 測試哨兵

新檔 `game/scripts/world/test_explore_native.gd`：

- 載入 `village.tscn`
- Navigation 有路徑
- 從 Spawn 走到一個 Marker
- 印 `EXPLORE_NATIVE_OK`

舊 `test_tap_move.gd` 在未遷移的圖上維持綠，直到該圖切白名單。
