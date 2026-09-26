extends SceneTree
## 《發條之心》探索性 QA 第三十六輪 實機截圖腳本 (qa_round36)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗證重點：
## 1. 大廳村莊全景在 zh_TW、en、ja、ko 下，左側四殿堂卡標題與副標題清晰可見、無截字、無破圖、無 Emoji。
## 2. 大廳背景、頂欄、右側出征卡與底部 Dock 連動同步切換語系 (0-QA25)。
## 3. 實機截圖輸出目錄嚴格限定為 proofs/qa_round36/ (0-QA23)。
## 4. 局部 Crops 供顯微比對標題、副標、Dock、TopBar 排版。
## 5. 舊功能入口回歸：天宮鐵匠、手藝工坊、冒險委託、冒險出征入口正常運作。

const OUT_DIR := "proofs/qa_round36"
const CROPS_DIR := "proofs/qa_round36/crops"

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _wait := 0
var _lobby: MobileLobby = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES := ["zh_TW", "en", "ja", "ko"]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var abs_out := base.path_join("../" + OUT_DIR)
	var abs_crops := base.path_join("../" + CROPS_DIR)
	DirAccess.make_dir_recursive_absolute(abs_out)
	DirAccess.make_dir_recursive_absolute(abs_crops)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行探索性 QA 第三十六輪實機截圖腳本 (qa_round36) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3, 4:
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", code)

				if _gs:
					_gs.call("reset_new_game")
					_gs.set("player_race", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("chapter", "c0")
					_gs.set("gold", 1000)
					_gs.set("level", 10)
					_gs.set("energy", 15)

				_lobby = MobileLobby.new()
				root.add_child(_lobby)
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.select_hall_card(-1)
			elif _wait >= 30:
				var filename := "proof_0%d_lobby_village_%s.png" % [_step, code]
				_save_full_and_crops(filename, code)
				print("  ✓ [%d/8] 大廳村莊全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0

		5:
			# 回歸測試 1：天宮鐵匠入口（open_forge）
			if _wait == 1:
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")

				if _gs:
					_gs.call("reset_new_game")
					_gs.set("player_race", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("chapter", "c0")
					_gs.set("gold", 1000)
					_gs.set("level", 10)
					_gs.set("energy", 15)

				_lobby = MobileLobby.new()
				root.add_child(_lobby)
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.open_forge()
			elif _wait >= 30:
				var filename := "proof_05_regression_forge_dialog.png"
				_save_full(filename)
				print("  ✓ [5/8] 天宮鐵匠回歸實機截圖完成: %s" % filename)
				_step += 1
				_wait = 0

		6:
			# 回歸測試 2：手藝工坊入口（open_gem_workshop）
			if _wait == 1:
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")

				if _gs:
					_gs.call("reset_new_game")
					_gs.set("player_race", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("chapter", "c0")
					_gs.set("gold", 1000)
					_gs.set("level", 10)
					_gs.set("energy", 15)

				_lobby = MobileLobby.new()
				root.add_child(_lobby)
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.open_gem_workshop()
			elif _wait >= 30:
				var filename := "proof_06_regression_gem_workshop_dialog.png"
				_save_full(filename)
				print("  ✓ [6/8] 手藝工坊回歸實機截圖完成: %s" % filename)
				_step += 1
				_wait = 0

		7:
			# 回歸測試 3：冒險委託入口（open_windup_daily）
			if _wait == 1:
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")

				if _gs:
					_gs.call("reset_new_game")
					_gs.set("player_race", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("chapter", "c0")
					_gs.set("gold", 1000)
					_gs.set("level", 10)
					_gs.set("energy", 15)

				_lobby = MobileLobby.new()
				root.add_child(_lobby)
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.open_windup_daily()
			elif _wait >= 30:
				var filename := "proof_07_regression_windup_quest_dialog.png"
				_save_full(filename)
				print("  ✓ [7/8] 冒險委託回歸實機截圖完成: %s" % filename)
				_step += 1
				_wait = 0

		8:
			# 回歸測試 4：冒險出征入口（go_to_sortie）
			if _wait == 1:
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")

				if _gs:
					_gs.call("reset_new_game")
					_gs.set("player_race", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("chapter", "c0")
					_gs.set("gold", 1000)
					_gs.set("level", 10)
					_gs.set("energy", 15)

				_lobby = MobileLobby.new()
				root.add_child(_lobby)
				_lobby.go_to_sortie()
			elif _wait >= 30:
				var filename := "proof_08_regression_sortie_adventure_tab.png"
				_save_full(filename)
				print("  ✓ [8/8] 冒險出征回歸實機截圖完成: %s" % filename)
				_step += 1
				_wait = 0

		9:
			if _lobby != null and is_instance_valid(_lobby):
				_lobby.queue_free()
				_lobby = null
			print("\nCAPTURE_QA_ROUND36_OK")
			quit(0)
			return true

	return false


func _save_full(filename: String) -> void:
	var base := ProjectSettings.globalize_path("res://")
	var full_dir := base.path_join("../" + OUT_DIR)

	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法截取畫面: %s" % filename)
		return

	var full_path := full_dir.path_join(filename)
	var err := img.save_png(full_path)
	if err != OK:
		push_error("儲存截圖失敗: %s" % full_path)


func _save_full_and_crops(filename: String, code: String) -> void:
	var base := ProjectSettings.globalize_path("res://")
	var full_dir := base.path_join("../" + OUT_DIR)
	var crops_dir := base.path_join("../" + CROPS_DIR)

	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法截取畫面: %s" % filename)
		return

	var full_path := full_dir.path_join(filename)
	var err := img.save_png(full_path)
	if err != OK:
		push_error("儲存截圖失敗: %s" % full_path)
		return

	# 1. 左側四殿堂卡特寫 crop: x in [30..270], y in [100..390]
	var rect_cards := Rect2i(30, 100, 240, 290)
	var crop_cards := img.get_region(rect_cards)
	if crop_cards and not crop_cards.is_empty():
		crop_cards.save_png(crops_dir.path_join("crop_hall_cards_%s.png" % code))

	# 2. 底部 Dock 導航特寫 crop: x in [20..1260], y in [625..715]
	var rect_dock := Rect2i(20, 625, 1240, 90)
	var crop_dock := img.get_region(rect_dock)
	if crop_dock and not crop_dock.is_empty():
		crop_dock.save_png(crops_dir.path_join("crop_dock_%s.png" % code))

	# 3. 頂部 HUD 狀態列特寫 crop: x in [10..1270], y in [5..80]
	var rect_topbar := Rect2i(10, 5, 1260, 75)
	var crop_topbar := img.get_region(rect_topbar)
	if crop_topbar and not crop_topbar.is_empty():
		crop_topbar.save_png(crops_dir.path_join("crop_topbar_%s.png" % code))
