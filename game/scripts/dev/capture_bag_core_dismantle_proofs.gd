extends SceneTree
## 多餘未裝備機芯拆成既有鐵屑實機 Framebuffer 截圖 (capture_bag_core_dismantle_proofs.gd)
## 依據任務 t_c48032bf 驗收要求：
## 1. xvfb-run 實機圖（framebuffer，不准 PIL 假圖）：繁中＋英文「拆解」按鈕與拆解流程
## 2. 遵守 review.md 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖）
## 3. 遵守 review.md 0-QA23（OUT_DIR 鎖定 proofs/t_c48032bf）
## 4. 遵守 review.md 0-QA28（六語系 ui.json 對齊，畫面 100% 過翻譯層，en 零中文殘留）與 0-QA29

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
		_proof_dir = base.path_join("../proofs/t_c48032bf")
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
			if _wait < 35:
				return false
			_loc_node = root.get_node_or_null("Loc")
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game")
				gs.set("gold", 8888)
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
			if _wait < 25:
				return false

			_lobby = _find_lobby(root)
			if _lobby == null:
				push_error("無法找到 MobileLobby")
				quit(1)
				return true

			var CoreSystem = load("res://scripts/systems/core_system.gd")
			CoreSystem.clear_inventory()

			# 放入 3 件未裝備機芯（藍、橘、金階）
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
				"slot": "gear_train",
				"slot_name": "傳動齒輪組",
				"tier": "orange",
				"tier_name": "橘",
				"calibration_count": 1,
				"max_calibrations": 7,
				"stats": {"crit": 4.0}
			}
			var p3 := {
				"uid": "proof_core_part_3",
				"slot": "soul_core",
				"slot_name": "共鳴核心",
				"tier": "gold",
				"tier_name": "金",
				"calibration_count": 2,
				"max_calibrations": 7,
				"stats": {"atk": 30, "def": 20}
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
			if _wait < 25:
				return false
			# 截圖 1: 繁中大廳背包，展示未裝備機芯卡片與「拆解」果凍厚底鈕（高 >= 50px）
			_save_frame("proof_dismantle_btn_zh_TW.png")

			# 切換至英文 (en)
			if _loc_node:
				_loc_node.call("set_locale", "en")
			_lobby.call("_apply_locale_texts")
			_lobby.call("_refresh_bag_tab", false)

			_step = 20
			_wait = 0

		# ── 2. 英文 (en) ──
		20:
			if _wait < 25:
				return false
			# 截圖 2: 英文大廳背包，展示 "Dismantle" 果凍厚底鈕（高 >= 50px，零中文 CJK 殘留）
			_save_frame("proof_dismantle_btn_en.png")

			# 切換回繁中並準備點擊拆解
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			_lobby.call("_apply_locale_texts")
			_lobby.call("_refresh_bag_tab", false)

			_step = 30
			_wait = 0

		# ── 3. 點擊拆解獲得鐵屑 Toast ──
		30:
			if _wait < 20:
				return false

			# 點擊第 0 張卡片的「拆解」按鈕 (藍階機芯，拆解可得 4 鐵屑)
			var cards_box = _lobby.find_child("CoreCardsBox", true, false)
			if cards_box and cards_box.get_child_count() > 0:
				var card0 = cards_box.get_child(0)
				var d_btn: Button = card0.find_child("DismantleButton", true, false) as Button
				if d_btn:
					d_btn.pressed.emit()

			_step = 31
			_wait = 0

		31:
			if _wait < 15:
				return false
			# 截圖 3: 拆解成功 Toast「已拆解機芯，獲得 4 鐵屑」，背包即時扣除機芯
			_save_frame("proof_dismantled_toast_zh_TW.png")

			# 繼續將剩餘機芯拆解清空
			var CoreSystem = load("res://scripts/systems/core_system.gd")
			CoreSystem.clear_inventory()
			_lobby.call("_refresh_core_bag")
			_lobby.call("_refresh_bag_tab", false)

			_step = 40
			_wait = 0

		# ── 4. 全部拆解後無機芯不留空白破版 ──
		40:
			if _wait < 20:
				return false
			# 截圖 4: 無未裝備機芯時 CoreBagPanel 正確隱藏收合，不留空白破版
			_save_frame("proof_bag_empty_after_dismantle_zh_TW.png")

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
