extends SceneTree
## 探索性 QA 第四十六輪：六語系與裝備面板合主線後實機巡檢存證腳本 (tools/capture_qa_round46.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收清單：
## 1. 裝備品質標籤（ja/ko/es/zh_CN）
## 2. 裝備面板英文折行（Bladestance Ring / Rare）與繁中殘留 sword 修復（· 劍）
## 3. W8 Hub 殼玩家可見字六語系在地化與即時刷新（en / ja）
## 4. 過場字幕繼續提示（桌面繁中 / 觸控英文 / 觸控日文）
## 5. 大廳主角戳碰氣泡六語系（en / ja）
## 6. 聚魂完畢提示六語系（ja / zh_TW）

const OUT_DIR_NAME := "proofs/qa_round46"
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const CutscenePlayerScript = preload("res://scripts/ui/cutscene_player.gd")

var _step := 0
var _wait := 0

var _out_dir: String = ""
var _crops_dir: String = ""

var _loc_node: Node = null
var _gs: Node = null
var _dt: Node = null
var _eq_sys: Node = null

var _lobby: Control = null
var _host: MockHost = null
var _equip_ui: RefCounted = null
var _hub: Control = null
var _player: Control = null

class MockHost extends Control:
	var ui_container: Control
	func _init():
		set_anchors_preset(Control.PRESET_FULL_RECT)
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		ui_container = Control.new()
		ui_container.set_anchors_preset(Control.PRESET_FULL_RECT)
		ui_container.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(ui_container)
	func ui_host() -> Control:
		return ui_container
	func ui_clear_host() -> void:
		for c in ui_container.get_children():
			ui_container.remove_child(c)
			c.queue_free()
	func ui_reset_fade() -> void:
		pass
	func ui_refresh_hud() -> void:
		pass
	func ui_goto(_target: String) -> void:
		pass
	func ui_toast(_msg: String) -> void:
		pass

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	_crops_dir = _out_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_dt = root.get_node_or_null("DataTables")
	if _dt == null:
		var DtClass = load("res://scripts/systems/data_tables.gd")
		if DtClass:
			_dt = DtClass.new()
			_dt.name = "DataTables"
			root.add_child(_dt)

	_eq_sys = root.get_node_or_null("EquipmentSystem")
	if _eq_sys == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq_sys = EqClass.new()
			_eq_sys.name = "EquipmentSystem"
			root.add_child(_eq_sys)

	_init_player_data()

	print("=== 開始執行探索性 QA 第四十六輪實機存證截圖腳本 (qa_round46) ===")
	print("OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0

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

	if _eq_sys:
		var w1 = _eq_sys.call("roll_instance", "rusty_blade", "common")
		_eq_sys.call("equip_weapon_to_loadout", w1.uid, 0)
		var w2 = _eq_sys.call("roll_instance", "meager_edge", "uncommon")
		_eq_sys.call("equip_weapon_to_loadout", w2.uid, 1)
		var a1 = _eq_sys.call("roll_instance", "ash_mail", "common")
		_eq_sys.call("equip", a1.uid)

		var b1 = _eq_sys.call("roll_instance", "knight_saber", "rare")
		_eq_sys.call("add_to_bag", b1)
		var b2 = _eq_sys.call("roll_instance", "dawn_blade", "epic")
		_eq_sys.call("add_to_bag", b2)
		var b3 = _eq_sys.call("roll_instance", "knight_plate", "rare")
		_eq_sys.call("add_to_bag", b3)
		var b4 = _eq_sys.call("roll_instance", "star_pendant", "uncommon")
		_eq_sys.call("add_to_bag", b4)
		var b5 = _eq_sys.call("roll_instance", "scar_amulet", "rare")
		_eq_sys.call("add_to_bag", b5)
		var b6 = _eq_sys.call("roll_instance", "blade_ring", "rare")
		_eq_sys.call("add_to_bag", b6)
		var b7 = _eq_sys.call("roll_instance", "dawn_blade", "legendary")
		_eq_sys.call("add_to_bag", b7)

func _clear_scene() -> void:
	if _host and is_instance_valid(_host):
		_host.queue_free()
		_host = null
	if _lobby and is_instance_valid(_lobby):
		_lobby.queue_free()
		_lobby = null
	if _hub and is_instance_valid(_hub):
		_hub.queue_free()
		_hub = null
	if _player and is_instance_valid(_player):
		_player.queue_free()
		_player = null
	_equip_ui = null

func _save_screenshot(target_path: String) -> void:
	var tex := root.get_texture()
	if tex == null:
		push_error("Root texture is null")
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

func _setup_equip_scene(locale: String) -> void:
	_clear_scene()
	if _loc_node:
		_loc_node.call("set_locale", locale)

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		_lobby.name = "MobileLobby"
		root.add_child(_lobby)

	_host = MockHost.new()
	root.add_child(_host)

	var EquipPanelScn: GDScript = load("res://scripts/ui/panels/equip_panel.gd")
	_equip_ui = EquipPanelScn.new(_host)
	_equip_ui.call("open")

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		# ── Phase 1: 裝備品質標籤四語系（ja / ko / es / zh_CN）──
		# Step 1: ja 裝備品質標籤
		1:
			if _wait == 1:
				_setup_equip_scene("ja")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 500
			elif _wait == 30:
				var path := "%s/proof_01_ja_equip_quality.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_01_ja_equip_quality.png" % _crops_dir, Rect2i(350, 240, 580, 440))
				print("  ✓ [1/15] proof_01_ja_equip_quality 完成")
				_step = 2
				_wait = 0

		# Step 2: ko 裝備品質標籤
		2:
			if _wait == 1:
				_setup_equip_scene("ko")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 500
			elif _wait == 30:
				var path := "%s/proof_02_ko_equip_quality.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_02_ko_equip_quality.png" % _crops_dir, Rect2i(350, 240, 580, 440))
				print("  ✓ [2/15] proof_02_ko_equip_quality 完成")
				_step = 3
				_wait = 0

		# Step 3: es 裝備品質標籤
		3:
			if _wait == 1:
				_setup_equip_scene("es")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 500
			elif _wait == 30:
				var path := "%s/proof_03_es_equip_quality.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_03_es_equip_quality.png" % _crops_dir, Rect2i(350, 240, 580, 440))
				print("  ✓ [3/15] proof_03_es_equip_quality 完成")
				_step = 4
				_wait = 0

		# Step 4: zh_CN 裝備品質標籤
		4:
			if _wait == 1:
				_setup_equip_scene("zh_CN")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 500
			elif _wait == 30:
				var path := "%s/proof_04_zh_CN_equip_quality.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_04_zh_CN_equip_quality.png" % _crops_dir, Rect2i(350, 240, 580, 440))
				print("  ✓ [4/15] proof_04_zh_CN_equip_quality 完成")
				_step = 5
				_wait = 0

		# ── Phase 2: 裝備面板英文折行與繁中殘字 ──
		# Step 5: en 裝備面板折行與品質標籤
		5:
			if _wait == 1:
				_setup_equip_scene("en")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 600
			elif _wait == 30:
				var path := "%s/proof_05_en_equip_wrap.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_05_en_equip_wrap.png" % _crops_dir, Rect2i(470, 480, 170, 160))
				print("  ✓ [5/15] proof_05_en_equip_wrap 完成")
				_step = 6
				_wait = 0

		# Step 6: zh_TW 裝備面板武器欄位（驗證無 sword 殘字）
		6:
			if _wait == 1:
				_setup_equip_scene("zh_TW")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 600
			elif _wait == 30:
				var path := "%s/proof_06_zh_TW_equip_weapon.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_06_zh_TW_equip_weapon.png" % _crops_dir, Rect2i(365, 360, 250, 150))
				print("  ✓ [6/15] proof_06_zh_TW_equip_weapon 完成")
				_clear_scene()
				_step = 7
				_wait = 0

		# ── Phase 3: W8 Hub 殼六語系與即時動態刷新 ──
		# Step 7: en W8 Hub 殼
		7:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var HubClass = load("res://scripts/systems/wave8/w8_hub_view.gd")
				_hub = HubClass.new()
				_hub.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_hub)
				_hub.call("_goto", 2) # Phase.CHAPTER
			elif _wait == 30:
				var path := "%s/proof_07_en_w8_hub.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_07_en_w8_hub.png" % _crops_dir, Rect2i(20, 10, 1240, 680))
				print("  ✓ [7/15] proof_07_en_w8_hub 完成")
				_step = 8
				_wait = 0

		# Step 8: ja W8 Hub 殼（即時動態切換語系 0-QA25 檢查）
		8:
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
			elif _wait == 30:
				var path := "%s/proof_08_ja_w8_hub.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_08_ja_w8_hub.png" % _crops_dir, Rect2i(20, 10, 1240, 680))
				print("  ✓ [8/15] proof_08_ja_w8_hub 完成")
				_clear_scene()
				_step = 9
				_wait = 0

		# ── Phase 4: 過場字幕繼續提示對齊對話框 ──
		# Step 9: 繁中桌面模式（點擊 / Space 繼續）
		9:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_player = CutscenePlayerScript.new()
				root.add_child(_player)
				_player.set("force_touch_mode", false)
				var slides := [
					{
						"bg": "village",
						"portrait": "maisui",
						"speaker": "麥穗",
						"text": "在這個被齒輪與發條運轉的世界裡，每一顆心臟都有它甦醒的時刻。",
						"hold": 0.0,
					}
				]
				_player.call("play", slides, Callable())
			elif _wait == 35:
				var path := "%s/proof_09_desktop_zh_TW_cutscene.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_09_desktop_zh_TW_cutscene.png" % _crops_dir, Rect2i(770, 610, 460, 80))
				print("  ✓ [9/15] proof_09_desktop_zh_TW_cutscene 完成")
				_step = 10
				_wait = 0

		# Step 10: 英文觸控模式（Tap to continue）
		10:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_player = CutscenePlayerScript.new()
				root.add_child(_player)
				_player.set("force_touch_mode", true)
				var slides := [
					{
						"bg": "village",
						"portrait": "maisui",
						"speaker": "麥穗",
						"text": "In a world driven by gears and wind-up springs, every heart has its awakening moment.",
						"hold": 0.0,
					}
				]
				_player.call("play", slides, Callable())
			elif _wait == 35:
				var path := "%s/proof_10_touch_en_cutscene.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_10_touch_en_cutscene.png" % _crops_dir, Rect2i(770, 610, 460, 80))
				print("  ✓ [10/15] proof_10_touch_en_cutscene 完成")
				_step = 11
				_wait = 0

		# Step 11: 日文觸控模式（タップで進む）
		11:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				_player = CutscenePlayerScript.new()
				root.add_child(_player)
				_player.set("force_touch_mode", true)
				var slides := [
					{
						"bg": "village",
						"portrait": "maisui",
						"speaker": "麥穗",
						"text": "歯車とぜんまいで動くこの世界で、すべての心臓に目覚めの時がある。",
						"hold": 0.0,
					}
				]
				_player.call("play", slides, Callable())
			elif _wait == 35:
				var path := "%s/proof_11_touch_ja_cutscene.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_11_touch_ja_cutscene.png" % _crops_dir, Rect2i(770, 610, 460, 80))
				print("  ✓ [11/15] proof_11_touch_ja_cutscene 完成")
				_clear_scene()
				_step = 12
				_wait = 0

		# ── Phase 5: 大廳主角戳碰氣泡 ──
		# Step 12: en 大廳戳碰氣泡
		12:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 0) # Tab.VILLAGE
				_lobby.call("_on_hero_clicked", 0, 1) # 台詞 1
			elif _wait == 20:
				var bubble = _lobby.get("_speech_bubble") as Control
				if bubble:
					bubble.visible = true
					bubble.modulate.a = 1.0
			elif _wait == 30:
				var path := "%s/proof_12_en_lobby_poke.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_12_en_lobby_poke.png" % _crops_dir, Rect2i(420, 110, 460, 150))
				print("  ✓ [12/15] proof_12_en_lobby_poke 完成")
				_step = 13
				_wait = 0

		# Step 13: ja 大廳戳碰氣泡
		13:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 0) # Tab.VILLAGE
				_lobby.call("_on_hero_clicked", 0, 1) # 台詞 1
			elif _wait == 20:
				var bubble = _lobby.get("_speech_bubble") as Control
				if bubble:
					bubble.visible = true
					bubble.modulate.a = 1.0
			elif _wait == 30:
				var path := "%s/proof_13_ja_lobby_poke.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_13_ja_lobby_poke.png" % _crops_dir, Rect2i(420, 110, 460, 150))
				print("  ✓ [13/15] proof_13_ja_lobby_poke 完成")
				_step = 14
				_wait = 0

		# ── Phase 6: 聚魂完畢提示 ──
		# Step 14: ja 聚魂完畢 toast
		14:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
				var toast_text: String = ContentLoc.text("ui", "聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
				_lobby.call("_show_toast", toast_text)
			elif _wait == 15:
				var toast = _lobby.get("_current_toast") as Label
				if toast:
					toast.visible = true
					toast.modulate.a = 1.0
			elif _wait == 25:
				var path := "%s/proof_14_ja_lobby_toast.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_14_ja_lobby_toast.png" % _crops_dir, Rect2i(280, 40, 720, 110))
				print("  ✓ [14/15] proof_14_ja_lobby_toast 完成")
				_step = 15
				_wait = 0

		# Step 15: zh_TW 聚魂完畢 toast
		15:
			if _wait == 1:
				_clear_scene()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
				var toast_text: String = ContentLoc.text("ui", "聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
				_lobby.call("_show_toast", toast_text)
			elif _wait == 15:
				var toast = _lobby.get("_current_toast") as Label
				if toast:
					toast.visible = true
					toast.modulate.a = 1.0
			elif _wait == 25:
				var path := "%s/proof_15_zh_TW_lobby_toast.png" % _out_dir
				_save_screenshot(path)
				_save_crop(path, "%s/crop_15_zh_TW_lobby_toast.png" % _crops_dir, Rect2i(280, 40, 720, 110))
				print("  ✓ [15/15] proof_15_zh_TW_lobby_toast 完成")
				_clear_scene()
				_step = 16
				_wait = 0

		# Step 16: 完成退出
		16:
			print("=== 全數 15 張實機截圖與 15 張 Crops 生成完畢！ ===")
			print("QA_ROUND46_CAPTURE_OK")
			quit(0)
			return true

	return false
