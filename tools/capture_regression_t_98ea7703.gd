extends SceneTree
## 《發條之心》SkillDialog 招式卡片熟練度進度條、一鍵突破升階與體悟習得實機截圖 (t_98ea7703)
## 產出：
## 1. proof_01_skill_progress_half.png: 熟練度進度條半滿 (15/30, 8px 薄荷綠條) 與『體悟習得』薄荷綠果凍按鈕
## 2. proof_02_skill_upgrade_button.png: 滿熟練度 (30/30) 觸發暖橘立體果凍『突破升階』按鈕 (高48px、底邊厚度4px)
## 3. proof_03_skill_max_tier_badge.png: 滿級招式展示『Lv.MAX · 極階』金色標籤 (無突破按鈕)
## 4. proof_04_skill_upgrade_en.png: 英文語系 (Breakthrough / Comprehend / Lv.MAX · Mastered) 即時對齊截圖

const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_98ea7703",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_98ea7703/proofs/t_98ea7703"
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

	print("=== 開始執行 SkillDialog 熟練度進度條與突破升階實機截圖 (t_98ea7703) ===")
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
			# 招式卡片彈窗特寫區 (x: 250, y: 100, w: 780, h: 540)
			var rect_cards := Rect2i(250, 100, 780, 540)
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
			var sk = root.get_node_or_null("SkillSystem")
			if loc:
				loc.call("set_locale", "zh_TW")
			if gs:
				gs.skill_data = {
					"slash": {"lv": 1, "mastery": 15}
				}
			if sk:
				sk.call("ensure_skill_map")

			_dlg = SkillDialogScn.new()
			root_node.add_child(_dlg)
			_step = 1
			_wait = 0

		1:
			# 等待 5 幀後拍攝 proof 1: 熟練度半滿 + 體悟按鈕
			if _wait >= 5:
				_save_to_all("proof_01_skill_progress_half.png", "crop_01_skill_progress_half.png")
				var gs = root.get_node_or_null("GameState")
				if gs:
					# 設定熟練度滿 (30/30)
					gs.skill_data["slash"] = {"lv": 1, "mastery": 30}
				_dlg.call("_refresh_display")
				_step = 2
				_wait = 0

		2:
			# 等待 5 幀後拍攝 proof 2: 突破升階按鈕
			if _wait >= 5:
				_save_to_all("proof_02_skill_upgrade_button.png", "crop_02_skill_upgrade_button.png")
				var gs = root.get_node_or_null("GameState")
				if gs:
					# 設定滿級 (Lv.3)
					gs.skill_data["slash"] = {"lv": 3, "mastery": 0}
				_dlg.call("_refresh_display")
				_step = 3
				_wait = 0

		3:
			# 等待 5 幀後拍攝 proof 3: 滿級極階金色標籤
			if _wait >= 5:
				_save_to_all("proof_03_skill_max_tier_badge.png", "crop_03_skill_max_tier_badge.png")
				var loc = root.get_node_or_null("Loc")
				var gs = root.get_node_or_null("GameState")
				if gs:
					# 設定 slash 可突破升階，測試英文介面
					gs.skill_data["slash"] = {"lv": 1, "mastery": 30}
				if loc:
					loc.call("set_locale", "en")
				_dlg.call("_refresh_display")
				_step = 4
				_wait = 0

		4:
			# 等待 5 幀後拍攝 proof 4: 英文語系即時切換
			if _wait >= 5:
				_save_to_all("proof_04_skill_upgrade_en.png", "crop_04_skill_upgrade_en.png")
				var loc = root.get_node_or_null("Loc")
				if loc:
					loc.call("set_locale", "zh_TW")
				_dlg.call("_refresh_display")
				_step = 5
				_wait = 0

		5:
			# 滾動至【槍】區域以特寫『體悟習得』按鈕
			if _wait >= 5:
				var sb: ScrollContainer = _dlg.find_child("SkillScrollBox", true, false) as ScrollContainer
				if sb:
					sb.scroll_vertical = 480
					if sb.get_v_scroll_bar():
						sb.get_v_scroll_bar().value = 480
				_step = 6
				_wait = 0

		6:
			# 等待 5 幀後拍攝 proof 5: 體悟習得按鈕特寫
			if _wait >= 5:
				_save_to_all("proof_05_skill_unlock_button.png", "crop_05_skill_unlock_button.png")
				print("=== 實機截圖存證完成 ===")
				quit(0)
				return true
	return false
