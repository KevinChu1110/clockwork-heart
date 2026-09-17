extends SceneTree
## 側案·美術總監 小柔 - 熊族與虎族修圖後實機特寫截圖 (t_9d6493fb)
## 捕捉畫面：
## 1. 熊族大廳 (1280x720，有場景有 HUD) + 頭部特寫
## 2. 虎族大廳 (1280x720，有場景有 HUD) + 頭部特寫

var _out_dirs: Array[String] = []
var _step: int = 0
var _wait: int = 0
var _current_node: Node = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始執行 熊族與虎族實機截圖 (t_9d6493fb) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round13")
	_out_dirs.append(repo_proofs)

	var ws_proofs := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9d6493fb/proofs/qa_round13"
	_out_dirs.append(ws_proofs)

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)
		DirAccess.make_dir_recursive_absolute(d.path_join("head_audit"))

	_gs = root.get_node_or_null("GameState")
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 熊族大廳
			if _wait == 1:
				print(">>> [1/2] 建立熊族大廳...")
				_setup_player("bear", "玄軸熊", {
					"race": "bear",
					"costume": "none",
					"chassis": "paint_bear_amber",
					"head_unit": "head_iron_bear_stock"
				})
				var MobileLobby = load("res://scripts/ui/mobile_lobby.gd")
				var lobby = MobileLobby.new()
				_current_node = lobby
				root.add_child(lobby)
				lobby.call("_switch_tab", 0) # VILLAGE
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_bear_lobby_1280x720.png",
					"head_audit/proof_bear_head_closeup.png",
					Rect2i(540, 200, 200, 200)
				)
				_clean_node()
				_step = 1
				_wait = 0
		1:
			# 虎族大廳
			if _wait == 1:
				print(">>> [2/2] 建立虎族大廳...")
				_setup_player("tiger", "餘燼虎", {
					"race": "tiger",
					"costume": "none",
					"chassis": "paint_ember_orange",
					"head_unit": "head_ember_tiger_stock"
				})
				var MobileLobby = load("res://scripts/ui/mobile_lobby.gd")
				var lobby = MobileLobby.new()
				_current_node = lobby
				root.add_child(lobby)
				lobby.call("_switch_tab", 0) # VILLAGE
			elif _wait >= 25:
				_save_full_and_crop(
					"proof_tiger_lobby_1280x720.png",
					"head_audit/proof_tiger_head_closeup.png",
					Rect2i(540, 200, 200, 200)
				)
				_clean_node()
				print("=== 熊族與虎族實機截圖全部完成 ===")
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
	print("  ✓ 截圖與特寫存檔完成: %s, %s" % [full_name, crop_name])
