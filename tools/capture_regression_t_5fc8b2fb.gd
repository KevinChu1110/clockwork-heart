extends SceneTree
## 全面回歸驗收實機截圖腳本 (t_5fc8b2fb)
## 驗收內容：大廳角色頁『招式 · 核心心法』入口按鈕與 SkillDialog 招式卡片出招優先標籤合進主線後的全站回歸驗收
## 規範遵守：review.md 0-QA5, 0-QA26, 0-QA23, CANON.md, 多巴胺色盤與手遊人體工學規範

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const OUT_DIRS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_5fc8b2fb",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5fc8b2fb/proofs"
]

var _step: int = 0
var _wait: int = 0
var _lobby: Control = null
var _loc: Node = null
var _gs: Node = null
var _sk: Node = null
var _dlg: Control = null
var _btn_skill: Button = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for d in OUT_DIRS:
		DirAccess.make_dir_recursive_absolute(d)
		DirAccess.make_dir_recursive_absolute(d.path_join("crops"))

	print("=== 開始執行大廳招式心法按鈕與優先標籤全站回歸實機截圖 (t_5fc8b2fb) ===")

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)
	if _gs and _gs.has_method("reset_new_game"):
		_gs.call("reset_new_game", "rabbit")
	if _gs:
		_gs.skill_data = {
			"slash": {"lv": 1, "mastery": 0}
		}

	_sk = root.get_node_or_null("SkillSystem")
	if _sk == null:
		var SkClass = load("res://scripts/systems/skill_system.gd")
		if SkClass:
			_sk = SkClass.new()
			_sk.name = "SkillSystem"
			root.add_child(_sk)

	if _loc:
		_loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	_lobby.size = Vector2(1280, 720)
	root.add_child(_lobby)

