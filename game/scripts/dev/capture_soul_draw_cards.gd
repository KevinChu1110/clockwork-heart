extends SceneTree
## 截圖：十連結果面板（固定種子），確認 10 張卡都是完整零件圖、框色只有五色。
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_soul_draw_cards.gd

const PoolScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_pool.gd")
const TenPullScript := preload("res://scripts/ui/soul_draw/soul_ten_pull_view.gd")

var _frame := 0
var _view: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_view = TenPullScript.new()
	root.add_child(_view)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 2:
		var pool = PoolScript.new()
		pool.setup(null, 20261006)
		var drops: Array[Dictionary] = []
		for i in 10:
			drops.append(pool.pull())
		_view.show_drops(drops)
	elif _frame == 120:
		var img := root.get_viewport().get_texture().get_image()
		var out := ProjectSettings.globalize_path("res://").path_join("../proofs/soul_draw/proof_soul_draw_ten_cards.png")
		if img != null:
			img.save_png(out)
			print("saved ", out)
		quit(0)
		return true
	return false
