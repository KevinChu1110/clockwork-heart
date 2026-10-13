extends SceneTree
## 手藝工坊一鍵合成實機截圖存證 (t_9a860b7a)
## 截取 5 張全景截圖：
## 1. proof_01_auto_fuse_disabled_empty.png (無可合成寶石，BtnAutoFuse 呈 disabled)
## 2. proof_02_auto_fuse_enabled_with_gems.png (注入達標寶石，BtnAutoFuse 啟用天藍色果凍厚底按鈕)
## 3. proof_03_auto_fuse_clicked_toast_success.png (點擊一鍵合成後，即時提示成功與刷新儲量)
## 4. proof_04_auto_fuse_en_quick_fuse.png (en 語系：Quick Fuse 即時連動)
## 5. proof_05_auto_fuse_ja_quick_fuse.png (ja 語系：一括合成 即時連動)

var _step := 0
var _wait := 0
var _main: Node = null
var _lobby: Node = null
var _dlg: Control = null
var _loc: Node = null

var OUT_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	OUT_DIR = base.path_join("../proofs/t_9a860b7a")
	DirAccess.make_dir_recursive_absolute(OUT_DIR)

	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行手藝工坊一鍵合成截圖存證腳本 (t_9a860b7a) ──")


func _save_shot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("  ! 無法取得截圖: ", filename)
		return
	var target_path := OUT_DIR.path_join(filename)
	var err := img.save_png(target_path)
	if err != OK:
		print("  ! 存圖失敗 err=%d: %s" % [err, target_path])
	else:
		print("  ✓ 成功存證截圖: %s (%dx%d)" % [target_path, img.get_width(), img.get_height()])


func _find_named(node: Node, target_name: String) -> Node:
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待大廳加載穩定
			if _wait >= 40:
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.set("level", 25)
					gs.set("gold", 8000)
					gs.set("gem_bag", [])
					gs.call("set_flag", "tut_done", true)
					gs.call("set_flag", "c1_entered_city", true)

				_loc = root.get_node_or_null("Loc")
				if _loc:
					_loc.call("set_locale", "zh_TW")

				_lobby = root.find_child("MobileLobby", true, false)
				if _lobby == null and _main != null:
					_lobby = _main.find_child("MobileLobby", true, false)

				if _lobby and _lobby.has_method("open_gem_workshop"):
					_dlg = _lobby.call("open_gem_workshop")
				else:
					var GemClass = load("res://scripts/ui/gem_workshop_dialog.gd")
					_dlg = GemClass.new()
					root.add_child(_dlg)

				_step = 1
				_wait = 0

		1:
			# 截圖 1: 空背包無可合成寶石，BtnAutoFuse disabled
			if _wait >= 25:
				_save_shot("proof_01_auto_fuse_disabled_empty.png")
				print("  [截圖 1] 完成：無寶石時按鈕 disabled")

				# 注入達標寶石：9 顆紅寶石 1 級、4 顆黃寶石 2 級、3 顆藍寶石 4 級
				var gem: Node = root.get_node_or_null("GemSystem")
				if gem:
					gem.call("add_gem", "red", 1, 9)
					gem.call("add_gem", "yellow", 2, 4)
					gem.call("add_gem", "blue", 4, 3)

				if _dlg and is_instance_valid(_dlg):
					_dlg.call("_refresh_smelt_view")

				_step = 2
				_wait = 0

		2:
			# 截圖 2: 注入寶石後，BtnAutoFuse 啟用天藍色立體果凍按鈕
			if _wait >= 25:
				_save_shot("proof_02_auto_fuse_enabled_with_gems.png")
				print("  [截圖 2] 完成：有寶石時按鈕啟用 (天藍色果凍厚底)")

				# 點擊一鍵合成
				var btn_auto := _find_named(_dlg, "BtnAutoFuse") as Button
				if btn_auto:
					btn_auto.pressed.emit()
				print("  >> 觸發一鍵合成...")

				_step = 3
				_wait = 0

		3:
			# 截圖 3: 一鍵合成完成，提示訊息與按鈕狀態更新
			if _wait >= 25:
				_save_shot("proof_03_auto_fuse_clicked_toast_success.png")
				print("  [截圖 3] 完成：一鍵合成成功提示與回退 disabled")

				# 切換至 en 語系
				if _loc:
					_loc.call("set_locale", "en")
				if _dlg and is_instance_valid(_dlg):
					_dlg.call("_on_locale_changed", "en")

				_step = 4
				_wait = 0

		4:
			# 截圖 4: en 語系 Quick Fuse
			if _wait >= 25:
				_save_shot("proof_04_auto_fuse_en_quick_fuse.png")
				print("  [截圖 4] 完成：en 語系 Quick Fuse")

				# 切換至 ja 語系
				if _loc:
					_loc.call("set_locale", "ja")
				if _dlg and is_instance_valid(_dlg):
					_dlg.call("_on_locale_changed", "ja")

				_step = 5
				_wait = 0

		5:
			# 截圖 5: ja 語系 一括合成
			if _wait >= 25:
				_save_shot("proof_05_auto_fuse_ja_quick_fuse.png")
				print("  [截圖 5] 完成：ja 語系 一括合成")

				# 還原回 zh_TW 並關閉彈窗
				if _loc:
					_loc.call("set_locale", "zh_TW")
				if _dlg and is_instance_valid(_dlg):
					_dlg.call("_on_close")

				_step = 6
				_wait = 0

		6:
			print("CAPTURE_GEM_AUTO_FUSE_OK")
			quit(0)
			return true

	return false
