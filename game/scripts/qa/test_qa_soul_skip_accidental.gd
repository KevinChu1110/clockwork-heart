extends SceneTree
## QA：抽魂演出「點畫面跳過」不能被誤觸（#93／PR #96）
## 量四種常見誤觸：連點抽卡的第二下（演出開始 1 幀內）、滑鼠滾輪、右鍵、只有放開沒有按下。
## 每種情境都重開一次演出，印出「有沒有被跳過」；誤觸會跳過就判 FAIL。
## 另外量：一般點擊（演出 0.5 秒後）一定要能跳過。
##
## ⚠️ 情境用「幀數」排時間，一定要用 --fixed-fps 60 跑（30 幀＝0.5 秒）；
## 不鎖幀的 headless 約 150fps，30 幀只有 0.2 秒，會撞到開場保護時間（#101 留言）。
## godot --path game --headless --fixed-fps 60 -s res://scripts/qa/test_qa_soul_skip_accidental.gd

const SoulSummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")

var _ok := true
var _fx: Control
var _done := 0
var _frame := 0
var _case := 0
var _armed := false
var _base_done := 0

## [名稱, 演出開始後第幾幀送, 事件種類, 是否算誤觸（true＝不該跳過）]
const CASES := [
	["連點：演出開始後第 1 幀左鍵", 1, "left", true],
	["滑鼠滾輪往下", 30, "wheel", true],
	["右鍵", 30, "right", true],
	["只有放開（上一下的 release）", 1, "release", true],
	["演出 0.5 秒後正常點畫面", 30, "left", false],
]


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	root.size = Vector2i(1280, 720)
	_fx = SoulSummonFx.new()
	root.add_child(_fx)


func _on_done() -> void:
	_done += 1


func _send(kind: String) -> void:
	var pos := Vector2(640, 420)
	var evs: Array = []
	match kind:
		"left", "right":
			for p in [true, false]:
				var e := InputEventMouseButton.new()
				e.button_index = MOUSE_BUTTON_LEFT if kind == "left" else MOUSE_BUTTON_RIGHT
				e.pressed = p
				evs.append(e)
		"wheel":
			for p in [true, false]:
				var e := InputEventMouseButton.new()
				e.button_index = MOUSE_BUTTON_WHEEL_DOWN
				e.pressed = p
				e.factor = 1.0
				evs.append(e)
		"release":
			var e := InputEventMouseButton.new()
			e.button_index = MOUSE_BUTTON_LEFT
			e.pressed = false
			evs.append(e)
	for e in evs:
		e.position = pos
		e.global_position = pos
		root.push_input(e, true)


func _process(_d: float) -> bool:
	_frame += 1
	if _case >= CASES.size():
		print("QA_SOUL_SKIP_ACCIDENTAL_OK" if _ok else "QA_SOUL_SKIP_ACCIDENTAL_FAIL")
		quit(0 if _ok else 1)
		return true
	var c: Array = CASES[_case]
	if not _armed:
		if _frame < 5:
			return false
		_base_done = _done
		_fx.call("play_summon", false, _on_done)
		_armed = true
		_frame = 0
		return false
	if _frame == int(c[1]):
		_send(str(c[2]))
	elif _frame == int(c[1]) + 4:
		var skipped: bool = _done > _base_done
		var accidental: bool = c[3]
		print("  %s → %s" % [c[0], "被跳過" if skipped else "沒跳過"])
		if accidental and skipped:
			_fail("誤觸會跳過演出：%s" % c[0])
		if not accidental and not skipped:
			_fail("正常點畫面沒有跳過：%s" % c[0])
		if not skipped:
			_fx.call("skip")
		_case += 1
		_armed = false
		_frame = 0
	return false
