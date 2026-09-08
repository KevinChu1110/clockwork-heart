extends SceneTree
## 擷取發條能量原型介面截圖：
## godot --path game --headless -s res://scripts/dev/capture_clockwork_energy.gd

const ClockworkEnergyView = preload("res://scripts/ui/clockwork_energy_view.gd")

var _frame: int = 0
var _view: Control = null
var _out_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_view = ClockworkEnergyView.new()
	root.add_child(_view)


func _process(_delta: float) -> bool:
	_frame += 1

	if _frame == 2:
		## 模擬充能觸發倒數分配視窗
		_view.sim.shared_energy = 55.0
		_view.sim.update(0.1)
		_view.sim.allocation_countdown = 2.8  ## 展示倒數中的視覺狀態
		_view.call("_refresh_all")
	elif _frame == 4:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_clockwork_energy.png")
			img.save_png(p)
			print("SAVED_CLOCKWORK_ENERGY: ", p)
		print("CLOCKWORK_ENERGY_CAPTURE_OK")
		quit(0)

	return false