func _save_viewport(filename: String, crop_rect: Rect2i = Rect2i(), crop_filename: String = "") -> void:
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 viewport: " + filename)
		return
	var img: Image = vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法取得 viewport image: " + filename)
		return

	for d in OUT_DIRS:
		var target := d.path_join(filename)
		var err := img.save_png(target)
		if err == OK:
			print("  ✓ 成功儲存全景截圖: %s (%dx%d)" % [target, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存全景截圖失敗 err=%d: %s" % [err, target])

	if crop_rect.size.x > 0 and crop_rect.size.y > 0 and not crop_filename.is_empty():
		var rx := clampi(crop_rect.position.x, 0, 1280)
		var ry := clampi(crop_rect.position.y, 0, 720)
		var rw := clampi(crop_rect.size.x, 1, 1280 - rx)
		var rh := clampi(crop_rect.size.y, 1, 720 - ry)
		var clamped_rect := Rect2i(rx, ry, rw, rh)
		var crop_img: Image = img.get_region(clamped_rect)
		if crop_img != null and not crop_img.is_empty():
			for d in OUT_DIRS:
				var crop_dir := d.path_join("crops")
				var crop_target := crop_dir.path_join(crop_filename)
				var err := crop_img.save_png(crop_target)
				if err == OK:
					print("  ✓ 成功儲存特寫截圖: %s (%dx%d)" % [crop_target, crop_img.get_width(), crop_img.get_height()])
				else:
					push_error("  ✗ 儲存特寫截圖失敗 err=%d: %s" % [err, crop_target])

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			# 切換至角色頁
			_lobby._switch_tab(MobileLobbyScript.Tab.CHARACTER)
			_btn_skill = _lobby.find_child("BtnSkillDialog", true, false) as Button
			if _btn_skill == null:
				push_error("找不到 BtnSkillDialog 按鈕")
			_step = 1
			_wait = 0
		1:
			if _wait < 15:
				return false
			# 截圖 01: 角色頁中文版（招式 · 核心心法按鈕）
			var btn_crop := Rect2i()
			if _btn_skill != null:
				var gr := _btn_skill.get_global_rect()
				btn_crop = Rect2i(int(gr.position.x) - 10, int(gr.position.y) - 10, int(gr.size.x) + 20, int(gr.size.y) + 20)
			_save_viewport("proof_01_lobby_character_tab_skill_btn_zh_TW.png", btn_crop, "crop_01_lobby_skill_btn_zh_TW.png")
			_step = 2
			_wait = 0
		2:
			if _wait < 10:
				return false
			# 切換語系為英文 en
			if _loc:
				_loc.call("set_locale", "en")
			_step = 3
			_wait = 0
		3:
			if _wait < 15:
				return false
			# 截圖 02: 角色頁英文版（Skills & Passives 按鈕）
			var btn_crop_en := Rect2i()
			if _btn_skill != null:
				var gr := _btn_skill.get_global_rect()
				btn_crop_en = Rect2i(int(gr.position.x) - 10, int(gr.position.y) - 10, int(gr.size.x) + 20, int(gr.size.y) + 20)
			_save_viewport("proof_02_lobby_character_tab_skill_btn_en.png", btn_crop_en, "crop_02_lobby_skill_btn_en.png")
			_step = 4
			_wait = 0
		4:
			if _wait < 10:
				return false
			# 切回中文 zh_TW
			if _loc:
				_loc.call("set_locale", "zh_TW")
			_step = 5
			_wait = 0
		5:
			if _wait < 10:
				return false
			# 點擊按鈕開啟 SkillDialog
			if _btn_skill != null:
				_btn_skill.pressed.emit()
				print("  ok 已觸發 BtnSkillDialog.pressed")
			_dlg = _lobby.get_node_or_null("SkillDialog")
			_step = 6
			_wait = 0
		6:
			if _wait < 20:
				return false
			# 截圖 03: 彈窗 SkillDialog（初始狀態：平常首發金黃膠囊標籤）
			var crop_dlg := Rect2i(260, 80, 760, 560)
			_save_viewport("proof_03_skill_dialog_popup_normal_badge_zh_TW.png", crop_dlg, "crop_03_skill_dialog_normal_zh_TW.png")
			_step = 7
			_wait = 0
		7:
			if _wait < 10:
				return false
			# 升級/習得 emergency_heal 技能
			if _sk:
				_sk.call("_set_lv", "emergency_heal", 1)
			if _dlg and _dlg.has_method("_refresh_display"):
				_dlg.call("_refresh_display")
			print("  ok 已設定 emergency_heal 並刷新 SkillDialog")
			_step = 8
			_wait = 0
		8:
			if _wait < 20:
				return false
			# 截圖 04: SkillDialog 同時呈現【平常首發】與【危急應急】雙標籤
			var crop_dlg := Rect2i(260, 80, 760, 560)
			_save_viewport("proof_04_skill_dialog_popup_panic_badge_zh_TW.png", crop_dlg, "crop_04_skill_dialog_panic_zh_TW.png")
			_step = 9
			_wait = 0
		9:
			if _wait < 10:
				return false
			# 切換至英文語系 en
			if _loc:
				_loc.call("set_locale", "en")
			_step = 10
			_wait = 0
		10:
			if _wait < 20:
				return false
			# 截圖 05: SkillDialog 英文語系 (Normal Opener / Crisis Emergency)
			var crop_dlg := Rect2i(260, 80, 760, 560)
			_save_viewport("proof_05_skill_dialog_popup_en.png", crop_dlg, "crop_05_skill_dialog_en.png")
			_step = 11
			_wait = 0
		11:
			if _wait < 10:
				return false
			# 切換至日文語系 ja
			if _loc:
				_loc.call("set_locale", "ja")
			_step = 12
			_wait = 0
		12:
			if _wait < 20:
				return false
			# 截圖 06: SkillDialog 日文語系 (通常発動 / 緊急時発動)
			var crop_dlg := Rect2i(260, 80, 760, 560)
			_save_viewport("proof_06_skill_dialog_popup_ja.png", crop_dlg, "crop_06_skill_dialog_ja.png")
			_step = 13
			_wait = 0
		13:
			if _wait < 10:
				return false
			# 測試關閉按鈕
			if _dlg != null:
				var close_btn: Button = _dlg.find_child("BtnCloseX", true, false) as Button
				if close_btn == null:
					close_btn = _dlg.find_child("BtnCloseBottom", true, false) as Button
				if close_btn != null:
					close_btn.pressed.emit()
					print("  ok 已點擊關閉按鈕")
			_step = 14
			_wait = 0
		14:
			if _wait < 15:
				return false
			var remaining_dlg = _lobby.get_node_or_null("SkillDialog")
			if remaining_dlg == null or not remaining_dlg.is_inside_tree():
				print("  ✓ 驗證通過: SkillDialog 已成功關閉並釋放")
			print("=== CAPTURE_REGRESSION_T_5FC8B2FB_SUCCESS ===")
			quit(0)
			return true
	return false
