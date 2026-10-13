extends SceneTree
## 手藝工坊寶石櫃『一鍵卸下』實機 Viewport Texture Framebuffer 存證腳本
## (capture_gem_workshop_auto_unsocket_proofs.gd)
##
## 存證清單：
## 1. proof_01_case_tab_with_socketed_gems_zh_TW.png: 孔位已鑲嵌寶石，『一鍵卸下』珊瑚粉果凍按鈕亮起 (disabled=false)
## 2. proof_02_click_auto_unsocket_toast_and_empty_slots_zh_TW.png: 點擊卸下後，孔位清空、屬性歸零、飄字提示「已卸下 X 顆寶石並歸還背包！」、按鈕置灰
## 3. proof_03_no_gem_disabled_and_toast_zh_TW.png: 無寶石防呆點擊飄字提示「當前無已鑲嵌寶石！」
## 4. proof_04_gem_workshop_unsocket_en.png: 英文語系 (en) Quick Unsocket 按鈕與介面
## 5. proof_05_gem_workshop_unsocket_ja.png: 日文語系 (ja) 一括解除 按鈕與介面
## 6. proof_06_gem_workshop_unsocket_ko.png: 韓文語系 (ko) 일괄 해제 按鈕與介面
## 7. proof_07_gem_workshop_unsocket_es.png: 西班牙文語系 (es) Desengarzar Todo 按鈕與介面

var _step := 0
var _frame := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()
var _current_dlg: Node = null
var _gs: Node = null
var _loc: Node = null
var _gem: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_proof_dir = env_out
		else:
			_proof_dir = base.path_join(env_out)
	else:
		_proof_dir = base.path_join("../proofs/t_87339dc9")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	change_scene_to_file("res://scenes/main.tscn")


func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE_FAIL: null image for ", filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	print("CAPTURE_SAVED: ", out_path, " err=", err, " ", img.get_width(), "x", img.get_height())
	_saved.append(out_path)


func _find_named(node: Node, target_name: String) -> Node:
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame < 25:
				return false
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			_gem = root.get_node_or_null("GemSystem")

			if _gs:
				_gs.call("reset_new_game")
				_gs.set("level", 25)
				_gs.set("gold", 50000)
				_gs.set("equip_worn", {
					"w1": {
						"uid": "w1",
						"slot": "weapon",
						"name": "發條刺劍",
						"gem": {"color": "red", "level": 3}
					},
					"a1": {
						"uid": "a1",
						"slot": "armor",
						"name": "黃銅板甲",
						"gem": {"color": "yellow", "level": 2}
					}
				})
			if _loc:
				_loc.call("set_locale", "zh_TW")

			var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
			_current_dlg = GemWorkshopDialogScn.new()
			root.add_child(_current_dlg)

			# 切換到寶石櫃頁
			var tab_case := _find_named(_current_dlg, "TabCaseBtn") as Button
			if tab_case:
				tab_case.pressed.emit()

			_step = 1
			_frame = 0

		1:
			# 等待渲染並截圖 1: 穿戴有寶石，一鍵卸下亮起
			if _frame < 8:
				return false
			_save_frame("proof_01_case_tab_with_socketed_gems_zh_TW.png")

			# 點擊一鍵卸下
			var btn_unsocket := _find_named(_current_dlg, "BtnAutoUnsocket") as Button
			if btn_unsocket:
				btn_unsocket.pressed.emit()

			_step = 2
			_frame = 0

		2:
			# 等待渲染並截圖 2: 點擊卸下飄字與孔位清空
			if _frame < 5:
				return false
			_save_frame("proof_02_click_auto_unsocket_toast_and_empty_slots_zh_TW.png")

			# 再次觸發點擊驗證無寶石防呆飄字
			var btn_unsocket := _find_named(_current_dlg, "BtnAutoUnsocket") as Button
			if btn_unsocket:
				btn_unsocket.pressed.emit()

			_step = 3
			_frame = 0

		3:
			# 等待渲染並截圖 3: 無寶石防呆提示飄字
			if _frame < 5:
				return false
			_save_frame("proof_03_no_gem_disabled_and_toast_zh_TW.png")

			# 切換至英文 en
			if _loc:
				_loc.call("set_locale", "en")
			_step = 4
			_frame = 0

		4:
			# 截圖 4: 英文 en
			if _frame < 8:
				return false
			_save_frame("proof_04_gem_workshop_unsocket_en.png")

			# 切換至日文 ja
			if _loc:
				_loc.call("set_locale", "ja")
			_step = 5
			_frame = 0

		5:
			# 截圖 5: 日文 ja
			if _frame < 8:
				return false
			_save_frame("proof_05_gem_workshop_unsocket_ja.png")

			# 切換至韓文 ko
			if _loc:
				_loc.call("set_locale", "ko")
			_step = 6
			_frame = 0

		6:
			# 截圖 6: 韓文 ko
			if _frame < 8:
				return false
			_save_frame("proof_06_gem_workshop_unsocket_ko.png")

			# 切換至西班牙文 es
			if _loc:
				_loc.call("set_locale", "es")
			_step = 7
			_frame = 0

		7:
			# 截圖 7: 西班牙文 es
			if _frame < 8:
				return false
			_save_frame("proof_07_gem_workshop_unsocket_es.png")

			# 還原繁中
			if _loc:
				_loc.call("set_locale", "zh_TW")
			if _current_dlg and is_instance_valid(_current_dlg):
				_current_dlg.queue_free()

			print("CAPTURE_ALL_SUCCESS: 共產出 %d 張實機截圖" % _saved.size())
			quit(0)
			return true

	return false
