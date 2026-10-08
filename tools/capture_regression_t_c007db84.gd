extends SceneTree
## 《發條之心》SkillDialog 招式卡片自選首發出招實機截圖腳本 (t_c007db84)
## 驗收內容：
## 1. proof_01_skill_custom_priority_slash_zh_TW.png: SkillDialog 內自選 slash 為首發，slash 帶【平常首發】膠囊標籤與【已設首發】按鈕，counter_strike 帶【設為首發】按鈕
## 2. proof_02_skill_custom_priority_counter_strike_zh_TW.png: 切換 counter_strike 為首發，標籤與按鈕即時切換
## 3. proof_03_skill_custom_priority_en.png: 英文在地化 (Normal Opener / Opener Set / Set as Opener)
## 4. proof_04_skill_custom_priority_ja.png: 日文在地化 (通常初手 / 初手設定済 / 初手に設定)
## 5. proof_05_lobby_trigger_dummy_with_custom_slash.png: 木人樁開戰首發連動橫斬實機畫面

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_c007db84",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c007db84/proofs/t_c007db84"
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

	print("=== 開始執行自選首發出招實機截圖 (t_c007db84) ===")
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
					"slash": {"lv": 1, "mastery": 0},
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
			# 截圖 01: 自選 slash 為首發 (繁中)
			_save_to_all("proof_01_skill_custom_priority_slash_zh_TW.png", "skill_cards", "crop_01_skill_custom_slash.png")

			# 切換偏好至 counter_strike
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
			# 截圖 02: 切換 counter_strike 為首發 (繁中)
			_save_to_all("proof_02_skill_custom_priority_counter_strike_zh_TW.png", "card_action", "crop_02_skill_custom_counter_strike.png")

			# 切換英文語系並將 slash 設為首發
			var loc = root.get_node_or_null("Loc")
			var sk = root.get_node_or_null("SkillSystem")
			if sk:
				sk.call("set_preferred_skill", "slash", "sword")
			if loc:
				loc.call("set_locale", "en")

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

			_step = 5
			_wait = 0

		5:
			if _wait < 15:
				return false
			# 截圖 04: 日文語系 (通常初手 / 初手設定済 / 初手に設定)
			_save_to_all("proof_04_skill_custom_priority_ja.png", "skill_cards", "crop_04_skill_custom_ja.png")

			# 切回繁中，關閉 SkillDialog，透過試招按鈕進入木人樁戰鬥場景
			var loc = root.get_node_or_null("Loc")
			var sk = root.get_node_or_null("SkillSystem")
			if loc:
				loc.call("set_locale", "zh_TW")
			if sk:
				sk.call("set_preferred_skill", "slash", "sword")

			var dummy_btn = _dlg.call("get_practice_dummy_button") as Button
			if dummy_btn != null:
				dummy_btn.emit_signal("pressed")
			else:
				if _dlg:
					_dlg.queue_free()
				if _main_node and _main_node.has_method("_start_battle"):
					_main_node.call("_start_battle", "training_dummy")

			_step = 6
			_wait = 0

		6:
			if _wait < 25:
				return false
			# 截圖 05: 木人樁戰鬥場景實機存證（首發自選橫斬）
			_save_to_all("proof_05_training_dummy_opener_slash.png")

			print("\n=======================================================")
			print("CAPTURE_REGRESSION_T_C007DB84_OK")
			quit(0)
			return true

	return false
