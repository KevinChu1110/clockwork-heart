extends SceneTree
## 第一季節奏與等級上限 Lv30 實機截圖腳本 (t_1a1e5f32)
## 遵循規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 角色分頁在 zh_TW、en 各一張，Lv 數字清楚（Lv.30 · 本季上限 / Season Cap）
## 2. 零系統 Emoji，色盤鮮亮果凍質感
## 3. OUT_DIR 嚴格限定為 proofs/t_1a1e5f32/，不覆蓋其它卡片

const OUT_DIR := "proofs/t_1a1e5f32"
const CROPS_DIR := "proofs/t_1a1e5f32/crops"

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _wait := 0
var _lobby: MobileLobby = null
var _loc_node: Node = null
var _gs: Node = null


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

	if _gs:
		_gs.call("reset_new_game")
		_gs.set("player_race", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c1")
		_gs.set("gold", 8888)
		_gs.set("level", 30)
		_gs.set("energy", 15)

	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("── 開始執行第一季節奏 Lv30 實機截圖腳本 (t_1a1e5f32) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 確保切到角色分頁 (Tab.CHARACTER = 1)
			if _wait == 2:
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_lobby.refresh_hud()
			elif _wait >= 25:
				_save_full_and_crops("proof_char_tab_zh_TW.png", "zh_TW")
				print("  ✓ [1/2] 角色分頁全景 [zh_TW] 實機截圖完成: proof_char_tab_zh_TW.png")
				# 切換至 en 語系
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_lobby._apply_locale_texts()
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_lobby.refresh_hud()
				_step = 2
				_wait = 0
		2:
			if _wait == 2:
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_lobby.refresh_hud()
			elif _wait >= 25:
				_save_full_and_crops("proof_char_tab_en.png", "en")
				print("  ✓ [2/2] 角色分頁全景 [en] 實機截圖完成: proof_char_tab_en.png")
				_step = 3
				_wait = 0
		3:
			print("\nCAPTURE_PACING_S1_PROOFS_OK")
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

	# 角色分頁標題與屬性等級標籤特寫 crop: x in [480..1180], y in [180..320]
	var rect_lv := Rect2i(480, 180, 700, 140)
	var crop_lv := img.get_region(rect_lv)
	if crop_lv and not crop_lv.is_empty():
		crop_lv.save_png(crops_dir.path_join("crop_char_lv_%s.png" % code))
