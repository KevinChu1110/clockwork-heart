extends SceneTree
## 實機截圖產生器：四區出征關卡名與敵人名玩具世界化轉譯六語系存證 (capture_campaign_stages_i18n.gd)
## 依據規範：review.md 0-QA5, 0-QA26, 0-QA23, 0-QA24, 0-QA25, CANON.md

var _out_dir: String = ""
var _crops_dir: String = ""
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

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_9ade3069")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

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

	print("── 開始執行四區主線出征與戰鬥抬頭實機截圖腳本 (t_9ade3069) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0

func _save_viewport(filename: String, crop_rect: Rect2i = Rect2i(), crop_filename: String = "") -> void:
	var img := root.get_texture().get_image()
	if img == null:
		print("  [ERROR] 無法取得 viewport 影像: ", filename)
		return
	var full_path := _out_dir.path_join(filename)
	img.save_png(full_path)
	print("  ✓ 已儲存全景截圖: ", filename)

	if crop_rect.size.x > 0 and crop_rect.size.y > 0 and not crop_filename.is_empty():
		var crop_img := img.get_region(crop_rect)
		var crop_path := _out_dir.path_join(crop_filename)
		crop_img.save_png(crop_path)
		print("  ✓ 已儲存裁切特寫: ", crop_filename)

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
				_lobby.call("_switch_tab", 1) # ADVENTURE
				_lobby.call("_select_region", 0)
			elif _wait == 4:
				_save_viewport(
					"proof_01_stages_region1_zh_TW.png",
					Rect2i(60, 180, 560, 240),
					"crops/crop_01_stage_1_1_card.png"
				)
				_step = 1
				_wait = 0

		1:
			# 切換至 EN 語系，檢查第一地區出征卡片
			if _wait == 1:
				_loc.call("set_locale", "en")
			elif _wait == 4:
				_save_viewport("proof_02_stages_region1_en.png")
				_step = 2
				_wait = 0

		2:
			# 切回繁中，選擇第二地區（白霧外緣、市集街道、排水管道·黑鏽機關偶、聖獅內殿·守衛泰坦雷歐）
			if _wait == 1:
				_loc.call("set_locale", "zh_TW")
				_lobby.call("_select_region", 1)
			elif _wait == 4:
				_save_viewport(
					"proof_03_stages_region2_zh_TW.png",
					Rect2i(60, 340, 560, 240),
					"crops/crop_02_stage_2_3_card.png"
				)
				_step = 3
				_wait = 0

		3:
			# 選擇第三地區（西林外緣·霧影機關偶、霧崖小徑·旋風發條偶、鏡廊入口·鐘擺守衛、白霧核心·守衛泰坦白狐）
			if _wait == 1:
				_lobby.call("_select_region", 2)
			elif _wait == 4:
				_save_viewport(
					"proof_04_stages_region3_zh_TW.png",
					Rect2i(60, 180, 560, 240),
					"crops/crop_03_stage_3_1_card.png"
				)
				_step = 4
				_wait = 0

		4:
			# 選擇第四地區（石岸潮線·破浪哨衛、潮岸沉船·舵輪機關衛、疤地焰徑·熔火發條偶、通天塔底·終境停擺核）
			if _wait == 1:
				_lobby.call("_select_region", 3)
			elif _wait == 4:
				_save_viewport(
					"proof_05_stages_region4_zh_TW.png",
					Rect2i(640, 340, 560, 240),
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
				_save_viewport("proof_10_battle_1_1_en.png")
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_gs.set("current_expedition_stage", "")
				_loc.call("set_locale", "zh_TW")
				print("── 截圖生成完畢 ──")
				quit(0)
				return true

	return false
