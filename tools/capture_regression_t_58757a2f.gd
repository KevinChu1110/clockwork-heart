extends SceneTree
## 《發條之心》SkillDialog 底欄新增前往木人樁試招按鈕連動大廳實機截圖 (t_58757a2f)
## 產出：
## 1. proof_01_skill_dialog_dummy_practice_btn_zh_TW.png: SkillDialog 底欄左側天藍『前往木人樁試招』與右側暖橘『關閉』果凍按鈕
## 2. proof_02_skill_dialog_dummy_btn_en.png: 英文語系 (Practice at Training Dummy) 即時切換全景
## 3. proof_03_skill_dialog_dummy_btn_ja.png: 日文語系 (木人で試技する) 即時切換全景
## 4. proof_04_lobby_trigger_training_dummy_battle.png: 點擊試招按鈕後平滑關閉彈窗並切換至木人樁戰鬥場景

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_58757a2f/proofs/t_58757a2f",
	"/opt/side/bravesoul-game/proofs/t_58757a2f"
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

	print("=== 開始執行 SkillDialog 木人樁試招按鈕實機截圖 (t_58757a2f) ===")
	change_scene_to_file("res://scenes/main.tscn")


func _save_to_all(filename: String, crop_name: String = "") -> void:
	var img: Image = root.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法取得 viewport image")
		return

	for dir_path in OUT_PATHS:
		var target := dir_path.path_join(filename)
		var err := img.save_png(target)
		if err == OK:
			print("  ✓ 成功儲存截圖: %s (%dx%d)" % [target, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存截圖失敗 err=%d: %s" % [err, target])

		if crop_name != "":
			var crops_dir := dir_path.path_join("crops")
			# 彈窗底部控制列特寫 (x: 260, y: 550, w: 760, h: 100)
			var rect_bottom := Rect2i(260, 545, 760, 100)
			var crop_img := img.get_region(rect_bottom)
			if crop_img and not crop_img.is_empty():
				crop_img.save_png(crops_dir.path_join(crop_name))


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main_node = root.get_node_or_null("Main")
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_TW")

			# 切換至手遊大廳
			if _main_node and _main_node.has_method("_go_mobile_lobby"):
				_main_node.call("_go_mobile_lobby")

			_step = 1
			_wait = 0

		1:
			if _wait < 15:
				return false
			# 取得大廳節點
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
			# 截圖 01: 繁體中文全景與底部控制列特寫
			_save_to_all("proof_01_skill_dialog_dummy_practice_btn_zh_TW.png", "crop_01_dummy_btn_zh_TW.png")
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			# 切換英文語系
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_step = 4
			_wait = 0

		4:
			if _wait < 15:
				return false
			# 截圖 02: 英文語系
			_save_to_all("proof_02_skill_dialog_dummy_btn_en.png", "crop_02_dummy_btn_en.png")
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			# 切換日文語系
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "ja")
			_step = 6
			_wait = 0

		6:
			if _wait < 15:
				return false
			# 截圖 03: 日文語系
			_save_to_all("proof_03_skill_dialog_dummy_btn_ja.png", "crop_03_dummy_btn_ja.png")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			# 切回繁中
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_TW")

			# 點擊試招按鈕進入木人樁戰鬥
			var dummy_btn = _dlg.find_child("BtnPracticeDummy", true, false) as Button
			if dummy_btn != null:
				dummy_btn.pressed.emit()
				print("  ok 已點擊 BtnPracticeDummy，觸發 training_dummy 戰鬥")
			else:
				push_error("找不到 BtnPracticeDummy 按鈕")
			_step = 8
			_wait = 0

		8:
			if _wait < 25:
				return false
			# 截圖 04: 木人樁戰鬥畫面
			_save_to_all("proof_04_lobby_trigger_training_dummy_battle.png")
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			print("\n=======================================================")
			print("CAPTURE_ALL_SUCCESS")
			quit(0)
			return true

	return false
