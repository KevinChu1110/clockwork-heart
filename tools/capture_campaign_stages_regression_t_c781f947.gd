extends SceneTree
## 全面回歸驗收實機截圖腳本 (t_c781f947)
## 驗收內容：四區主線出征關卡名與敵方稱號玩具世界化轉譯合併至 main 主線後之全站回歸驗收
## 規範遵守：review.md 0-QA5, 0-QA26, 0-QA23, CANON.md

const OUT_DIRS := [
	"/opt/side/bravesoul-game/proofs/t_c781f947",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c781f947/proofs"
]

var _step := 0
var _wait := 0

var _lobby: Control = null
var _battle: Control = null
var _loc: Node = null
var _gs: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for d in OUT_DIRS:
		DirAccess.make_dir_recursive_absolute(d)
		DirAccess.make_dir_recursive_absolute(d.path_join("crops"))

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GSClass = load("res://scripts/autoload/game_state.gd")
		if GSClass:
			_gs = GSClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("energy", 15)

	print("── 開始執行四區主線出征全站回歸實機截圖 (t_c781f947) ──")
	_step = 0
	_wait = 0

func _save_viewport(filename: String, crop_rect: Rect2i = Rect2i(), crop_filename: String = "") -> void:
	var img := root.get_texture().get_image()
	if img == null:
		print("  [ERROR] 無法取得 viewport 影像: ", filename)
		return
	if not filename.is_empty():
		for d: String in OUT_DIRS:
			var full_path: String = d.path_join(filename)
			var err := img.save_png(full_path)
			if err == OK:
				print("  ✓ 已儲存全景截圖: ", full_path)
			else:
				push_error("  ✗ 儲存失敗: " + full_path)

	if crop_rect.size.x > 0 and crop_rect.size.y > 0 and not crop_filename.is_empty():
		var crop_img := img.get_region(crop_rect)
		for d: String in OUT_DIRS:
			var crop_path: String = d.path_join(crop_filename)
			var err := crop_img.save_png(crop_path)
			if err == OK:
				print("  ✓ 已儲存裁切特寫: ", crop_path)
			else:
				push_error("  ✗ 裁切儲存失敗: " + crop_path)

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			# 初始化大廳 (zh_TW)，切換至冒險出征分頁，第一地區
			if _wait == 1:
				_loc.call("set_locale", "zh_TW")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
			elif _wait == 2:
				_lobby.call("go_to_sortie")
				_lobby.call("_select_region", 0)
			elif _wait == 6:
				_save_viewport(
					"proof_01_stages_region1_zh_TW.png",
					Rect2i(66, 248, 570, 157),
					"crops/crop_01_stage_1_1_card.png"
				)
				_step = 1
				_wait = 0

		1:
			# 切換至 EN 語系，檢查第一地區出征卡片
			if _wait == 1:
				_loc.call("set_locale", "en")
			elif _wait == 5:
				_save_viewport(
					"proof_02_stages_region1_en.png",
					Rect2i(66, 248, 570, 157),
					"crops/crop_02_stage_1_1_en_card.png"
				)
				_step = 2
				_wait = 0

		2:
			# 切回繁中，選擇第二地區
			if _wait == 1:
				_loc.call("set_locale", "zh_TW")
				_lobby.call("_select_region", 1)
			elif _wait == 5:
				_save_viewport(
					"proof_03_stages_region2_zh_TW.png",
					Rect2i(66, 411, 570, 157),
					"crops/crop_03_stage_2_3_card.png"
				)
				_step = 3
				_wait = 0

		3:
			# 選擇第三地區
			if _wait == 1:
				_lobby.call("_select_region", 2)
			elif _wait == 5:
				_save_viewport(
					"proof_04_stages_region3_zh_TW.png",
					Rect2i(66, 248, 570, 157),
					"crops/crop_04_stage_3_1_card.png"
				)
				_step = 4
				_wait = 0

		4:
			# 選擇第四地區
			if _wait == 1:
				_lobby.call("_select_region", 3)
			elif _wait == 5:
				_save_viewport(
					"proof_05_stages_region4_zh_TW.png",
					Rect2i(644, 411, 570, 157),
					"crops/crop_05_stage_4_4_card.png"
				)
				if _lobby and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 5
				_wait = 0

		5:
			# 進入 1-1 戰鬥實機，截取繁中戰鬥抬頭（停擺發條鼠）
			if _wait == 1:
				_gs.set("current_expedition_stage", "1-1")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "ash_rat")
			elif _wait == 4:
				_save_viewport(
					"proof_06_battle_1_1_zh_TW.png",
					Rect2i(850, 20, 400, 100),
					"crops/crop_06_battle_1_1_header.png"
				)
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 6
				_wait = 0

		6:
			# 進入 1-3 戰鬥實機，截取繁中戰鬥抬頭（發條機關偶 · 零史萊姆/黏怪）
			if _wait == 1:
				_gs.set("current_expedition_stage", "1-3")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "sewer_slime")
			elif _wait == 4:
				_save_viewport(
					"proof_07_battle_1_3_zh_TW.png",
					Rect2i(850, 20, 400, 100),
					"crops/crop_07_battle_1_3_header.png"
				)
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 7
				_wait = 0

		7:
			# 進入 4-1 戰鬥實機，截取繁中戰鬥抬頭（破浪哨衛 · 零海盜）
			if _wait == 1:
				_gs.set("current_expedition_stage", "4-1")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "coast_raider")
			elif _wait == 4:
				_save_viewport(
					"proof_08_battle_4_1_zh_TW.png",
					Rect2i(850, 20, 400, 100),
					"crops/crop_08_battle_4_1_header.png"
				)
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 8
				_wait = 0

		8:
			# 進入 4-4 戰鬥實機，截取繁中戰鬥抬頭（終境停擺核 · 零惡魔）
			if _wait == 1:
				_gs.set("current_expedition_stage", "4-4")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "demon")
			elif _wait == 4:
				_save_viewport(
					"proof_09_battle_4_4_zh_TW.png",
					Rect2i(850, 20, 400, 100),
					"crops/crop_09_battle_4_4_header.png"
				)
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 9
				_wait = 0

		9:
			# 進入 1-1 戰鬥實機 EN 語系，截取英文戰鬥抬頭（Stagnant Clockwork Rat）
			if _wait == 1:
				_gs.set("current_expedition_stage", "1-1")
				_loc.call("set_locale", "en")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "ash_rat")
			elif _wait == 4:
				_save_viewport(
					"proof_10_battle_1_1_en.png",
					Rect2i(850, 20, 400, 100),
					"crops/crop_10_battle_1_1_header.png"
				)
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_gs.set("current_expedition_stage", "")
				_loc.call("set_locale", "zh_TW")
				print("── 截圖生成完畢 ──")
				quit(0)
				return true

	return false
