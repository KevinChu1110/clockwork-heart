extends SceneTree
## 《發條之心》武術館木人樁試招按鈕實機截圖工具 (t_655239f0)
## 產出：
## proof_02_skill_dummy_button.png: 武術館灰鬚指點招式面板底欄「前往木人樁試招」快捷鈕（已移除聚魂按鈕）

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_655239f0",
	"/opt/side/bravesoul-game/proofs",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_655239f0/proofs"
]

var _main: Node = null
var _wait: int = 0
var _step: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)

	print("=== 開始執行武術館木人樁試招按鈕實機截圖 (t_655239f0) ===")
	change_scene_to_file("res://scenes/main.tscn")


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
			if _wait < 20:
				return false
			_main = current_scene
			if _main == null or not _main.has_method("_go_skill_panel"):
				push_error("main scene 載入失敗或無 _go_skill_panel")
				quit(1)
				return false
			_main.call("_go_skill_panel")
			_step = 1
			_wait = 0
		1:
			if _wait < 8:
				return false
			# 滾動至底部展示「前往木人樁試招」快捷鈕
			var host: Control = _main.get("host")
			if host:
				var scrolls: Array[Node] = host.find_children("", "ScrollContainer", true, false)
				for sc in scrolls:
					if sc is ScrollContainer:
						(sc as ScrollContainer).scroll_vertical = 99999
			_step = 2
			_wait = 0
		2:
			if _wait < 10:
				return false
			await _save_to_all("proof_02_skill_dummy_button.png")
			print("\n=======================================================")
			print("  SKILL_DUMMY_BUTTON_CAPTURE_SUCCESS_OK")
			print("=======================================================")
			quit(0)
			return false
	return false
