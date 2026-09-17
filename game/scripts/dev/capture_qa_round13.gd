extends SceneTree
## 側案·測試 小婷 - 探索性 QA 第十三輪實機截圖產生器 (t_eb607930)
## 覆蓋對象：
## 1. 大廳立牌 512 (兔、狐、獅)
## 2. 創角種族列與舞台 512 (兔、狐、企鵝)
## 3. 衣櫥格子＋中央預覽 512 (兔、狐、企鵝)
## 4. 探索站立 512 (兔、獅)
## 5. 探索走動 512 (狐、獅)
## 6. 戰鬥待機 512 (企鵝、獅)
## 總計 15 張全景實機 (1280x720) + 15 張角色區 crop

var _out_dirs: Array[String] = []
var _step: int = 0
var _wait: int = 0
var _current_node: Node = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始執行 QA Round 13 實機截圖 (t_eb607930) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round13")
	_out_dirs.append(repo_proofs)

	var ws_proofs := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_eb607930/proofs/qa_round13"
	_out_dirs.append(ws_proofs)

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	_gs = root.get_node_or_null("GameState")
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 01: 兔族大廳全景 (大廳立牌 512 + HUD + Dock)
			if _wait == 1:
				print(">>> [1/15] 建立兔族大廳...")
				_setup_player("rabbit", "小白", {
					"race": "rabbit",
					"costume": "none",
					"chassis": "paint_ivory_stock"
				})
				var MobileLobby = load("res://scripts/ui/mobile_lobby.gd")
				var lobby = MobileLobby.new()
				_current_node = lobby
				root.add_child(lobby)
				lobby.call("_switch_tab", 0) # VILLAGE
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_01_lobby_rabbit.png",
					"proof_01_lobby_rabbit_crop.png",
					Rect2i(460, 180, 360, 400)
				)
				_clean_node()
				_step = 1
				_wait = 0
			return false

		1:
			# 02: 狐族大廳全景 (狐族大廳立牌 512 + HUD + Dock)
			if _wait == 1:
				print(">>> [2/15] 建立狐族大廳...")
				_setup_player("fox", "靈狐", {
					"race": "fox",
					"costume": "none",
					"chassis": "paint_fox_orange"
				})
				var MobileLobby = load("res://scripts/ui/mobile_lobby.gd")
				var lobby = MobileLobby.new()
				_current_node = lobby
				root.add_child(lobby)
				lobby.call("_switch_tab", 0)
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_02_lobby_fox.png",
					"proof_02_lobby_fox_crop.png",
					Rect2i(460, 180, 360, 400)
				)
				_clean_node()
				_step = 2
				_wait = 0
			return false

		2:
			# 03: 獅族大廳全景 (獅族大廳立牌 512 + HUD + Dock)
			if _wait == 1:
				print(">>> [3/15] 建立獅族大廳...")
				_setup_player("lion", "雷恩", {
					"race": "lion",
					"costume": "none",
					"chassis": "paint_brass_gold"
				})
				var MobileLobby = load("res://scripts/ui/mobile_lobby.gd")
				var lobby = MobileLobby.new()
				_current_node = lobby
				root.add_child(lobby)
				lobby.call("_switch_tab", 0)
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_03_lobby_lion.png",
					"proof_03_lobby_lion_crop.png",
					Rect2i(460, 180, 360, 400)
				)
				_clean_node()
				_step = 3
				_wait = 0
			return false

		3:
			# 04: 創角畫面 - 兔族 (種族列 + 512 舞台)
			if _wait == 1:
				print(">>> [4/15] 建立創角介面 (兔族)...")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "rabbit")
					_current_node = demo
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_04_creation_rabbit.png",
					"proof_04_creation_rabbit_crop.png",
					Rect2i(180, 140, 400, 440)
				)
				_clean_node()
				_step = 4
				_wait = 0
			return false

		4:
			# 05: 創角畫面 - 狐族 (種族列 + 512 舞台)
			if _wait == 1:
				print(">>> [5/15] 建立創角介面 (狐族)...")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "fox")
					_current_node = demo
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_05_creation_fox.png",
					"proof_05_creation_fox_crop.png",
					Rect2i(180, 140, 400, 440)
				)
				_clean_node()
				_step = 5
				_wait = 0
			return false

		5:
			# 06: 創角畫面 - 企鵝族 (種族列 + 512 舞台)
			if _wait == 1:
				print(">>> [6/15] 建立創角介面 (企鵝族)...")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "penguin")
					_current_node = demo
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_06_creation_penguin.png",
					"proof_06_creation_penguin_crop.png",
					Rect2i(180, 140, 400, 440)
				)
				_clean_node()
				_step = 6
				_wait = 0
			return false

		6:
			# 07: 衣櫥 - 兔族穿著 nutcracker_guard (中央 512 預覽 + 格子)
			if _wait == 1:
				print(">>> [7/15] 建立兔族衣櫥...")
				_setup_player("rabbit", "小白", {
					"race": "rabbit",
					"costume": "costume_nutcracker_guard",
					"chassis": "paint_ivory_stock",
					"costume_id": "costume_nutcracker_guard",
					"paint_id": "paint_ivory_stock"
				})
				var WardrobeDialog = load("res://scripts/ui/wardrobe_dialog.gd")
				var wd = WardrobeDialog.new()
				wd.creation_mode = false
				wd.current_race = "rabbit"
				wd.selected_costume_id = "costume_nutcracker_guard"
				wd.selected_chassis_id = "paint_ivory_stock"
				root.add_child(wd)
				wd.call("_update_card_selection_states")
				wd.call("_update_preview")
				wd.call("_update_ui_texts")
				_current_node = wd
			elif _wait >= 35:
				_save_full_and_crop(
					"proof_07_wardrobe_rabbit_costume.png",
					"proof_07_wardrobe_rabbit_costume_crop.png",
					Rect2i(295, 230, 100, 160)
				)
				_clean_node()
				_step = 7
				_wait = 0
			return false

		7:
			# 08: 衣櫥 - 狐族穿著 costume_astral_cape (中央 512 預覽 + 格子)
			if _wait == 1:
				print(">>> [8/15] 建立狐族衣櫥...")
				_setup_player("fox", "靈狐", {
					"race": "fox",
					"costume": "costume_astral_cape",
					"chassis": "paint_fox_orange",
					"costume_id": "costume_astral_cape",
					"paint_id": "paint_fox_orange"
				})
				var WardrobeDialog = load("res://scripts/ui/wardrobe_dialog.gd")
				var wd = WardrobeDialog.new()
				wd.creation_mode = false
				wd.current_race = "fox"
				wd.selected_costume_id = "costume_astral_cape"
				wd.selected_chassis_id = "paint_fox_orange"
				root.add_child(wd)
				wd.call("_update_card_selection_states")
				wd.call("_update_preview")
				wd.call("_update_ui_texts")
				_current_node = wd
			elif _wait >= 35:
				_save_full_and_crop(
					"proof_08_wardrobe_fox_costume.png",
					"proof_08_wardrobe_fox_costume_crop.png",
					Rect2i(340, 230, 120, 190)
				)
				_clean_node()
				_step = 8
				_wait = 0
			return false

		8:
			# 09: 衣櫥 - 企鵝族 (中央 512 預覽 + 格子)
			if _wait == 1:
				print(">>> [9/15] 建立企鵝族衣櫥...")
				_setup_player("penguin", "企鵝波波", {
					"race": "penguin",
					"costume": "none",
					"chassis": "paint_penguin_navy",
					"costume_id": "none",
					"paint_id": "paint_penguin_navy"
				})
				var WardrobeDialog = load("res://scripts/ui/wardrobe_dialog.gd")
				var wd = WardrobeDialog.new()
				wd.creation_mode = false
				wd.current_race = "penguin"
				wd.selected_costume_id = "none"
				wd.selected_chassis_id = "paint_penguin_navy"
				root.add_child(wd)
				wd.call("_update_card_selection_states")
				wd.call("_update_preview")
				wd.call("_update_ui_texts")
				_current_node = wd
			elif _wait >= 35:
				_save_full_and_crop(
					"proof_09_wardrobe_penguin_costume.png",
					"proof_09_wardrobe_penguin_costume_crop.png",
					Rect2i(340, 230, 120, 190)
				)
				_clean_node()
				_step = 9
				_wait = 0
			return false

		9:
			# 10: 探索站著 - 兔族 (穿著 nutcracker_guard 512)
			if _wait == 1:
				print(">>> [10/15] 建立兔族探索站立...")
				_setup_player("rabbit", "小白", {
					"race": "rabbit",
					"costume": "costume_nutcracker_guard",
					"chassis": "paint_ivory_stock",
					"costume_id": "costume_nutcracker_guard",
					"paint_id": "paint_ivory_stock"
				})
				var Host = load("res://scripts/world/explore_host.gd")
				var host = Host.new()
				_current_node = host
				root.add_child(host)
				host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				host.setup("village")
			elif _wait >= 35:
				var pl: CanvasItem = _current_node.call("get_player") if _current_node else null
				var crop_pos := Vector2i(540, 260)
				if pl:
					var screen_pos: Vector2 = pl.get_global_transform_with_canvas().origin
					crop_pos = Vector2i(int(screen_pos.x - 100), int(screen_pos.y - 120))
					crop_pos.x = clampi(crop_pos.x, 0, 1280 - 220)
					crop_pos.y = clampi(crop_pos.y, 0, 720 - 220)
				_save_full_and_crop(
					"proof_10_explore_rabbit_idle.png",
					"proof_10_explore_rabbit_idle_crop.png",
					Rect2i(crop_pos.x, crop_pos.y, 220, 220)
				)
				_clean_node()
				_step = 10
				_wait = 0
			return false

		10:
			# 11: 探索站著 - 獅族 (穿著 costume_nutcracker_guard 512)
			if _wait == 1:
				print(">>> [11/15] 建立獅族探索站立...")
				_setup_player("lion", "雷恩", {
					"race": "lion",
					"costume": "costume_nutcracker_guard",
					"chassis": "paint_brass_gold",
					"costume_id": "costume_nutcracker_guard",
					"paint_id": "paint_brass_gold"
				})
				var Host = load("res://scripts/world/explore_host.gd")
				var host = Host.new()
				_current_node = host
				root.add_child(host)
				host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				host.setup("village")
			elif _wait >= 35:
				var pl: CanvasItem = _current_node.call("get_player") if _current_node else null
				var crop_pos := Vector2i(540, 260)
				if pl:
					var screen_pos: Vector2 = pl.get_global_transform_with_canvas().origin
					crop_pos = Vector2i(int(screen_pos.x - 100), int(screen_pos.y - 120))
					crop_pos.x = clampi(crop_pos.x, 0, 1280 - 220)
					crop_pos.y = clampi(crop_pos.y, 0, 720 - 220)
				_save_full_and_crop(
					"proof_11_explore_lion_idle.png",
					"proof_11_explore_lion_idle_crop.png",
					Rect2i(crop_pos.x, crop_pos.y, 220, 220)
				)
				_clean_node()
				_step = 11
				_wait = 0
			return false

		11:
			# 12: 探索走動 - 狐族 (穿著 costume_astral_cape 走動 512 合成)
			if _wait == 1:
				print(">>> [12/15] 建立狐族探索走動...")
				_setup_player("fox", "靈狐", {
					"race": "fox",
					"costume": "costume_astral_cape",
					"chassis": "paint_fox_orange",
					"costume_id": "costume_astral_cape",
					"paint_id": "paint_fox_orange"
				})
				var Host = load("res://scripts/world/explore_host.gd")
				var host = Host.new()
				_current_node = host
				root.add_child(host)
				host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				host.setup("village")
			elif _wait == 15:
				var pl: Node = _current_node.call("get_player") if _current_node else null
				if pl and pl.has_method("go_to"):
					pl.call("go_to", pl.get("global_position") + Vector2(240, 0))
					print("  已觸發狐族走動...")
			elif _wait >= 40:
				var pl: CanvasItem = _current_node.call("get_player") if _current_node else null
				var crop_pos := Vector2i(540, 260)
				if pl:
					var screen_pos: Vector2 = pl.get_global_transform_with_canvas().origin
					crop_pos = Vector2i(int(screen_pos.x - 100), int(screen_pos.y - 120))
					crop_pos.x = clampi(crop_pos.x, 0, 1280 - 220)
					crop_pos.y = clampi(crop_pos.y, 0, 720 - 220)
				_save_full_and_crop(
					"proof_12_explore_fox_walk.png",
					"proof_12_explore_fox_walk_crop.png",
					Rect2i(crop_pos.x, crop_pos.y, 220, 220)
				)
				_clean_node()
				_step = 12
				_wait = 0
			return false

		12:
			# 13: 探索走動 - 獅族 (穿著 costume_nutcracker_guard 走動 512 合成)
			if _wait == 1:
				print(">>> [13/15] 建立獅族探索走動...")
				_setup_player("lion", "雷恩", {
					"race": "lion",
					"costume": "costume_nutcracker_guard",
					"chassis": "paint_brass_gold",
					"costume_id": "costume_nutcracker_guard",
					"paint_id": "paint_brass_gold"
				})
				var Host = load("res://scripts/world/explore_host.gd")
				var host = Host.new()
				_current_node = host
				root.add_child(host)
				host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				host.setup("village")
			elif _wait == 15:
				var pl: Node = _current_node.call("get_player") if _current_node else null
				if pl and pl.has_method("go_to"):
					pl.call("go_to", pl.get("global_position") + Vector2(240, 0))
					print("  已觸發獅族走動...")
			elif _wait >= 40:
				var pl: CanvasItem = _current_node.call("get_player") if _current_node else null
				var crop_pos := Vector2i(540, 260)
				if pl:
					var screen_pos: Vector2 = pl.get_global_transform_with_canvas().origin
					crop_pos = Vector2i(int(screen_pos.x - 100), int(screen_pos.y - 120))
					crop_pos.x = clampi(crop_pos.x, 0, 1280 - 220)
					crop_pos.y = clampi(crop_pos.y, 0, 720 - 220)
				_save_full_and_crop(
					"proof_13_explore_lion_walk.png",
					"proof_13_explore_lion_walk_crop.png",
					Rect2i(crop_pos.x, crop_pos.y, 220, 220)
				)
				_clean_node()
				_step = 13
				_wait = 0
			return false

		13:
			# 14: 戰鬥待機 - 企鵝族 (512 待機姿態)
			if _wait == 1:
				print(">>> [14/15] 建立企鵝族戰鬥待機...")
				_setup_player("penguin", "企鵝波波", {
					"race": "penguin",
					"costume": "none",
					"chassis": "paint_penguin_navy",
					"costume_id": "none",
					"paint_id": "paint_penguin_navy"
				})
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				var battle = b_scn.instantiate()
				_current_node = battle
				root.add_child(battle)
				if battle.has_method("setup"):
					battle.call("setup", "wolf")
			elif _wait >= 35:
				_save_full_and_crop(
					"proof_14_battle_penguin_idle.png",
					"proof_14_battle_penguin_idle_crop.png",
					Rect2i(180, 220, 300, 300)
				)
				_clean_node()
				_step = 14
				_wait = 0
			return false

		14:
			# 15: 戰鬥待機 - 獅族 (512 待機姿態)
			if _wait == 1:
				print(">>> [15/15] 建立獅族戰鬥待機...")
				_setup_player("lion", "雷恩", {
					"race": "lion",
					"costume": "costume_nutcracker_guard",
					"chassis": "paint_brass_gold",
					"costume_id": "costume_nutcracker_guard",
					"paint_id": "paint_brass_gold"
				})
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				var battle = b_scn.instantiate()
				_current_node = battle
				root.add_child(battle)
				if battle.has_method("setup"):
					battle.call("setup", "wolf")
			elif _wait >= 35:
				_save_full_and_crop(
					"proof_15_battle_lion_idle.png",
					"proof_15_battle_lion_idle_crop.png",
					Rect2i(180, 220, 300, 300)
				)
				_clean_node()
				print("=== 15 張實機截圖擷取完成！ ===")
				quit(0)
				return true

	return false

func _setup_player(race: String, pname: String, slots: Dictionary) -> void:
	if _gs:
		_gs.call("reset_new_game", race)
		_gs.set("player_race", race)
		_gs.set("player_name", pname)
		_gs.set("chapter", "c0")
		_gs.set("paperdoll_slots", slots)
	SpriteDB.clear_equipped_cache()

func _clean_node() -> void:
	if _current_node != null:
		_current_node.queue_free()
		_current_node = null

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

	var crop_img := img.get_region(crop_rect) if not crop_name.is_empty() else null

	for out_d in _out_dirs:
		var full_p := out_d.path_join(full_name)
		img.save_png(full_p)
		if crop_img != null:
			var crop_p := out_d.path_join(crop_name)
			crop_img.save_png(crop_p)
	print("  ✓ 截圖與裁切存檔完成: %s" % full_name)
