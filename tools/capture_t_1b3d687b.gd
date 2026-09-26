extends SceneTree
## 裝備面板缺陷修復存證截圖腳本 (tools/capture_t_1b3d687b.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
##
## 驗證重點：
## 1. 英文裝備名折行保護與品質標籤不壓線不溢出 (Bladestance Ring / Rare)。
## 2. 繁中背包武器品質標籤無未翻譯英文 sword，正確顯示武器類型（· 劍）。
## 3. OUT_DIR 嚴格限定為 proofs/t_1b3d687b/ (0-QA23 專屬目錄，絕無跨卡覆蓋)。
## 4. 1280x720 實機全景 + 必要特寫 Crops。

var _step := 0
var _wait := 0
var _main: Node = null
var _loc: Node = null
var _gs: Node = null
var _eq: Node = null

var OUT_DIR := ""
var CROPS_DIR := ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/t_1b3d687b")
	OUT_DIR = resolved_dir
	CROPS_DIR = resolved_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	print("=== 開始執行 t_1b3d687b 實機存證截圖腳本 ===")
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
			if _wait < 30:
				return false
			_main = current_scene
			_loc = root.get_node_or_null("Loc")
			_gs = root.get_node_or_null("GameState")
			_eq = root.get_node_or_null("EquipmentSystem")
			_init_player_data()
			print("1. 準備開始測試 en 裝備面板背包區域...")
			_step = 10
			_wait = 0

		# ── 裝備面板：en 捲到底 (proof_01) ──
		10:
			if _wait == 10:
				_loc.call("set_locale", "en")
				_main.call("_go_equip_panel")
			elif _wait == 25:
				var host = _main.get("host")
				var scroll = host.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 600
				else:
					push_error("EquipScroll not found")
			elif _wait == 40:
				var path := OUT_DIR + "/proof_01_en_equip_panel_bottom.png"
				_save_screenshot(path)
				# 特寫聚焦在第 6 個背包格 Bladestance Ring 與品質標籤 Rare
				_save_crop(path, CROPS_DIR + "/crop_01_en_equip_blade_ring.png", Rect2i(475, 490, 150, 145))
				print("  ✓ proof_01_en_equip_panel_bottom 完成")
				_step = 20
				_wait = 0

		# ── 裝備面板：zh_TW 動態切換語系並捲到底 (proof_02) ──
		20:
			if _wait == 10:
				# 開著面板切換語系至 zh_TW，驗證即時連動
				_loc.call("set_locale", "zh_TW")
			elif _wait == 25:
				var host = _main.get("host")
				var scroll = host.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 600
				else:
					push_error("EquipScroll not found")
			elif _wait == 40:
				var path := OUT_DIR + "/proof_02_zh_TW_equip_panel_bottom.png"
				_save_screenshot(path)
				# 特寫聚焦在第 1、2 格武器（騎士軍刀、晨光長劍）品質標籤「上品 · 劍」/「秘寶 · 劍」
				_save_crop(path, CROPS_DIR + "/crop_02_zh_TW_equip_weapon_slot.png", Rect2i(365, 360, 250, 145))
				print("  ✓ proof_02_zh_TW_equip_panel_bottom 完成")
				_step = 30
				_wait = 0

		30:
			print("=== 所有截圖存證完成！ ===")
			quit(0)
	return false
