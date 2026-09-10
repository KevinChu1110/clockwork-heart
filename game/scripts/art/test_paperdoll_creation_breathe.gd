extends SceneTree
## 《發條之心》開局選族創角角色預覽待機呼吸小動作測試 (Creation Preview Breathe)
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_creation_breathe.gd

const PaperdollSelectDemo = preload("res://scripts/ui/paperdoll_select_demo.gd")

var _ok := true
var _frame := 0


func _assert(cond: bool, msg: String) -> void:
	if cond:
		print("  ✓ %s" % msg)
	else:
		push_error("斷言失敗: %s" % msg)
		print("  ❌ 斷言失敗: %s" % msg)
		_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	match _frame:
		1:
			_run_test_suite()
			if _ok:
				print("\n=======================================================")
				print("PAPERDOLL_CREATION_BREATHE_OK")
				quit(0)
			else:
				push_error("PAPERDOLL_CREATION_BREATHE_FAIL")
				print("PAPERDOLL_CREATION_BREATHE_FAIL")
				quit(1)
			return true
	return false


func _run_test_suite() -> void:
	print("=== 開始開局選族創角預覽角色待機呼吸 (Creation Preview Breathe) 單元測試 ===")

	var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
	if demo_packed == null:
		push_error("無法載入 res://scenes/ui/paperdoll_select_demo.tscn")
		_ok = false
		return

	var demo: Node = demo_packed.instantiate()
	demo.set("creation_mode", true)
	root.add_child(demo)

	# 1. 測試初始化時呼吸動畫啟動
	var is_running: bool = bool(demo.call("is_breathe_running"))
	_assert(is_running, "PaperdollSelectDemo 開啟後預覽角色待機呼吸動畫正常啟動")

	var char_node: Node2D = demo.get("character") as Node2D
	_assert(char_node != null, "預覽角色 PaperdollCharacter 節點存在")

	# 2. 切換種族時呼吸不中斷
	var races := ["fox", "lion", "boar", "macaque", "rabbit"]
	for r in races:
		demo.call("select_race", r)
		var running_after_race: bool = bool(demo.call("is_breathe_running"))
		_assert(running_after_race, "切換至種族 '%s' 後呼吸動畫持續進行不中斷" % r)

	# 3. 換部件時呼吸不中斷
	demo.call("_on_costume_next_pressed")
	_assert(bool(demo.call("is_breathe_running")), "切換外裝後預覽角色呼吸動畫持續進行")

	demo.call("_on_chassis_next_pressed")
	_assert(bool(demo.call("is_breathe_running")), "切換塗裝後預覽角色呼吸動畫持續進行")

	demo.call("reset_to_default")
	_assert(bool(demo.call("is_breathe_running")), "重設為預設部件後預覽角色呼吸動畫持續進行")

	# 4. 關閉面板時呼吸 tween 確實停止且 scale 還原為 Vector2.ONE
	demo.call("close")
	var running_after_close: bool = bool(demo.call("is_breathe_running"))
	_assert(not running_after_close, "PaperdollSelectDemo 關閉時呼吸 tween 確實停止")
	if char_node:
		_assert(char_node.scale == Vector2.ONE, "呼吸停止後 character.scale 確實還原為 Vector2.ONE (1, 1)")

	print("=== 開局選族預覽待機呼吸單元測試完成 ===")
