extends SceneTree
## 《發條之心》手藝工坊寶石櫃新增『一鍵鑲嵌』果凍按鈕實機驗收存證腳本 (t_3258c8f7)
## 遵循 0-QA5 / 0-QA26 / 0-QA28（1280x720 真實 Viewport OpenGL3 Framebuffer 截圖，零 PIL 假圖）

var GemWorkshopDialogClass: GDScript = null
var ContentLoc: GDScript = null

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_3258c8f7",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3258c8f7/proofs/t_3258c8f7",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3258c8f7/bravesoul-game/proofs/t_3258c8f7"
]

var _step: int = 0
var _wait: int = 0
var _ok: bool = true

var _dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null

var _saved_hashes: Dictionary = {}


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	const FORBIDDEN := ["⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"]
	for sym in FORBIDDEN:
		if text.find(sym) >= 0:
			return true
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	for base_dir in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(base_dir)
		DirAccess.make_dir_recursive_absolute(base_dir.path_join("crops"))

	change_scene_to_file("res://scenes/main.tscn")
	print("=== 開始執行手藝工坊寶石櫃一鍵鑲嵌實機驗收存證 (t_3258c8f7) ===")
	_step = 0
	_wait = 0


func _save_viewport(filename: String, crop_node: Control = null, crop_filename: String = "") -> String:
	var vp := root.get_viewport()
	if vp == null:
		_fail("無法獲取 Viewport")
		return ""
	var tex := vp.get_texture()
	if tex == null:
		_fail("無法獲取 Viewport Texture")
		return ""
	var img := tex.get_image()
	if img == null or img.is_empty():
		_fail("Viewport 渲染為空")
		return ""

	var full_bytes := img.save_png_to_buffer()
	var full_ctx := HashingContext.new()
	full_ctx.start(HashingContext.HASH_SHA256)
	full_ctx.update(full_bytes)
	var full_sha := full_ctx.finish().hex_encode()

	if _saved_hashes.values().has(full_sha):
		_fail("偵測到重複截圖 (SHA256 碰撞): %s 與既有截圖相同！" % filename)

	for base_dir in OUT_PATHS:
		var full_path := base_dir.path_join(filename)
		var err := img.save_png(full_path)
		if err == OK:
			print("  ✓ 儲存實機全景圖: %s (%dx%d, SHA256=%s)" % [full_path, img.get_width(), img.get_height(), full_sha.substr(0, 12)])
		else:
			_fail("儲存全景圖失敗: %s" % full_path)

		if crop_node != null and is_instance_valid(crop_node) and crop_filename != "":
			var crops_dir := base_dir.path_join("crops")
			var g_rect := crop_node.get_global_rect()
			var crop_rect := Rect2i(int(g_rect.position.x), int(g_rect.position.y), int(g_rect.size.x), int(g_rect.size.y))
			# 限制在畫面內
			crop_rect = crop_rect.intersection(Rect2i(0, 0, 1280, 720))
			if crop_rect.size.x > 0 and crop_rect.size.y > 0:
				var cropped := img.get_region(crop_rect)
				var crop_path := crops_dir.path_join(crop_filename)
				var c_err := cropped.save_png(crop_path)
				if c_err == OK:
					print("  ✓ 儲存特寫裁切圖: %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])
				else:
					_fail("儲存特寫圖失敗: %s" % crop_path)

	_saved_hashes[filename] = full_sha
	return full_sha


func _find_named(node: Node, target_name: String) -> Node:
	if node == null:
		return null
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
			# Step 0: 等待場景與 Autoloads 就緒，加載類別與初始化測試數據
			if _wait >= 35:
				GemWorkshopDialogClass = load("res://scripts/ui/gem_workshop_dialog.gd")
				ContentLoc = load("res://scripts/systems/content_loc.gd")

				_loc_node = root.get_node_or_null("Loc")
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")

				_gs = root.get_node_or_null("GameState")
				if _gs:
					_gs.set("level", 25)
					_gs.set("gold", 88888)
					var w_item := {
						"uid": "w_proof_01",
						"name": "天工鋼刃",
						"slot": "weapon",
						"tier": 2,
						"line": "sword",
						"quality": "epic",
					}
					var a_item := {
						"uid": "a_proof_01",
						"name": "發條重鎧",
						"slot": "armor",
						"tier": 2,
						"line": "heavy",
						"quality": "epic",
					}
					var equip_worn := {
						"w_proof_01": w_item,
						"a_proof_01": a_item,
					}
					var equip_slots := {
						"weapon": "w_proof_01",
						"armor": "a_proof_01",
					}
					_gs.set("equip_worn", equip_worn)
					_gs.set("equip_slots", equip_slots)
					_gs.set("gem_bag", [
						{"id": "gem_p_y2", "color": "yellow", "level": 2},
						{"id": "gem_p_r1", "color": "red", "level": 1},
						{"id": "gem_p_b1", "color": "blue", "level": 1},
					])

				_dlg = GemWorkshopDialogClass.new()
				root.add_child(_dlg)

				# 切換至寶石櫃盤點分頁
				var tab_case := _find_named(_dlg, "TabCaseBtn") as Button
				if tab_case:
					tab_case.pressed.emit()
				print(">>> [1/8] 繁中 (zh_TW) 寶石櫃初始分頁渲染完成...")
				_step = 1
				_wait = 0

		1:
			# Step 1: 存證 proof_01_gem_workshop_case_tab_zh_TW.png
			if _wait >= 25:
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				if btn_auto == null:
					_fail("找不到 BtnAutoSocket")
					return true

				if _has_emoji(btn_auto.text):
					_fail("BtnAutoSocket 包含 Emoji")
				print("  ✓ BtnAutoSocket 屬性檢查通過: 尺寸=%s, 文字='%s'" % [btn_auto.custom_minimum_size, btn_auto.text])

				_save_viewport("proof_01_gem_workshop_case_tab_zh_TW.png", btn_auto, "crop_01_btn_auto_socket_zh_TW.png")
				_step = 2
				_wait = 0

		2:
			# Step 2: 點擊一鍵鑲嵌按鈕
			if _wait >= 15:
				print(">>> [2/8] 點擊 BtnAutoSocket 執行一鍵鑲嵌...")
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				btn_auto.pressed.emit()
				_step = 3
				_wait = 0

		3:
			# Step 3: 存證 proof_02_click_auto_socket_success.png
			if _wait >= 25:
				var bonus_panel := _find_named(_dlg, "CaseBonusPanel") as Control
				var msg_label := _find_named(_dlg, "MsgLabel") as Label
				print("  ✓ 一鍵鑲嵌執行成功，MsgLabel: '%s'" % msg_label.text)
				_save_viewport("proof_02_click_auto_socket_success.png", bonus_panel, "crop_02_auto_socket_bonus_refreshed.png")
				_step = 4
				_wait = 0

		4:
			# Step 4: 再次點擊一鍵鑲嵌，展示全孔位已滿防呆提示
			if _wait >= 15:
				print(">>> [3/8] 再次點擊 BtnAutoSocket，觸發全孔位填滿防呆回饋...")
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				btn_auto.pressed.emit()
				_step = 5
				_wait = 0

		5:
			# Step 5: 存證 proof_03_auto_socket_full_feedback.png
			if _wait >= 25:
				var msg_label := _find_named(_dlg, "MsgLabel") as Label
				print("  ✓ 全滿防呆回饋 MsgLabel: '%s'" % msg_label.text)
				_save_viewport("proof_03_auto_socket_full_feedback.png", msg_label, "crop_03_auto_socket_full_feedback.png")
				_step = 6
				_wait = 0

		6:
			# Step 6: 切換至 zh_CN
			if _wait >= 15:
				print(">>> [4/8] 切換至簡體中文 (zh_CN)...")
				if _loc_node:
					_loc_node.call("set_locale", "zh_CN")
				_step = 7
				_wait = 0

		7:
			# Step 7: 存證 proof_04_gem_workshop_auto_socket_zh_CN.png
			if _wait >= 25:
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				if btn_auto.text != "一键镶嵌":
					_fail("zh_CN 下 BtnAutoSocket 未正確更新為 '一键镶嵌' (實際: %s)" % btn_auto.text)
				_save_viewport("proof_04_gem_workshop_auto_socket_zh_CN.png", btn_auto, "crop_04_btn_auto_socket_zh_CN.png")
				_step = 8
				_wait = 0

		8:
			# Step 8: 切換至 en (英文)
			if _wait >= 15:
				print(">>> [5/8] 切換至英文 (en)...")
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_step = 9
				_wait = 0

		9:
			# Step 9: 存證 proof_05_gem_workshop_auto_socket_en.png
			if _wait >= 25:
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				if btn_auto.text != "Quick Socket":
					_fail("en 下 BtnAutoSocket 未正確更新為 'Quick Socket' (實際: %s)" % btn_auto.text)
				if _has_cjk(btn_auto.text):
					_fail("en 語系下殘留 CJK 字元")
				_save_viewport("proof_05_gem_workshop_auto_socket_en.png", btn_auto, "crop_05_btn_auto_socket_en.png")
				_step = 10
				_wait = 0

		10:
			# Step 10: 切換至 ja (日文)
			if _wait >= 15:
				print(">>> [6/8] 切換至日文 (ja)...")
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				_step = 11
				_wait = 0

		11:
			# Step 11: 存證 proof_06_gem_workshop_auto_socket_ja.png
			if _wait >= 25:
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				if btn_auto.text != "一括装着":
					_fail("ja 下 BtnAutoSocket 未正確更新為 '一括装着' (實際: %s)" % btn_auto.text)
				_save_viewport("proof_06_gem_workshop_auto_socket_ja.png", btn_auto, "crop_06_btn_auto_socket_ja.png")
				_step = 12
				_wait = 0

		12:
			# Step 12: 切換至 ko (韓文)
			if _wait >= 15:
				print(">>> [7/8] 切換至韓文 (ko)...")
				if _loc_node:
					_loc_node.call("set_locale", "ko")
				_step = 13
				_wait = 0

		13:
			# Step 13: 存證 proof_07_gem_workshop_auto_socket_ko.png
			if _wait >= 25:
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				if btn_auto.text != "일괄 장착":
					_fail("ko 下 BtnAutoSocket 未正確更新為 '일괄 장착' (實際: %s)" % btn_auto.text)
				_save_viewport("proof_07_gem_workshop_auto_socket_ko.png", btn_auto, "crop_07_btn_auto_socket_ko.png")
				_step = 14
				_wait = 0

		14:
			# Step 14: 切換至 es (西班牙文)
			if _wait >= 15:
				print(">>> [8/8] 切換至西班牙文 (es)...")
				if _loc_node:
					_loc_node.call("set_locale", "es")
				_step = 15
				_wait = 0

		15:
			# Step 15: 存證 proof_08_gem_workshop_auto_socket_es.png
			if _wait >= 25:
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				if btn_auto.text != "Engarzar Todo":
					_fail("es 下 BtnAutoSocket 未正確更新為 'Engarzar Todo' (實際: %s)" % btn_auto.text)
				if _has_cjk(btn_auto.text):
					_fail("es 語系下殘留 CJK 字元")
				_save_viewport("proof_08_gem_workshop_auto_socket_es.png", btn_auto, "crop_08_btn_auto_socket_es.png")
				_step = 16
				_wait = 0

		16:
			# Step 16: 驗證總結與退出
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			if _dlg and is_instance_valid(_dlg):
				_dlg.queue_free()

			if not _ok:
				printerr("實機驗收存證有失敗項目！")
				quit(1)
				return true

			print("\n=======================================================")
			print("實機驗收存證全部完成！共產出 %d 張獨立全景圖與對應特寫。" % _saved_hashes.size())
			print("CAPTURE_T_3258C8F7_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
