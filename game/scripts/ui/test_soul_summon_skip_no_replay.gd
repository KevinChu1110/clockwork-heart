extends SceneTree
## （#96 迴歸；QA 在 #98 重驗發現跳過後約 1.5 秒翻卡音重播）
## 抽魂演出跳過後，不能在原本的收尾時間再結束一次（callback 再叫一次 → 翻卡音又響一次）。
## 單抽與十連各跑一次：開演 0.3 秒後跳過，再等過整段演出的長度，callback 只能被叫 1 次。

const SummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")
const SKIP_AT := 0.3
const WAIT_AFTER := 3.0

var _ok := true
var _fx: Control
var _calls := 0
var _phase := 0
var _t := 0.0
var _is_ten := false


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	_fx = SummonFx.new()
	root.add_child(_fx)


func _on_done() -> void:
	_calls += 1


func _process(delta: float) -> bool:
	_t += delta
	match _phase:
		0:
			if _t > 0.1:
				_calls = 0
				_fx.call("play_summon", _is_ten, _on_done)
				_t = 0.0
				_phase = 1
		1:
			if _t >= SKIP_AT:
				_fx.call("skip")
				if _calls != 1:
					_fail("跳過當下 callback 應叫 1 次，實際 %d" % _calls)
				_t = 0.0
				_phase = 2
		2:
			if _t >= WAIT_AFTER:
				var label := "十連" if _is_ten else "單抽"
				if _calls != 1:
					_fail("%s：跳過後又結束了一次（callback 共 %d 次 → 翻卡音重播）" % [label, _calls])
				else:
					print("  ok %s：跳過後 %.1f 秒內 callback 只叫 1 次" % [label, WAIT_AFTER])
				if _is_ten:
					print("TEST_SOUL_SUMMON_SKIP_NO_REPLAY_OK" if _ok else "TEST_SOUL_SUMMON_SKIP_NO_REPLAY_FAIL")
					quit(0 if _ok else 1)
					return true
				_is_ten = true
				_t = 0.0
				_phase = 0
	return false
