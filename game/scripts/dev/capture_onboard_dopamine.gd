extends SceneTree
## 截取 W8 新手引導多巴胺畫面截圖（N01 初步畫面 與 N07 兩顆按鈕畫面）

var _frame: int = 0
var _view: Control = null
var _out_dir: String = ""
var _proof_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_proof_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/onboard_dopamine")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/onboard_w8/onboard_w8.tscn")

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 10:
		_view = current_scene as Control
	elif _frame == 15:
		# 截取 N01 畫面
		var tex: ViewportTexture = root.get_viewport().get_texture()
		var img: Image = tex.get_image() if tex else null
		if img:
			var p1 := _out_dir.path_join("proof_onboard_dopamine_n01.png")
			img.save_png(p1)
			var p2 := _proof_dir.path_join("proof_onboard_dopamine_n01.png")
			img.save_png(p2)
			print("SAVED_N01_PROOF: ", p1)
	elif _frame == 20:
		# 切換至 N07
		if _view:
			var flow = _view.get("flow")
			while flow != null and str(flow.current().get("node", "")) != "N07" and not flow.done:
				_view.call("_advance", false)
			print("ONBOARD_ADVANCED_TO_N07: node=", str(flow.current().get("node", "")))
	elif _frame == 30:
		# 截取 N07 畫面（含兩顆按鈕：下一步 ＋ 稍後再說）
		var tex: ViewportTexture = root.get_viewport().get_texture()
		var img: Image = tex.get_image() if tex else null
		if img:
			var p1 := _out_dir.path_join("proof_onboard_dopamine.png")
			img.save_png(p1)
			var p2 := _proof_dir.path_join("proof_onboard_dopamine.png")
			img.save_png(p2)
			var p3 := _out_dir.path_join("proof_onboard_dopamine_n07.png")
			img.save_png(p3)
			print("SAVED_N07_PROOF: ", p1, " & ", p3)
		else:
			print("NO_IMAGE_CAPTURED")
		print("ONBOARD_CAPTURE_OK")
		quit(0)
	return false
