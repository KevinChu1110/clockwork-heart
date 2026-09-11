extends SceneTree

var _frame: int = 0
var _start_time: float = 0.0

func _initialize() -> void:
	Engine.max_fps = 30
	_start_time = Time.get_ticks_msec() / 1000.0
	print("Engine.max_fps set to 30. Start time: ", _start_time)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame % 30 == 0:
		var now: float = Time.get_ticks_msec() / 1000.0
		print("Frame: ", _frame, " Elapsed: ", now - _start_time, " delta: ", _delta)
	if _frame >= 90:
		var total: float = (Time.get_ticks_msec() / 1000.0) - _start_time
		print("Finished 90 frames in ", total, " seconds")
		quit(0)
	return false
