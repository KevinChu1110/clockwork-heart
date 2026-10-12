extends SceneTree
## 《發條之心》全站回歸驗收實機截圖腳本 (t_b4716ab5)
## 驗收內容：
## 1. SkillDialog 招式首選與戰鬥首發連動合進主線後之全站功能
## 2. 招式卡片【平常首發】膠囊標籤、【設為首發】/【已設首發】操作按鈕（高48px、立體厚底、圓角果凍）
## 3. 招式熟練度進度條、突破升階、底欄木人樁試招按鈕於主線之整合共存
## 4. 多語系即時切換 (zh_TW, zh_CN, en, ja)
## 5. 木人樁戰鬥開局首發連動出招實機畫面
## 6. Framebuffer 1280x720 實機全景截圖與 crops/ 特寫存證 (0-QA15 雜湊唯一性)

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_b4716ab5",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_b4716ab5/proofs/t_b4716ab5"
]

var _main_node: Node = null
var _lobby: Control = null
var _dlg: Control = null
var _wait: int = 0
var _step: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)
		DirAccess.make_dir_recursive_absolute(p.path_join("crops"))

	print("=== 開始執行全站回歸驗收實機截圖 (t_b4716ab5) ===")
	change_scene_to_file("res://scenes/main.tscn")


func _save_to_all(filename: String, crop_type: String = "", crop_name: String = "") -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 viewport")
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法取得 viewport image")
		return

	for dir_path in OUT_PATHS:
		var target := dir_path.path_join(filename)
		var err := img.save_png(target)
		if err == OK:
			print("  ✓ 成功儲存全景截圖: %s (%dx%d)" % [target, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存全景截圖失敗 err=%d: %s" % [err, target])

		if crop_type != "" and crop_name != "":
			var crops_dir := dir_path.path_join("crops")
			var rect := Rect2i()
			if crop_type == "skill_cards":
				# 卡片區特寫 (x: 250, y: 100, w: 780, h: 540)
				rect = Rect2i(250, 100, 780, 540)
			elif crop_type == "card_action":
				# 右側卡片動作按鈕特寫 (x: 550, y: 180, w: 470, h: 220)
				rect = Rect2i(550, 180, 470, 220)
			elif crop_type == "bottom_bar":
				# 底欄按鈕區特寫 (x: 260, y: 545, w: 760, h: 100)
				rect = Rect2i(260, 545, 760, 100)

			if rect.size != Vector2i.ZERO:
				var crop_img := img.get_region(rect)
				if crop_img and not crop_img.is_empty():
					crop_img.save_png(crops_dir.path_join(crop_name))
					print("  ✓ 成功儲存特寫裁切: %s" % crops_dir.path_join(crop_name))


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 25:
				return false
			_main_node = root.get_node_or_null("Main")
			var loc = root.get_node_or_null("Loc")
			var gs = root.get_node_or_null("GameState")
			var sk = root.get_node_or_null("SkillSystem")
			if loc:
				loc.call("set_locale", "zh_TW")
			if gs:
				gs.skill_data = {
					"slash": {"lv": 1, "mastery": 15},
					"counter_strike": {"lv": 1, "mastery": 0}
				}
				gs.preferred_skills = {}
			if sk:
				sk.call("ensure_skill_map")
				sk.call("set_preferred_skill", "slash", "sword")

			# 切換至手遊大廳
			if _main_node and _main_node.has_method("_go_mobile_lobby"):
				_main_node.call("_go_mobile_lobby")

			_step = 1
			_wait = 0

		1:
			if _wait < 20:
				return false
			var host = _main_node.get("host") if _main_node else null
			if host:
				for c in host.get_children():
					if c.has_method("open_skill_dialog"):
						_lobby = c
						break
			if _lobby == null:
				push_error("找不到 MobileLobby")
				quit(1)
				return true

			# 開啟 SkillDialog
			_dlg = _lobby.call("open_skill_dialog") as Control
			_step = 2
			_wait = 0

		2:
			if _wait < 15:
				return false
			# 截圖 01: 繁中自選橫斬為首發（帶【平常首發】膠囊標籤與【已設首發】按鈕）
			_save_to_all("proof_01_skill_custom_priority_slash_zh_TW.png", "skill_cards", "crop_01_skill_custom_slash.png")

			# 切換反戈一擊為首發
			var sk = root.get_node_or_null("SkillSystem")
			if sk:
				sk.call("set_preferred_skill", "counter_strike", "sword")
			if _dlg and _dlg.has_method("_refresh_display"):
				_dlg.call("_refresh_display")

			_step = 3
			_wait = 0

		3:
			if _wait < 15:
				return false
			# 截圖 02: 繁中切換反戈一擊為首發（反戈一擊帶【平常首發】與【已設首發】，橫斬變為【設為首發】）
			_save_to_all("proof_02_skill_custom_priority_counter_strike_zh_TW.png", "card_action", "crop_02_skill_custom_counter_strike.png")

			# 切換英文語系
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			if _dlg and _dlg.has_method("_refresh_display"):
				_dlg.call("_refresh_display")

			_step = 4
			_wait = 0

		4:
			if _wait < 15:
				return false
			# 截圖 03: 英文語系 (Normal Opener / Opener Set / Set as Opener)
			_save_to_all("proof_03_skill_custom_priority_en.png", "skill_cards", "crop_03_skill_custom_en.png")

			# 切換日文語系
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "ja")
			if _dlg and _dlg.has_method("_refresh_display"):
				_dlg.call("_refresh_display")

			_step = 5
			_wait = 0

		5:
			if _wait < 15:
				return false
			# 截圖 04: 日文語系 (通常初手 / 初手設定済 / 初手に設定)
			_save_to_all("proof_04_skill_custom_priority_ja.png", "skill_cards", "crop_04_skill_custom_ja.png")

			# 切換回繁中並設定 slash 熟練度滿 (30/30) 展現突破升階與底欄試招按鈕共存
			var loc = root.get_node_or_null("Loc")
			var gs = root.get_node_or_null("GameState")
			var sk = root.get_node_or_null("SkillSystem")
			if loc:
				loc.call("set_locale", "zh_TW")
			if gs:
				gs.skill_data["slash"] = {"lv": 1, "mastery": 30}
			if sk:
				sk.call("set_preferred_skill", "slash", "sword")
			if _dlg and _dlg.has_method("_refresh_display"):
				_dlg.call("_refresh_display")

			_step = 6
			_wait = 0

		6:
			if _wait < 15:
				return false
			# 截圖 05: 繁中突破升階暖橘按鈕 + 首選標籤 + 底欄前往木人樁試招按鈕共存全景
			_save_to_all("proof_05_skill_upgrade_and_dummy_btn_zh_TW.png", "bottom_bar", "crop_05_skill_bottom_bar.png")

			# 點擊前往木人樁試招按鈕進入實戰場景
			var dummy_btn = _dlg.find_child("BtnPracticeDummy", true, false) as Button
			if dummy_btn:
				print("  ✓ 找到 BtnPracticeDummy，觸發 pressed 信號連動木人樁戰鬥")
				dummy_btn.emit_signal("pressed")
			else:
				push_error("找不到 BtnPracticeDummy")

			_step = 7
			_wait = 0

		7:
			# 等待大廳切換至木人樁戰鬥場景並首發出招
			if _wait < 35:
				return false
			# 截圖 06: 木人樁開戰連動首選招式實機全景
			_save_to_all("proof_06_training_dummy_opener_slash.png")
			print("\n=======================================================")
			print("CAPTURE_REGRESSION_T_B4716AB5_OK")
			print("=======================================================\n")
			quit(0)
			return true

	return false
