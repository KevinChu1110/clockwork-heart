extends SceneTree
## 側案·程式 阿宏 - 非兔族換裝待機 512 合成實機驗證截圖 (t_800cf77e)
## 產出四張實機截圖（md5 不可重複）：
## 1. proof_explore_fox_equipped_512.png (狐族探索換裝待機)
## 2. proof_battle_lion_equipped_512.png (獅族戰鬥待機)
## 3. proof_wardrobe_center_preview_512.png (衣櫥中央預覽)
## 4. proof_wardrobe_grid_closeup_512.png (衣櫥格子特寫)

var _out_dir: String = ""
var _step := 0
var _wait := 0
var _gs: Node = null
var _host: Control = null
var _battle: Control = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始產生非兔族 512 換裝待機實機截圖 (t_800cf77e) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "fox")
		_gs.set("player_name", "靈狐")
		_gs.set("chapter", "c0")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# ── 步驟 0：狐族探索換裝待機 (costume_astral_cape 512 合成) ──
			if _wait == 1:
				print(">>> [步驟 1/4] 設定狐族探索換裝待機 (costume_astral_cape)...")
				if _gs:
					_gs.set("player_race", "fox")
					_gs.set("paperdoll_slots", {
						"race": "fox",
						"costume": "costume_astral_cape",
						"chassis": "paint_fox_orange",
						"costume_id": "costume_astral_cape",
						"paint_id": "paint_fox_orange"
					})
				SpriteDB.clear_equipped_cache()
				var Host = load("res://scripts/world/explore_host.gd")
				_host = Host.new()
				root.add_child(_host)
				_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				_host.setup("village")
			if _wait >= 40:
				_save_full_and_crop(
					"proof_explore_fox_equipped_512.png",
					"proof_explore_fox_equipped_crop.png",
					Rect2i(540, 260, 200, 200)
				)
				if _host:
					_host.queue_free()
					_host = null
				_step = 1
				_wait = 0
			return false

		1:
			# ── 步驟 1：獅族戰鬥待機 (costume_nutcracker_guard 512 合成) ──
			if _wait == 5:
				print(">>> [步驟 2/4] 設定獅族戰鬥待機 (costume_nutcracker_guard)...")
				if _gs:
					_gs.set("player_race", "lion")
					_gs.set("paperdoll_slots", {
						"race": "lion",
						"costume": "costume_nutcracker_guard",
						"chassis": "paint_brass_gold",
						"costume_id": "costume_nutcracker_guard",
						"paint_id": "paint_brass_gold"
					})
				SpriteDB.clear_equipped_cache()
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "wolf")
			if _wait >= 45:
				_save_full_and_crop(
					"proof_battle_lion_equipped_512.png",
					"proof_battle_lion_equipped_crop.png",
					Rect2i(200, 220, 260, 300)
				)
				if _battle:
					_battle.queue_free()
					_battle = null
				_step = 2
				_wait = 0
			return false

		2:
			# ── 步驟 2：衣櫥中央預覽與衣櫥格子特寫 (狐族換裝預覽) ──
			if _wait == 5:
				print(">>> [步驟 3/4 & 4/4] 開啟衣櫥 (WardrobeDialog) 進行預覽與格子擷取...")
				if _gs:
					_gs.set("player_race", "fox")
					_gs.set("paperdoll_slots", {
						"race": "fox",
						"costume": "costume_viking_harness",
						"chassis": "paint_fox_orange",
						"costume_id": "costume_viking_harness",
						"paint_id": "paint_fox_orange"
					})
				SpriteDB.clear_equipped_cache()
				var WardrobeDialog = load("res://scripts/ui/wardrobe_dialog.gd")
				_wardrobe = WardrobeDialog.new()
				_wardrobe.creation_mode = false
				_wardrobe.current_race = "fox"
				root.add_child(_wardrobe)
				_wardrobe.selected_costume_id = "costume_viking_harness"
				_wardrobe.selected_chassis_id = "paint_fox_orange"
				_wardrobe.call("_update_card_selection_states")
				_wardrobe.call("_update_preview")
				_wardrobe.call("_update_ui_texts")
			if _wait >= 45:
				# 3. 衣櫥全屏／中央預覽
				_save_full_and_crop(
					"proof_wardrobe_center_preview_512.png",
					"proof_wardrobe_preview_crop.png",
					Rect2i(340, 230, 120, 190)
				)
				# 4. 衣櫥格子特寫 (右側卡片網格區域特寫)
				_save_crop_only(
					"proof_wardrobe_grid_closeup_512.png",
					Rect2i(550, 175, 420, 380)
				)
				if _wardrobe:
					_wardrobe.queue_free()
					_wardrobe = null
				print("=== 4 張實機截圖擷取完成 ===")
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

func _save_crop_only(crop_name: String, crop_rect: Rect2i) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var crop_img := img.get_region(crop_rect)
	var crop_p := _out_dir.path_join(crop_name)
	crop_img.save_png(crop_p)
	print("  ✓ 儲存特寫截圖: %s (%dx%d)" % [crop_p, crop_rect.size.x, crop_rect.size.y])
