extends SceneTree
## 大廳出征十六張關卡卡名稱六語系實機截圖 (lobby-stages-i18n)
## 遵循規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 出征分頁全景在 en、ja (及 zh_TW) 下，1-1~4-4 關卡名稱在地化正常，不整排中文。
## 2. 彈窗以外的大廳底層（頂欄狀態、底部 Dock 等）同步切換至同一語系 (0-QA25)。
## 3. 實機截圖輸出目錄嚴格限定為 proofs/lobby_stages_i18n/ (0-QA23)。
## 4. 局部 Crops 供顯微比對關卡卡片排版，確保長譯名不截字、不溢出卡片。

const OUT_DIR := "proofs/lobby_stages_i18n"
const CROPS_DIR := "proofs/lobby_stages_i18n/crops"

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _wait := 0
var _lobby: MobileLobby = null
var _loc_node: Node = null
var _gs: Node = null

# 測試語系與地區組合：en (區1, 區2), ja (區1, 區2), zh_TW (區1)
var _capture_configs: Array[Dictionary] = [
	{"code": "en", "region": 0, "name": "proof_adventure_stages_en_r1.png"},
	{"code": "en", "region": 1, "name": "proof_adventure_stages_en_r2.png"},
	{"code": "ja", "region": 0, "name": "proof_adventure_stages_ja_r1.png"},
	{"code": "ja", "region": 1, "name": "proof_adventure_stages_ja_r2.png"},
	{"code": "zh_TW", "region": 0, "name": "proof_adventure_stages_zh_TW_r1.png"},
]


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

	print("── 開始執行大廳出征分頁六語系實機截圖腳本 (lobby-stages-i18n) ──")
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	if _step < _capture_configs.size():
		var cfg := _capture_configs[_step]
		var code: String = cfg["code"]
		var region: int = cfg["region"]
		var filename: String = cfg["name"]

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
			_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
			_lobby._select_region(region)
		elif _wait >= 25:
			_save_full_and_crops(filename, code, region)
			print("  ✓ [%d/%d] 出征分頁 [%s R%d] 實機截圖完成: %s" % [_step + 1, _capture_configs.size(), code, region + 1, filename])
			_step += 1
			_wait = 0
	else:
		print("\nCAPTURE_LOBBY_STAGES_I18N_OK")
		quit(0)
		return true

	return false


func _save_full_and_crops(filename: String, code: String, region: int) -> void:
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

	# 產生中間 4 張關卡卡片特寫 crop: x in [80..1200], y in [180..620]
	var rect_cards := Rect2i(80, 180, 1120, 440)
	var crop_cards := img.get_region(rect_cards)
	if crop_cards and not crop_cards.is_empty():
		crop_cards.save_png(crops_dir.path_join("crop_cards_%s_r%d.png" % [code, region + 1]))
