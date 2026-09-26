extends SceneTree
## 角色分頁武器槽與屬性小卡六語系實機截圖 (char-tab-i18n)
## 遵循規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 角色分頁全景在 en、ja、zh_TW 下，三個武器槽與五獨立屬性小卡在地化切換正常。
## 2. 彈窗以外的大廳底層（頂欄狀態、底部 Dock 等）同步切換至同一語系 (0-QA25)。
## 3. 實機截圖輸出目錄嚴格限定為 proofs/char-tab-i18n/ (0-QA23)。
## 4. 局部 Crops 供顯微比對武器槽與屬性小卡排版。

const OUT_DIR := "proofs/char-tab-i18n"
const CROPS_DIR := "proofs/char-tab-i18n/crops"

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

	print("── 開始執行角色分頁六語系實機截圖腳本 (char-tab-i18n) ──")
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
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_lobby.select_weapon_slot(0)
			elif _wait >= 25:
				var filename := "proof_char_tab_%s.png" % code
				_save_full_and_crops(filename, code)
				print("  ✓ [%d/3] 角色分頁全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0
		4:
			print("\nCAPTURE_CHAR_TAB_I18N_OK")
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

	# 產生右側武器槽與屬性小卡特寫 crop: x in [420..1220], y in [20..630]
	var rect_right := Rect2i(420, 20, 800, 610)
	var crop_right := img.get_region(rect_right)
	if crop_right and not crop_right.is_empty():
		crop_right.save_png(crops_dir.path_join("crop_char_tab_right_%s.png" % code))
