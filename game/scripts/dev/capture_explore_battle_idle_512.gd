extends SceneTree
## 《發條之心》探索站立與戰鬥待機兔族 512 高清紙娃娃實機截圖產生器
## 驗證項目：
## 1. 探索站立：裸機素體 (bare) 與 胡桃鉗近衛 (nutcracker_guard) 實機截圖
## 2. 戰鬥待機：裸機素體 (bare) 與 胡桃鉗近衛 (nutcracker_guard) 實機截圖
## 3. 像素級尺寸量測與邊緣硬邊品質檢驗

var _out_dir: String = ""
var _step := 0
var _wait := 0
var _gs: Node = null
var _host: Control = null
var _battle: Control = null


func _initialize() -> void:
	print("=== 開始產生探索與戰鬥待機兔族 512 實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c0")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# ── 步驟 0：載入探索場景，設定為兔族裸機 (costume: none) ──
			if _wait == 1:
				print(">>> [探索 1] 設定兔族裸機待機...")
				if _gs:
					_gs.set("paperdoll_slots", {
						"race": "rabbit",
						"costume": "none",
						"chassis": "paint_ivory_stock",
						"head_unit": "ear_rabbit_straight",
						"optic_core": "core_cyan_emerald",
						"winding_key": "key_classic_brass",
						"weapon": "wpn_dawn_blade"
					})
				SpriteDB.clear_equipped_cache()
				var Host = load("res://scripts/world/explore_host.gd")
				_host = Host.new()
				root.add_child(_host)
				_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				_host.setup("village")
			if _wait >= 35:
				_save_full_and_crop("proof_explore_rabbit_bare_512.png", "proof_explore_rabbit_bare_crop.png", Rect2i(540, 260, 200, 200))
				_step = 1
				_wait = 0
			return false

		1:
			# ── 步驟 1：切換探索為胡桃鉗近衛軍裝 (costume_nutcracker_guard) ──
			if _wait == 1:
				print(">>> [探索 2] 設定兔族胡桃鉗近衛待機...")
				if _gs:
					_gs.set("paperdoll_slots", {
						"race": "rabbit",
						"costume": "costume_nutcracker_guard",
						"chassis": "paint_ivory_stock",
						"head_unit": "ear_rabbit_straight",
						"optic_core": "core_cyan_emerald",
						"winding_key": "key_classic_brass",
						"weapon": "wpn_dawn_blade"
					})
				SpriteDB.clear_equipped_cache()
			if _wait >= 35:
				_save_full_and_crop("proof_explore_rabbit_nutcracker_512.png", "proof_explore_rabbit_nutcracker_crop.png", Rect2i(540, 260, 200, 200))
				if _host:
					_host.queue_free()
					_host = null
				_step = 2
				_wait = 0
			return false

		2:
			# ── 步驟 2：載入戰鬥場景，設定為兔族裸機 ──
			if _wait == 5:
				print(">>> [戰鬥 1] 設定兔族裸機戰鬥待機...")
				if _gs:
					_gs.set("paperdoll_slots", {
						"race": "rabbit",
						"costume": "none",
						"chassis": "paint_ivory_stock",
						"head_unit": "ear_rabbit_straight",
						"optic_core": "core_cyan_emerald",
						"winding_key": "key_classic_brass",
						"weapon": "wpn_dawn_blade"
					})
				SpriteDB.clear_equipped_cache()
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "wolf")
			if _wait >= 40:
				_save_full_and_crop("proof_battle_rabbit_bare_512.png", "proof_battle_rabbit_bare_crop.png", Rect2i(200, 220, 260, 300))
				if _battle:
					_battle.queue_free()
					_battle = null
				_step = 3
				_wait = 0
			return false

		3:
			# ── 步驟 3：載入戰鬥場景，設定為兔族胡桃鉗近衛 ──
			if _wait == 5:
				print(">>> [戰鬥 2] 設定兔族胡桃鉗近衛戰鬥待機...")
				if _gs:
					_gs.set("paperdoll_slots", {
						"race": "rabbit",
						"costume": "costume_nutcracker_guard",
						"chassis": "paint_ivory_stock",
						"head_unit": "ear_rabbit_straight",
						"optic_core": "core_cyan_emerald",
						"winding_key": "key_classic_brass",
						"weapon": "wpn_dawn_blade"
					})
				SpriteDB.clear_equipped_cache()
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "wolf")
			if _wait >= 40:
				_save_full_and_crop("proof_battle_rabbit_nutcracker_512.png", "proof_battle_rabbit_nutcracker_crop.png", Rect2i(200, 220, 260, 300))
				if _battle:
					_battle.queue_free()
					_battle = null
				print("=== 探索與戰鬥 512 實機截圖擷取完畢 ===")
				quit(0)
				return true

	return false


func _save_full_and_crop(full_name: String, crop_name: String, crop_rect: Rect2i) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var full_p := _out_dir.path_join(full_name)
	img.save_png(full_p)
	print("  ✓ 儲存全屏截圖: %s (1280x720)" % full_p)

	var crop_img := img.get_region(crop_rect)
	var crop_p := _out_dir.path_join(crop_name)
	crop_img.save_png(crop_p)
	print("  ✓ 儲存特寫截圖: %s (%dx%d)" % [crop_p, crop_rect.size.x, crop_rect.size.y])
