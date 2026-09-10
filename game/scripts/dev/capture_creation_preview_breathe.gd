extends SceneTree
## 《發條之心》開局選族創角預覽待機呼吸實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_creation_preview_breathe.gd

const PaperdollSelectDemo = preload("res://scripts/ui/paperdoll_select_demo.gd")

var _out_dir: String = ""
var _time: float = 0.0
var _step: int = 0
var _demo: PaperdollSelectDemo = null
var _char: Node2D = null

var rabbit_scale_t0: Vector2 = Vector2.ZERO
var rabbit_scale_t1: Vector2 = Vector2.ZERO
var fox_scale_t0: Vector2 = Vector2.ZERO
var fox_scale_t1: Vector2 = Vector2.ZERO


func _initialize() -> void:
	print("=== 開始產生開局選族預覽角色待機呼吸實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/creation_breathe")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(base.path_join("../screenshots"))

	var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
	if demo_packed == null:
		push_error("無法載入 paperdoll_select_demo.tscn")
		quit(1)
		return

	_demo = demo_packed.instantiate() as PaperdollSelectDemo
	_demo.creation_mode = true
	root.add_child(_demo)

	_char = _demo.get("character") as Node2D
	_step = 1
	_time = 0.0


func _process(delta: float) -> bool:
	_time += delta

	match _step:
		1:
			# 等待首幀佈局與渲染穩定 (0.1s)
			if _time >= 0.1:
				if _char == null and _demo != null:
					_char = _demo.get("character") as Node2D
				if _char:
					print("  [Step 1] 選族面板開啟成功 (rabbit)，character global_pos=%s, scale=%s" % [str(_char.global_position), str(_char.scale)])
				_step = 2
				_time = 0.0
		2:
			# 等待呼吸 Tween 運行至波峰 1 (1.1s，scale 約 (1.03, 0.97))
			if _time >= 1.1:
				if _char:
					rabbit_scale_t0 = _char.scale
				_save_screenshot("proof_creation_breathe_rabbit_t0.png")
				print("  ✓ [Rabbit t0=1.1s] 截取兔族預覽呼吸波峰 1: scale=%s" % str(rabbit_scale_t0))
				_step = 3
				_time = 0.0
		3:
			# 再等待 1.1s (間隔 1.1s >= 1.0s)，運行至反向波峰 2 (scale 約 (0.98, 1.02))
			if _time >= 1.1:
				if _char:
					rabbit_scale_t1 = _char.scale
				_save_screenshot("proof_creation_breathe_rabbit_t1.png")
				print("  ✓ [Rabbit t1=2.2s] 截取兔族預覽呼吸波峰 2 (間隔 1.1s): scale=%s" % str(rabbit_scale_t1))

				# 切換至第二種族：靈尾狐 (fox)
				if _demo:
					_demo.select_race("fox")
					print("  [Step 3] 切換選取種族至靈尾狐 (fox)")

				_step = 4
				_time = 0.0
		4:
			# 切換種族後等待 1.1s，呼吸波峰 1 (呼吸未中斷)
			if _time >= 1.1:
				if _char:
					fox_scale_t0 = _char.scale
				_save_screenshot("proof_creation_breathe_fox_t0.png")
				print("  ✓ [Fox t0=1.1s] 截取狐族預覽呼吸波峰 1: scale=%s" % str(fox_scale_t0))
				_step = 5
				_time = 0.0
		5:
			# 再等待 1.1s (間隔 1.1s >= 1.0s)，呼吸波峰 2
			if _time >= 1.1:
				if _char:
					fox_scale_t1 = _char.scale
				_save_screenshot("proof_creation_breathe_fox_t1.png")
				print("  ✓ [Fox t1=2.2s] 截取狐族預覽呼吸波峰 2 (間隔 1.1s): scale=%s" % str(fox_scale_t1))

				# 關閉面板
				if _demo:
					_demo.close()
					print("  ✓ 呼叫 PaperdollSelectDemo.close() 關閉選角面板")

				print("=== 開局選族預覽呼吸實機截圖產生完成 ===")
				quit(0)
				return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  [截圖成功] -> %s" % file_path)
	else:
		push_error("截圖失敗: %s" % file_path)

	var base := ProjectSettings.globalize_path("res://")
	var sc_path := base.path_join("../screenshots").path_join(filename)
	img.save_png(sc_path)
