extends SceneTree
## 《發條之心》全站回歸驗收實機截圖腳本 (t_8fe4da3b)
## 驗收內容：
## 1. SkillDialog 招式卡片熟練度進度條 (ProgressBar)、一鍵突破升階 (Orange Btn) 與體悟習得 (Mint Btn)
## 2. SkillDialog 底欄前往木人樁試招按鈕 (Sky Blue Btn) 與大廳連動切換木人樁戰鬥
## 3. 多語系即時切換 (zh_TW, zh_CN, en, ja)
## 4. 實機 Framebuffer 1280x720 截圖與 crops/ 特寫裁切存證 (符合 0-QA15 雜湊唯一性)

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_8fe4da3b",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_8fe4da3b/proofs/t_8fe4da3b"
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

	print("=== 開始執行全站回歸驗收實機截圖 (t_8fe4da3b) ===")
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
			if crop_type == "bottom_bar":
				# 底部試招按鈕區 (x: 260, y: 545, w: 760, h: 100)
				rect = Rect2i(260, 545, 760, 100)
			elif crop_type == "skill_cards":
				# 卡片區特寫 (x: 250, y: 100, w: 780, h: 540)
				rect = Rect2i(250, 100, 780, 540)
			elif crop_type == "card_action":
				# 右側卡片動作按鈕特寫 (x: 620, y: 180, w: 400, h: 220)
				rect = Rect2i(620, 180, 400, 220)

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
					"slash": {"lv": 1, "mastery": 15}
				}
			if sk:
				sk.call("ensure_skill_map")

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
			# 截圖 01: 熟練度進度條半滿 (15/30) + 體悟按鈕 (繁中)
			_save_to_all("proof_01_skill_progress_half_zh_TW.png", "skill_cards", "crop_01_skill_progress_half.png")

			# 設定 slash 熟練度達滿 (30/30)
			var gs = root.get_node_or_null("GameState")
			if gs:
				gs.skill_data["slash"] = {"lv": 1, "mastery": 30}
			if _dlg and _dlg.has_method("_refresh_display"):
				_dlg.call("_refresh_display")

			_step = 3
			_wait = 0

		3:
			if _wait < 10:
				return false
			# 截圖 02: 滿熟練度 (30/30) 觸發暖橘『突破升階』按鈕
			_save_to_all("proof_02_skill_upgrade_orange_btn_zh_TW.png", "card_action", "crop_02_skill_upgrade_btn.png")

			# 設定 slash 達到滿級 (Lv.3)
			var gs = root.get_node_or_null("GameState")
			if gs:
				gs.skill_data["slash"] = {"lv": 3, "mastery": 0}
			if _dlg and _dlg.has_method("_refresh_display"):
				_dlg.call("_refresh_display")

			_step = 4
			_wait = 0

		4:
			if _wait < 10:
				return false
			# 截圖 03: 滿級極階金色膠囊標籤
			_save_to_all("proof_03_skill_max_tier_gold_badge_zh_TW.png", "card_action", "crop_03_skill_max_badge.png")

			# 切換英文語系並重置 slash 為可突破
			var loc = root.get_node_or_null("Loc")
			var gs = root.get_node_or_null("GameState")
			if gs:
				gs.skill_data["slash"] = {"lv": 1, "mastery": 30}
			if loc:
				loc.call("set_locale", "en")
			_step = 5
			_wait = 0

		5:
			if _wait < 15:
				return false
			# 截圖 04: 英文語系即時在地化全景 (Breakthrough / Practice at Training Dummy / Lv.MAX 等)
			_save_to_all("proof_04_skill_upgrade_dialog_en.png", "skill_cards", "crop_04_skill_dialog_en.png")

			# 切換簡體中文 (zh_CN)
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_CN")
			_step = 6
			_wait = 0

		6:
			if _wait < 15:
				return false
			# 截圖 05: 簡體中文全景與底欄『前往木人桩试招』按鈕
			_save_to_all("proof_05_skill_dialog_bottom_dummy_btn_zh_CN.png", "bottom_bar", "crop_04_dummy_btn_zh_CN.png")

			# 切換日文語系
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "ja")
			_step = 7
			_wait = 0

		7:
			if _wait < 15:
				return false
			# 截圖 06: 日文語系全景與底欄『木人で試技する』特寫
			_save_to_all("proof_06_skill_dialog_bottom_dummy_btn_ja.png", "bottom_bar", "crop_05_dummy_btn_ja.png")

			# 切換回繁中並觸發木人樁試招按鈕
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_TW")

			# 找到試招按鈕並點擊
			var dummy_btn = _dlg.find_child("BtnPracticeDummy", true, false) as Button
			if dummy_btn:
				print("  ✓ 找到 BtnPracticeDummy，觸發 pressed 信號連動大廳")
				dummy_btn.emit_signal("pressed")
			else:
				push_error("找不到 BtnPracticeDummy")

			_step = 8
			_wait = 0

		8:
			# 等待大廳切換至戰鬥場景 (木人樁)
			if _wait < 30:
				return false
			# 截圖 07: 點擊試招按鈕後切換進入零消耗木人樁戰鬥場景全景
			_save_to_all("proof_07_lobby_link_training_dummy_battle.png")
			print("=== 全站回歸驗收實機截圖完成 (t_8fe4da3b) ===")
			quit(0)
			return true

	return false
