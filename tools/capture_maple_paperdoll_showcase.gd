extends SceneTree
## 發條白兔 楓之谷骨骼錨點展示場景實機 Framebuffer 截圖捕獲腳本
## 執行方式：xvfb-run godot --path game -s res://../tools/capture_maple_paperdoll_showcase.gd

const SCENE_PATH := "res://scenes/art/maple_paperdoll_showcase.tscn"
const OUT_PATH := "res://assets/sprites/player/paperdoll/rabbit/proof_maple_white_rabbit_showcase_viewport.png"


func _initialize() -> void:
	print("=== 開始捕捉 Maple Paperdoll 展示場景實機截圖 (xvfb-run) ===")
	var packed: PackedScene = load(SCENE_PATH)
	if packed == null:
		push_error("無法載入展示場景: %s" % SCENE_PATH)
		quit(1)
		return

	var scene: Node = packed.instantiate()
	root.add_child(scene)

	# 等待至少 15 幀確保 SubViewport、Font、Shader 與 Control 完整繪製排版
	for i in range(25):
		await process_frame

	var img := root.get_viewport().get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法取得 Viewport 影像！")
		quit(1)
		return

	var abs_path := ProjectSettings.globalize_path(OUT_PATH)
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("儲存截圖失敗: %d" % err)
		quit(1)
		return

	print("✓ 成功捕捉實機 Framebuffer 截圖: %s (尺寸: %s)" % [abs_path, str(img.get_size())])
	quit(0)
