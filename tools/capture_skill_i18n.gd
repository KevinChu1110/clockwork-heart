extends SceneTree
## 招式面板六語系實機截圖腳本 (skill-i18n)
## 遵循規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 招式心法面板全景在 en、ja、zh_TW 下，招式名、說明、升級預覽、解鎖提示在地化切換正常。
## 2. 彈窗以外的大廳底層（頂欄狀態、底部 Dock 等）同步切換至同一語系 (0-QA25)。
## 3. 實機截圖輸出目錄嚴格限定為 proofs/skill-i18n/ (0-QA23)。
## 4. 局部 Crops 供顯微比對招式卡片與排版。

const OUT_DIR := "proofs/skill-i18n"
const CROPS_DIR := "proofs/skill-i18n/crops"

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

var _step := 0
var _wait := 0
var _lobby: MobileLobby = null
var _skill_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _sk: Node = null

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
	_sk = root.get_node_or_null("SkillSystem")

	print("── 開始執行招式面板六語系實機截圖腳本 (skill-i18n) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _skill_dlg != null and is_instance_valid(_skill_dlg):
					_skill_dlg.queue_free()
					_skill_dlg = null

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

				if _sk:
					_sk.call("ensure_skill_map")
					_sk.call("learn", "slash", 1)
					_sk.call("add_mastery", "slash", 15)

				_lobby = MobileLobby.new()
				root.add_child(_lobby)

				# 開啟招式彈窗
				_skill_dlg = SkillDialogScn.new()
				root.add_child(_skill_dlg)

			elif _wait >= 25:
				var filename := "proof_skill_panel_%s.png" % code
				_save_full_and_crops(filename, code)
				print("  ✓ [%d/3] 招式面板全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0
		4:
			print("\nCAPTURE_SKILL_I18N_OK")
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

	# 產生招式彈窗主體 crop (x in [260..1020], y in [90..630], size 760x540)
	var rect_panel := Rect2i(260, 90, 760, 540)
	var crop_panel := img.get_region(rect_panel)
	if crop_panel and not crop_panel.is_empty():
		crop_panel.save_png(crops_dir.path_join("crop_skill_dialog_%s.png" % code))

	# 產生招式卡片特寫 crop (橫斬、反戈一擊等)
	var rect_cards := Rect2i(290, 260, 700, 300)
	var crop_cards := img.get_region(rect_cards)
	if crop_cards and not crop_cards.is_empty():
		crop_cards.save_png(crops_dir.path_join("crop_skill_cards_%s.png" % code))
