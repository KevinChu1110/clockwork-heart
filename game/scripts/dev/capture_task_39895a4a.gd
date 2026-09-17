extends SceneTree
## 側案·程式 阿宏 - 八族本職武器與獨有發條鑰匙 512 實機截圖 (t_39895a4a)
## 實機三張（md5 不可重複）：
## 1. proof_lion_lance_idle_512.png (獅持長槍待機)
## 2. proof_boar_hammer_idle_512.png (豬持巨錘待機)
## 3. proof_fox_staff_idle_512.png (狐持法杖待機)

var _out_dir: String = ""
var _step := 0
var _wait := 0
var _gs: Node = null
var _host: Control = null
var _battle: Control = null

func _initialize() -> void:
	print("=== 開始產生八族本職武器 512 實機截圖 (t_39895a4a) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "lion")
		_gs.set("player_name", "獅騎士")
		_gs.set("chapter", "c0")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# ── 步驟 1：獅持長槍戰鬥待機 ──
			if _wait == 1:
				print(">>> [步驟 1/3] 獅持長槍戰鬥待機 (wpn_knight_lance + key_classic_brass)...")
				if _gs:
					_gs.set("player_race", "lion")
					_gs.set("player_name", "獅騎士")
					_gs.set("paperdoll_slots", {
						"race": "lion",
						"chassis": "paint_brass_gold",
						"costume": "costume_nutcracker_guard",
						"weapon": "wpn_knight_lance",
						"winding_key": "key_classic_brass"
					})
				SpriteDB.clear_equipped_cache()
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "wolf")
			if _wait >= 45:
				_save_full_and_crop(
					"proof_lion_lance_idle_512.png",
					"proof_lion_lance_weapon_crop.png",
					Rect2i(210, 250, 100, 220)
				)
				if _battle:
					_battle.queue_free()
					_battle = null
				_step = 1
				_wait = 0
			return false

		1:
			# ── 步驟 2：豬持巨錘探索待機 ──
			if _wait == 5:
				print(">>> [步驟 2/3] 豬持巨錘探索待機 (wpn_anvil_greathammer + key_classic_brass)...")
				if _gs:
					_gs.set("player_race", "boar")
					_gs.set("player_name", "野豬戰士")
					_gs.set("paperdoll_slots", {
						"race": "boar",
						"chassis": "paint_molten_crimson",
						"costume": "costume_viking_harness",
						"weapon": "wpn_anvil_greathammer",
						"winding_key": "key_classic_brass"
					})
				SpriteDB.clear_equipped_cache()
				var Host = load("res://scripts/world/explore_host.gd")
				_host = Host.new()
				root.add_child(_host)
				_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				_host.setup("village")
			if _wait >= 45:
				_save_full_and_crop(
					"proof_boar_hammer_idle_512.png",
					"proof_boar_hammer_weapon_crop.png",
					Rect2i(570, 310, 80, 120)
				)
				if _host:
					_host.queue_free()
					_host = null
				_step = 2
				_wait = 0
			return false

		2:
			# ── 步驟 3：狐持法杖戰鬥待機 ──
			if _wait == 5:
				print(">>> [步驟 3/3] 狐持法杖戰鬥待機 (wpn_astral_staff + key_classic_brass)...")
				if _gs:
					_gs.set("player_race", "fox")
					_gs.set("player_name", "靈狐")
					_gs.set("paperdoll_slots", {
						"race": "fox",
						"chassis": "paint_fox_orange",
						"costume": "costume_astral_cape",
						"weapon": "wpn_astral_staff",
						"winding_key": "key_classic_brass"
					})
				SpriteDB.clear_equipped_cache()
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "falcon")
			if _wait >= 45:
				_save_full_and_crop(
					"proof_fox_staff_idle_512.png",
					"proof_fox_staff_weapon_crop.png",
					Rect2i(300, 210, 140, 160)
				)
				if _battle:
					_battle.queue_free()
					_battle = null
				print("=== 三張實機截圖擷取完成 ===")
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
	print("  ✓ 儲存實機全景截圖: %s (1280x720)" % full_p)

	if not crop_name.is_empty():
		var crop_img := img.get_region(crop_rect)
		var crop_p := _out_dir.path_join(crop_name)
		crop_img.save_png(crop_p)
		print("  ✓ 儲存特寫裁切截圖: %s (%dx%d)" % [crop_p, crop_rect.size.x, crop_rect.size.y])
