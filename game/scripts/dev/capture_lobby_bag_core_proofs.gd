extends SceneTree
## 大廳背包未裝備機芯列表與整備換裝實機 Framebuffer 截圖 (capture_lobby_bag_core_proofs.gd)
## 依據任務 t_c3f9e4e0 驗收要求：
## 1. xvfb-run 實機圖（framebuffer，不准 PIL 假圖）：繁中、英文各至少「背包有機芯」一張＋「點進去整備」一張
## 2. 遵守 review.md 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖，零 PIL 假圖）
## 3. 遵守 review.md 0-QA23（OUT_DIR 鎖定 proofs/t_c3f9e4e0）
## 4. 遵守 review.md 0-QA28（六語系 ui.json 對齊，畫面 100% 過翻譯層）與 0-QA29

var _step := 0
var _wait := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()

var _loc_node: Node = null
var _main_scene: Node = null
var _lobby: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_proof_dir = env_out
		else:
			_proof_dir = base.path_join(env_out)
	else:
		_proof_dir = base.path_join("../proofs/t_c3f9e4e0")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")

func _find_lobby(node: Node) -> Control:
	if node == null:
		return null
	if node.get_script() != null and str(node.get_script().resource_path).ends_with("mobile_lobby.gd"):
		return node as Control
	for c in node.get_children():
		var res := _find_lobby(c)
		if res != null:
			return res
	return null

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 初始化場景環境並進入手遊大廳背包分頁
			if _wait < 35:
				return false
			_loc_node = root.get_node_or_null("Loc")
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game")
				gs.set("gold", 9999)
				gs.call("set_flag", "c1_forged", true)
				gs.call("set_flag", "c1_entered_city", true)
				gs.call("set_flag", "tut_done", true)

			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys and inv_sys.has_method("grant_starter"):
				inv_sys.call("grant_starter")

			_main_scene = current_scene
			if _main_scene and _main_scene.has_method("_go_mobile_lobby"):
				_main_scene.call("_go_mobile_lobby", 4) # Tab.BAG

			_step = 1
			_wait = 0

		1:
			# 獲取 lobby 實例並填充機芯背包
			if _wait < 25:
				return false

			_lobby = _find_lobby(root)
			if _lobby == null:
				push_error("無法找到 MobileLobby")
				quit(1)
				return true

			var CoreSystem = load("res://scripts/systems/core_system.gd")
			CoreSystem.clear_inventory()

			var p1 := {
				"uid": "proof_core_part_1",
				"slot": "mainspring",
				"slot_name": "發條發電機",
				"tier": "blue",
				"tier_name": "藍",
				"calibration_count": 0,
				"max_calibrations": 7,
				"stats": {"atk": 18, "crit": 2.5}
			}
			var p2 := {
				"uid": "proof_core_part_2",
				"slot": "chassis",
				"slot_name": "機殼裝甲",
				"tier": "white",
				"tier_name": "白",
				"calibration_count": 1,
				"max_calibrations": 7,
				"stats": {"def": 12, "hp": 40}
			}
			var p3 := {
				"uid": "proof_core_part_3",
				"slot": "escapement",
				"slot_name": "擒縱調速器",
				"tier": "orange",
				"tier_name": "橘",
				"calibration_count": 2,
				"max_calibrations": 7,
				"stats": {"crit": 4.0}
			}
			CoreSystem.add_part_to_inventory(p1)
			CoreSystem.add_part_to_inventory(p2)
			CoreSystem.add_part_to_inventory(p3)

			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			_lobby.call("_apply_locale_texts")
			_lobby.call("_refresh_bag_tab", false)

			_step = 10
			_wait = 0

		# ── 1. 繁體中文 (zh_TW) ──
		10:
			# 截圖 1: 繁中背包有機芯部件
			if _wait < 25:
				return false
			_save_frame("proof_bag_cores_zh_TW.png")

			# 點擊第 0 顆機芯部件卡片按鈕，進入角色整備
			var cards_box = _lobby.find_child("CoreCardsBox", true, false)
			if cards_box and cards_box.get_child_count() > 0:
				var card0 = cards_box.get_child(0)
				var btn: Button = card0.find_child("CardButton", true, false) as Button
				if btn:
					btn.pressed.emit()

			_step = 11
			_wait = 0

		11:
			# 截圖 2: 繁中點擊卡片後進入角色整備，機芯五槽在畫面上
			if _wait < 30:
				return false
			_save_frame("proof_equip_from_bag_zh_TW.png")

			# 關閉整備回到背包
			_lobby.call("close_equip_panel")

			# 切換至英文 (en)
			if _loc_node:
				_loc_node.call("set_locale", "en")
			_lobby.call("_apply_locale_texts")
			_lobby.call("_refresh_bag_tab", false)

			_step = 20
			_wait = 0

		# ── 2. 英文 (en) ──
		20:
			# 截圖 3: 英文背包有機芯部件 (無中文色階字)
			if _wait < 25:
				return false
			_save_frame("proof_bag_cores_en.png")

			# 點擊卡片進入整備
			var cards_box = _lobby.find_child("CoreCardsBox", true, false)
			if cards_box and cards_box.get_child_count() > 0:
				var card0 = cards_box.get_child(0)
				var btn: Button = card0.find_child("CardButton", true, false) as Button
				if btn:
					btn.pressed.emit()

			_step = 21
			_wait = 0

		21:
			# 截圖 4: 英文點擊卡片後進入角色整備，無中文色階字
			if _wait < 30:
				return false
			_save_frame("proof_equip_from_bag_en.png")

			# 關閉整備回到背包
			_lobby.call("close_equip_panel")

			# 切換至日文 (ja)
			if _loc_node:
				_loc_node.call("set_locale", "ja")
			_lobby.call("_apply_locale_texts")
			_lobby.call("_refresh_bag_tab", false)

			_step = 30
			_wait = 0

		# ── 3. 日文 (ja) ──
		30:
			# 截圖 5: 日文背包有機芯部件 (純正青階，無藍字)
			if _wait < 25:
				return false
			_save_frame("proof_bag_cores_ja.png")

			# 點擊卡片進入整備
			var cards_box = _lobby.find_child("CoreCardsBox", true, false)
			if cards_box and cards_box.get_child_count() > 0:
				var card0 = cards_box.get_child(0)
				var btn: Button = card0.find_child("CardButton", true, false) as Button
				if btn:
					btn.pressed.emit()

			_step = 31
			_wait = 0

		31:
			# 截圖 6: 日文點擊卡片後進入角色整備
			if _wait < 30:
				return false
			_save_frame("proof_equip_from_bag_ja.png")

			# 關閉整備回到背包
			_lobby.call("close_equip_panel")

			# 清空機芯背包，切換回繁中，驗證無機芯時無空白破版
			var CoreSystem = load("res://scripts/systems/core_system.gd")
			CoreSystem.clear_inventory()
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			_lobby.call("_apply_locale_texts")
			_lobby.call("_refresh_bag_tab", false)

			_step = 40
			_wait = 0

		# ── 4. 空背包無空白破版 ──
		40:
			# 截圖 7: 背包無未裝備機芯時不留空白破版
			if _wait < 25:
				return false
			_save_frame("proof_bag_empty_zh_TW.png")

			print("=== 全部實機 Framebuffer 截圖完成 ===")
			for p in _saved:
				print("  MEDIA:", p)
			quit(0)
			return true

	return false

func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		push_error("CAPTURE_FAIL: null image for " + filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	print("CAPTURE_SAVED: ", out_path, " err=", err, " size=", img.get_width(), "x", img.get_height())
	_saved.append(out_path)
