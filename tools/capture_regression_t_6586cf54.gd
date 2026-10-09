extends SceneTree
## 戰鬥勝利結算三欄武器戰鬥數據統計膠囊實機存證腳本 (t_6586cf54)
## 覆蓋：
## 1. BattleVictoryDialog 資訊區新增 WeaponLoadoutStatsCapsules
## 2. 繁中 (zh_TW)、英文 (en)、日文 (ja) 六語系即時切換連動存證
## 3. 展示「輪替切換」次數膠囊與三欄武器傷害數值、百分比進度條
## 4. 零系統原生 Emoji，符合手遊多巴胺鮮亮高飽和色盤規範

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const CoreSystemClass := preload("res://scripts/systems/core_system.gd")

const OUT_DIR := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6586cf54/proofs/t_6586cf54"

var _step: int = 0
var _wait: int = 0
var _dlg: Control = null
var _loc_node: Node = null
var _bg: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(OUT_DIR.path_join("crops"))

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		cs = CoreSystemClass.new()
		cs.name = "CoreSystem"
		root.add_child(cs)

	print("=== 開始執行戰鬥勝利三欄武器數據統計膠囊實機截圖存證 (t_6586cf54) ===")

	# 建立全螢幕深色模擬戰鬥背景
	_bg = Control.new()
	_bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var cr := ColorRect.new()
	cr.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	cr.color = Color("#181424")
	_bg.add_child(cr)
	root.add_child(_bg)

	var sample_part := {
		"id": "part_boss_test_01",
		"slot": "soul_core",
		"tier": "gold",
		"tier_name": "金",
		"slot_name": "共鳴核心",
		"stats": {"atk": 18, "hp": 240, "crit": 6.5},
		"broken_parts": ["核心反應爐", "動力履帶"],
	}
	var sample_combat_stats := {
		"total_damage": 3450,
		"elapsed_time": 18.2,
		"dps": 189.5,
		"max_hit_damage": 680,
		"total_hit_count": 42,
		"weapon_swap_count": 9,
		"weapon_slot_damages": {0: 1850, 1: 980, 2: 620},
		"weapon_slot_swaps": {0: 4, 1: 3, 2: 2},
		"weapon_bars": [
			{"name": "鐵劍", "index": 0, "quality": "common"},
			{"name": "獵弓", "index": 1, "quality": "uncommon"},
			{"name": "拳套", "index": 2, "quality": "rare"},
		],
	}

	_dlg = BattleVictoryDialogScript.show_dialog(
		root,
		sample_part,
		Callable(),
		150,
		3,
		["核心反應爐", "動力履帶"],
		sample_combat_stats
	)

	_step = 0
	_wait = 10


func _process(_delta: float) -> bool:
	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			# zh_TW 截圖
			_loc_node.set_locale("zh_TW")
			_dlg.call("_refresh_display")
			_wait = 6
			_step = 1
		1:
			_capture_screen_and_crop(
				OUT_DIR.path_join("proof_01_victory_weapon_stats_zh_TW.png"),
				OUT_DIR.path_join("crops/crop_01_stats_zh_TW.png")
			)
			print("  ✓ 完成 zh_TW 繁中實機存證截圖")
			_step = 2
			_wait = 4
		2:
			# en 截圖
			_loc_node.set_locale("en")
			_dlg.call("_refresh_display")
			_wait = 6
			_step = 3
		3:
			_capture_screen_and_crop(
				OUT_DIR.path_join("proof_02_victory_weapon_stats_en.png"),
				OUT_DIR.path_join("crops/crop_02_stats_en.png")
			)
			print("  ✓ 完成 en 英文實機存證截圖")
			_step = 4
			_wait = 4
		4:
			# ja 截圖
			_loc_node.set_locale("ja")
			_dlg.call("_refresh_display")
			_wait = 6
			_step = 5
		5:
			_capture_screen_and_crop(
				OUT_DIR.path_join("proof_03_victory_weapon_stats_ja.png"),
				OUT_DIR.path_join("crops/crop_03_stats_ja.png")
			)
			print("  ✓ 完成 ja 日文實機存證截圖")
			_step = 6
			_wait = 4
		6:
			print("\n=== 全部實機截圖存證完成 ===")
			quit(0)
			return true

	return false


func _capture_screen_and_crop(full_path: String, crop_path: String) -> void:
	var img := root.get_texture().get_image()
	if img == null:
		push_error("無法獲取畫面截圖")
		return
	img.save_png(full_path)

	# 裁切中央彈窗區域或膠囊區域
	# 螢幕 1280x720，彈窗寬 750，置中 X 約 (1280-750)/2 = 265，Y 約 80~640
	# 裁切統計膠囊卡片區域：X: 275, Y: 360, W: 730, H: 170
	var crop_rect := Rect2i(275, 360, 730, 170)
	var crop_img := img.get_region(crop_rect)
	crop_img.save_png(crop_path)
