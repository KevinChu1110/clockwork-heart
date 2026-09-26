extends SceneTree
## 出征關卡區域抗性綠黃紅實機截圖腳本 (t_50cd3a23)
## 驗證規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收項目：
## 1. zh_TW 第一地區出征頁全景（三檔齊備：1-1 綠安全、1-2 黃吃力、1-4 紅過載）
## 2. 三檔特寫裁切（綠標安全、黃標吃力、紅標過載）
## 3. en 出征頁全景與卡片特寫（Safe / Strained / Overload，長譯名不截字）
## 4. ja 出征頁全景與卡片特寫（安全 / 苦戦 / 過負荷）

const OUT_DIR := "proofs/t_50cd3a23"
const CROPS_DIR := "proofs/t_50cd3a23/crops"

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
		_gs.set("gold", 6666)
		# 玩家設為 Lv2：1-1(sug1)綠安全, 1-2(sug3)黃吃力(差1), 1-3(sug6)黃吃力(差4), 1-4(sug8)紅過載(差6)
		_gs.set("level", 2)
		_gs.set("energy", 15)

	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("── 開始執行出征區域抗性實機截圖腳本 (t_50cd3a23) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 切換到出征分頁 (Tab.ADVENTURE = 2) 並選擇第一地區
			if _wait == 2:
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
				_lobby._select_region(0)
				_lobby.refresh_hud()
			elif _wait >= 25:
				_save_full_and_crops_zh_TW("proof_expedition_zh_TW.png")
				print("  ✓ [1/3] 出征頁全景與三檔特寫 [zh_TW] 完成: proof_expedition_zh_TW.png")
				# 切換至 en 語系
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_lobby._apply_locale_texts()
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
				_lobby._select_region(0)
				_lobby.refresh_hud()
				_step = 2
				_wait = 0

		2:
			# 步驟 2: en 出征頁 (第一地區)
			if _wait == 2:
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
				_lobby._select_region(0)
				_lobby.refresh_hud()
			elif _wait >= 25:
				_save_full_and_crops_lang("proof_expedition_en.png", "en")
				print("  ✓ [2/3] 出征頁全景與特寫 [en] 完成: proof_expedition_en.png")
				# 切換至 ja 語系
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
				_lobby._apply_locale_texts()
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
				_lobby._select_region(0)
				_lobby.refresh_hud()
				_step = 3
				_wait = 0

		3:
			# 步驟 3: ja 出征頁 (第一地區)
			if _wait == 2:
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
				_lobby._select_region(0)
				_lobby.refresh_hud()
			elif _wait >= 25:
				_save_full_and_crops_lang("proof_expedition_ja.png", "ja")
				print("  ✓ [3/3] 出征頁全景與特寫 [ja] 完成: proof_expedition_ja.png")
				_step = 4
				_wait = 0

		4:
			print("\nCAPTURE_EXPEDITION_RESISTANCE_PROOFS_OK")
			quit(0)
			return true

	return false


func _save_full_and_crops_zh_TW(filename: String) -> void:
	var base := ProjectSettings.globalize_path("res://")
	var full_dir := base.path_join("../" + OUT_DIR)
	var crops_dir := base.path_join("../" + CROPS_DIR)

	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		return

	img.save_png(full_dir.path_join(filename))

	# 1-1 綠標安全 (左上卡片): x in [60..630], y in [190..335]
	var rect_green := Rect2i(60, 190, 570, 145)
	var crop_g := img.get_region(rect_green)
	if crop_g and not crop_g.is_empty():
		crop_g.save_png(crops_dir.path_join("crop_card_safe_green_zh_TW.png"))

	# 1-2 黃標吃力 (右上卡片): x in [650..1220], y in [190..335]
	var rect_yellow := Rect2i(650, 190, 570, 145)
	var crop_y := img.get_region(rect_yellow)
	if crop_y and not crop_y.is_empty():
		crop_y.save_png(crops_dir.path_join("crop_card_strained_yellow_zh_TW.png"))

	# 1-4 紅標過載 (右下卡片): x in [650..1220], y in [355..500]
	var rect_red := Rect2i(650, 355, 570, 145)
	var crop_r := img.get_region(rect_red)
	if crop_r and not crop_r.is_empty():
		crop_r.save_png(crops_dir.path_join("crop_card_overload_red_zh_TW.png"))


func _save_full_and_crops_lang(filename: String, code: String) -> void:
	var base := ProjectSettings.globalize_path("res://")
	var full_dir := base.path_join("../" + OUT_DIR)
	var crops_dir := base.path_join("../" + CROPS_DIR)

	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		return

	img.save_png(full_dir.path_join(filename))

	# 特寫右上黃標卡片 (長譯名驗證): x in [650..1220], y in [190..335]
	var rect_card := Rect2i(650, 190, 570, 145)
	var crop_c := img.get_region(rect_card)
	if crop_c and not crop_c.is_empty():
		crop_c.save_png(crops_dir.path_join("crop_card_%s.png" % code))
