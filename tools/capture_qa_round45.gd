extends SceneTree
## 探索性 QA 第四十五輪 實機巡檢存證腳本 (tools/capture_qa_round45.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
##
## 驗收重點：
## 1. en／ja 抽魂結果卡（掉落種類與名稱六語系連動，零系統 Emoji）。
## 2. en／zh_TW 裝備面板頂部與捲到底（返回鈕清晰可見，背包品質標籤連動）。
## 3. 切語系時大廳 chrome（頂部狀態列、底部導航 Dock）是否同步連動切換。
## 4. OUT_DIR 嚴格限定為 proofs/qa_round45/ (0-QA23)。
## 5. 實機 1280x720 全景 + 必要特寫 Crops，MD5 全數相異 (0-QA15)。

var _step := 0
var _wait := 0
var _main: Node = null
var _loc: Node = null
var _gs: Node = null
var _eq: Node = null
var _soul_view: Control = null
var _lobby_view: Control = null

var OUT_DIR := ""
var CROPS_DIR := ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/qa_round45")
	OUT_DIR = resolved_dir
	CROPS_DIR = resolved_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	print("=== 開始執行 QA 第四十五輪實機巡檢存證腳本 (qa_round45) ===")
	print("OUT_DIR: ", OUT_DIR)

	change_scene_to_file("res://scenes/main.tscn")

func _save_screenshot(target_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Viewport is null")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Texture is null")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(target_path)
	if err == OK:
		print("  [Saved Full] %s (%dx%d)" % [target_path, img.get_width(), img.get_height()])
	else:
		push_error("save_png failed err=%d: %s" % [err, target_path])

