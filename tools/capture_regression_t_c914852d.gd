extends SceneTree
## 《發條之心》大廳角色頁『招式 · 核心心法』入口按鈕連動 SkillDialog 實機截圖 (t_c914852d)
## 產出：
## 1. proof_01_lobby_character_skill_button.png: 角色頁左側按鈕區『招式 · 核心心法』多巴胺天藍果凍按鈕
## 2. proof_02_lobby_skill_dialog_popup.png: 點擊按鈕順暢開啟之 SkillDialog 彈窗與各流派招式檢視

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_c914852d",
	"/opt/side/bravesoul-game/proofs",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c914852d/proofs"
]

var _lobby: Control = null
var _wait: int = 0
var _step: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)

	print("=== 開始執行大廳角色頁招式心法按鈕實機截圖 (t_c914852d) ===")

	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")

	var sk = root.get_node_or_null("SkillSystem")
	if sk == null:
		var SkClass = load("res://scripts/systems/skill_system.gd")
		if SkClass:
			sk = SkClass.new()
			sk.name = "SkillSystem"
			root.add_child(sk)

	if loc:
		loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	_lobby.size = Vector2(1280, 720)
	root.add_child(_lobby)

func _save_to_all(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = root.get_viewport().get_texture().get_image()
	if img == null:
		push_error("無法取得 viewport image")
		return

	for dir_path in OUT_PATHS:
		var target := dir_path.path_join(filename)
		var err := img.save_png(target)
		if err == OK:
			print("  ✓ 成功儲存截圖: %s (%dx%d)" % [target, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存截圖失敗 err=%d: %s" % [err, target])

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 15:
				return false
			# 切換至角色頁
			_lobby._switch_tab(MobileLobbyScript.Tab.CHARACTER)
			_step = 1
			_wait = 0
		1:
			if _wait < 10:
				return false
			# 截圖 1: 角色頁
			_save_to_all("proof_01_lobby_character_skill_button.png")
			_step = 2
			_wait = 0
		2:
			if _wait < 5:
				return false
			# 點擊按鈕開啟 SkillDialog
			var btn: Button = _lobby.find_child("BtnSkillDialog", true, false) as Button
			if btn != null:
				btn.pressed.emit()
				print("  ok 已點擊 BtnSkillDialog")
			else:
				push_error("找不到 BtnSkillDialog 按鈕")
			_step = 3
			_wait = 0
		3:
			if _wait < 15:
				return false
			# 截圖 2: SkillDialog 彈窗
			_save_to_all("proof_02_lobby_skill_dialog_popup.png")
			_step = 4
			_wait = 0
		4:
			if _wait < 5:
				return false
			print("CAPTURE_ALL_SUCCESS")
			quit(0)
			return true
	return false
