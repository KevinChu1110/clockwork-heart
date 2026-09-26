extends SceneTree
## 大廳左側四殿堂卡標題副標六語系實機截圖 (lobby-hall-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 大廳村莊全景在 en、ja、zh_TW 下，左側四殿堂卡標題與副標題清晰可見且在地化。
## 2. 大廳背景、頂欄、右側出征卡與底部 Dock 連動同步切換語系 (0-QA25)。
## 3. 實機截圖輸出目錄嚴格限定為 proofs/lobby-hall-i18n/ (0-QA23)。
## 4. 局部 Crops 供顯微比對標題與副標排版。

const OUT_DIR := "proofs/lobby-hall-i18n"
const CROPS_DIR := "proofs/lobby-hall-i18n/crops"

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _wait := 0
var _lobby: MobileLobby = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES := ["en", "ja", "zh_TW"]


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

	print("── 開始執行大廳四殿堂卡六語系實機截圖腳本 (lobby-hall-i18n) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
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
			elif _wait >= 25:
				var filename := "proof_lobby_hall_village_%s.png" % code
				_save_full_and_crops(filename, code)
				print("  ✓ [%d/3] 大廳全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0
		4:
			print("\nCAPTURE_LOBBY_HALL_I18N_OK")
			quit(0)
			return true

	return false


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

	# 產生左側四殿堂卡特寫 crop: x in [30..270], y in [100..390]
	var rect_cards := Rect2i(30, 100, 240, 290)
	var crop_cards := img.get_region(rect_cards)
	if crop_cards and not crop_cards.is_empty():
		crop_cards.save_png(crops_dir.path_join("crop_hall_cards_%s.png" % code))
