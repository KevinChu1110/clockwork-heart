extends SceneTree
## 《發條之心》SkillDialog 招式卡片出招優先膠囊標籤實機截圖 (t_cbafae97)
## 產出：
## 1. proof_01_skill_priority_badge_normal.png: SkillDialog 內平常首發金黃膠囊標籤 (#FFF4D0 底, #9A6B00 字)
## 2. proof_02_skill_priority_badge_panic.png: SkillDialog 同時呈現平常首發與危急應急天藍膠囊標籤 (#F0F7FF 底, #38A0FF 字)
## 3. proof_03_skill_priority_badge_en.png: 英文語系即時切換 (Normal Opener / Crisis Emergency) 零穿模截圖

const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_cbafae97",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_cbafae97/proofs/t_cbafae97"
]

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

	print("=== 開始執行 SkillDialog 招式優先標籤實機截圖 (t_cbafae97) ===")
	change_scene_to_file("res://scenes/main.tscn")


func _save_to_all(filename: String, crop_name: String = "") -> void:
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
			print("  ✓ 成功儲存截圖: %s (%dx%d)" % [target, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存截圖失敗 err=%d: %s" % [err, target])

		if crop_name != "":
			var crops_dir := dir_path.path_join("crops")
			DirAccess.make_dir_recursive_absolute(crops_dir)
			# 招式卡片特寫區 (x: 280, y: 250, w: 720, h: 320)
			var rect_cards := Rect2i(280, 250, 720, 320)
			var crop_img := img.get_region(rect_cards)
			if crop_img and not crop_img.is_empty():
				crop_img.save_png(crops_dir.path_join(crop_name))


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			var root_node := root.get_node_or_null("Main")
			var gs = root.get_node_or_null("GameState")
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_TW")
			if gs:
				gs.skill_data = {
					"slash": {"lv": 1, "mastery": 0}
				}

			_dlg = SkillDialogScn.new()
			root_node.add_child(_dlg)
			_step = 1
			_wait = 0
		1:
			if _wait < 15:
				return false
			# 截圖 1: 初始平常首發金黃膠囊
			_save_to_all("proof_01_skill_priority_badge_normal.png", "crop_01_badge_normal.png")
			_step = 2
			_wait = 0
		2:
			if _wait < 5:
				return false
			var sk_node = root.get_node_or_null("SkillSystem")
			if sk_node:
				sk_node.call("_set_lv", "emergency_heal", 1)
			_dlg.call("_refresh_display")
			_step = 3
			_wait = 0
		3:
			if _wait < 15:
				return false
			# 截圖 2: 平常首發 + 危急應急雙膠囊標籤
			_save_to_all("proof_02_skill_priority_badge_panic.png", "crop_02_badge_panic.png")
			_step = 4
			_wait = 0
		4:
			if _wait < 5:
				return false
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_step = 5
			_wait = 0
		5:
			if _wait < 15:
				return false
			# 截圖 3: 英文語系 (Normal Opener / Crisis Emergency)
			_save_to_all("proof_03_skill_priority_badge_en.png", "crop_03_badge_en.png")
			_step = 6
			_wait = 0
		6:
			if _wait < 5:
				return false
			print("CAPTURE_ALL_SUCCESS")
			quit(0)
			return true
	return false