func _save_crop(src_path: String, crop_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img == null or img.is_empty():
		push_error("Failed to load src image for crop: " + src_path)
		return
	var cropped := img.get_region(rect)
	if cropped != null and not cropped.is_empty():
		var err := cropped.save_png(crop_path)
		if err == OK:
			print("  [Saved Crop] %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])
		else:
			push_error("Failed to save crop: " + crop_path)

func _init_player_data() -> void:
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("level", 16)
		_gs.set("gold", 8800)
		_gs.set("energy", 15)
		_gs.set("stardust", 320)
		_gs.call("set_flag", "tut_done", true)
		_gs.call("set_flag", "c1_entered_city", true)

	if _eq:
		var w1 = _eq.call("roll_instance", "rusty_blade", "common")
		_eq.call("equip_weapon_to_loadout", w1.uid, 0)
		var w2 = _eq.call("roll_instance", "meager_edge", "uncommon")
		_eq.call("equip_weapon_to_loadout", w2.uid, 1)
		var a1 = _eq.call("roll_instance", "ash_mail", "common")
		_eq.call("equip", a1.uid)

		var b1 = _eq.call("roll_instance", "knight_saber", "rare")
		_eq.call("add_to_bag", b1)
		var b2 = _eq.call("roll_instance", "dawn_blade", "epic")
		_eq.call("add_to_bag", b2)
		var b3 = _eq.call("roll_instance", "knight_plate", "rare")
		_eq.call("add_to_bag", b3)
		var b4 = _eq.call("roll_instance", "star_pendant", "uncommon")
		_eq.call("add_to_bag", b4)
		var b5 = _eq.call("roll_instance", "scar_amulet", "rare")
		_eq.call("add_to_bag", b5)
		var b6 = _eq.call("roll_instance", "blade_ring", "rare")
		_eq.call("add_to_bag", b6)

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待主場景加載完成
			if _wait < 30:
				return false
			_main = current_scene
			_loc = root.get_node_or_null("Loc")
			_gs = root.get_node_or_null("GameState")
			_eq = root.get_node_or_null("EquipmentSystem")
			_init_player_data()
			print("1. 準備開始測試 抽魂結果卡 六語系連動...")
			_step = 10
			_wait = 0

		# ──────────────────────────────────────────
		# 抽魂結果卡：en (零件 Brass Gear / Part)
		# ──────────────────────────────────────────
		10:
			if _wait == 1:
				_loc.call("set_locale", "en")
			elif _wait == 10:
				var ViewClass = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
				_soul_view = ViewClass.new()
				_soul_view.name = "SoulDrawPlayView"
				_soul_view.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_soul_view)
				var drop := {
					"DropId": "drop_brass_gear",
					"kind": "part",
					"toastKey": "soul.pull_part"
				}
				if _soul_view.card != null:
					_soul_view.card.show_drop(drop)
			elif _wait == 30:
				var path := OUT_DIR + "/proof_01_en_soul_result_card.png"
				_save_screenshot(path)
				_save_crop(path, CROPS_DIR + "/crop_01_en_soul_badge_name.png", Rect2i(340, 360, 600, 180))
				print("  ✓ proof_01_en_soul_result_card 完成")
				_step = 11
				_wait = 0

		# ──────────────────────────────────────────
		# 抽魂結果卡：ja (即時切換至日文，零件 真鍮の歯車 / パーツ)
		# ──────────────────────────────────────────
		11:
			if _wait == 5:
				_loc.call("set_locale", "ja")
			elif _wait == 25:
				var path := OUT_DIR + "/proof_02_ja_soul_result_card.png"
				_save_screenshot(path)
				_save_crop(path, CROPS_DIR + "/crop_02_ja_soul_badge_name.png", Rect2i(340, 360, 600, 180))
				print("  ✓ proof_02_ja_soul_result_card 完成")
				_step = 12
				_wait = 0

		# ──────────────────────────────────────────
		# 抽魂結果卡：ja 換裝展示 (着せ替え / 小白・クリーム普段着)
		# ──────────────────────────────────────────
		12:
			if _wait == 5:
				var drop_outfit := {
					"DropId": "outfit_cream",
					"kind": "outfit",
					"toastKey": "soul.pull_outfit"
				}
				if _soul_view.card != null:
					_soul_view.card.show_drop(drop_outfit)
			elif _wait == 25:
				var path := OUT_DIR + "/proof_03_ja_soul_result_outfit.png"
				_save_screenshot(path)
				_save_crop(path, CROPS_DIR + "/crop_03_ja_soul_outfit_badge.png", Rect2i(340, 360, 600, 180))
				print("  ✓ proof_03_ja_soul_result_outfit 完成")
				_step = 13
				_wait = 0

		# ──────────────────────────────────────────
		# 抽魂結果卡：zh_TW 換裝基準對照
		# ──────────────────────────────────────────
		13:
			if _wait == 5:
				_loc.call("set_locale", "zh_TW")
			elif _wait == 25:
				var path := OUT_DIR + "/proof_04_zh_TW_soul_result_card.png"
				_save_screenshot(path)
				print("  ✓ proof_04_zh_TW_soul_result_card 完成")
				# 清除抽魂畫面
				if _soul_view and is_instance_valid(_soul_view):
					_soul_view.queue_free()
					_soul_view = null
				_step = 20
				_wait = 0

		# ──────────────────────────────────────────
		# 裝備面板：en 頂部 (Equipment / Total Bonus / Loadout)
		# ──────────────────────────────────────────
		20:
			if _wait == 10:
				_loc.call("set_locale", "en")
				_main.call("_go_equip_panel")
			elif _wait == 30:
				var path := OUT_DIR + "/proof_05_en_equip_panel_top.png"
				_save_screenshot(path)
				print("  ✓ proof_05_en_equip_panel_top 完成")
				_step = 21
				_wait = 0

		# ──────────────────────────────────────────
		# 裝備面板：en 捲到底 (ScrollContainer 捲動至 600，返回鈕 Back 可見)
		# ──────────────────────────────────────────
		21:
			if _wait == 5:
				var host = _main.get("host")
				var scroll = host.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 600
				else:
					push_error("EquipScroll not found")
			elif _wait == 25:
				var path := OUT_DIR + "/proof_06_en_equip_panel_bottom.png"
				_save_screenshot(path)
				_save_crop(path, CROPS_DIR + "/crop_04_en_equip_back_btn_bottom.png", Rect2i(340, 380, 600, 320))
				# 特寫聚焦在第 6 個背包格 Bladestance Ring 文字排版
				_save_crop(path, CROPS_DIR + "/crop_06_en_equip_item_text_issue.png", Rect2i(475, 490, 145, 140))
				print("  ✓ proof_06_en_equip_panel_bottom 完成")
				_step = 22
				_wait = 0

		# ──────────────────────────────────────────
		# 裝備面板：zh_TW 頂部基準
		# ──────────────────────────────────────────
		22:
			if _wait == 10:
				_loc.call("set_locale", "zh_TW")
				_main.call("_go_equip_panel")
			elif _wait == 30:
				var path := OUT_DIR + "/proof_07_zh_TW_equip_panel_top.png"
				_save_screenshot(path)
				print("  ✓ proof_07_zh_TW_equip_panel_top 完成")
				_step = 23
				_wait = 0

		# ──────────────────────────────────────────
		# 裝備面板：zh_TW 捲到底基準 (返回按鈕可見)
		# ──────────────────────────────────────────
		23:
			if _wait == 5:
				var host = _main.get("host")
				var scroll = host.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 600
				else:
					push_error("EquipScroll not found")
			elif _wait == 25:
				var path := OUT_DIR + "/proof_08_zh_TW_equip_panel_bottom.png"
				_save_screenshot(path)
				_save_crop(path, CROPS_DIR + "/crop_05_zh_TW_equip_back_btn_bottom.png", Rect2i(340, 380, 600, 320))
				print("  ✓ proof_08_zh_TW_equip_panel_bottom 完成")
				_step = 30
				_wait = 0

		# ──────────────────────────────────────────
		# 大廳 Chrome 語系連動：en
		# ──────────────────────────────────────────
		30:
			if _wait == 10:
				_loc.call("set_locale", "en")
				_main.call("_go_mobile_lobby")
			elif _wait == 35:
				var path := OUT_DIR + "/proof_09_en_lobby_chrome.png"
				_save_screenshot(path)
				_save_crop(path, CROPS_DIR + "/crop_07_en_lobby_top_bar.png", Rect2i(0, 0, 1280, 80))
				_save_crop(path, CROPS_DIR + "/crop_08_en_lobby_dock.png", Rect2i(0, 630, 1280, 90))
				print("  ✓ proof_09_en_lobby_chrome 完成")
				_step = 31
				_wait = 0

		# ──────────────────────────────────────────
		# 大廳 Chrome 語系連動：ja (即時切換，大廳背景/HUD/Dock連動)
		# ──────────────────────────────────────────
		31:
			if _wait == 10:
				_loc.call("set_locale", "ja")
			elif _wait == 35:
				var path := OUT_DIR + "/proof_10_ja_lobby_chrome.png"
				_save_screenshot(path)
				_save_crop(path, CROPS_DIR + "/crop_09_ja_lobby_top_bar.png", Rect2i(0, 0, 1280, 80))
				_save_crop(path, CROPS_DIR + "/crop_10_ja_lobby_dock.png", Rect2i(0, 630, 1280, 90))
				print("  ✓ proof_10_ja_lobby_chrome 完成")
				_step = 32
				_wait = 0

		# ──────────────────────────────────────────
		# 大廳 Chrome 語系連動：zh_TW 基準
		# ──────────────────────────────────────────
		32:
			if _wait == 10:
				_loc.call("set_locale", "zh_TW")
			elif _wait == 35:
				var path := OUT_DIR + "/proof_11_zh_TW_lobby_chrome.png"
				_save_screenshot(path)
				print("  ✓ proof_11_zh_TW_lobby_chrome 完成")
				_step = 40
				_wait = 0

		# ──────────────────────────────────────────
		# 收尾結束
		# ──────────────────────────────────────────
		40:
			if _wait == 10:
				print("=== 全部 QA 第四十五輪實機巡檢存證截圖完成 ===")
				quit(0)
				return true

	return false
