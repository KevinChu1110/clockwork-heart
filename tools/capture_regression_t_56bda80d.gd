extends SceneTree
## PowerStatDialog 前往整頓快捷分支合進主線全面回歸驗收 (t_56bda80d)
## 執行指令：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_56bda80d.gd

const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_56bda80d"
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")
const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _dlg: Control = null
var _lobby: Control = null
var _opened_dlg: Control = null
var _hashes: Array[String] = []


func _initialize() -> void:
	print("== 開始執行 t_56bda80d 主線全面回歸驗收流程 ==")
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")

	if _gs != null:
		_gs.call("reset_new_game", "rabbit")
		_gs.gold = 1000
		_gs.energy = 15

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	print("  ✓ 環境初始化完成 (zh_TW, 1280x720)")


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 2:
		return false

	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			print("\n── 階段 1: 驗證 PowerStatDialog 前往整頓快捷雙按鈕結構與樣式 (zh_TW) ──")
			_dlg = PowerStatDialogScript.new()
			root.add_child(_dlg)
			_wait = 5
			_step = 1

		1:
			_verify_dialog_buttons()
			var p1 := OUT_DIR + "/proof_01_power_stat_shortcuts_zh_tw.png"
			_save_and_record_hash(p1)
			print("  ✓ [1/3] 已儲存 PowerStatDialog (zh_TW) 截圖: ", p1)

			# 切換至英文
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_dlg.call("_on_locale_changed", "en")
			_wait = 5
			_step = 2

		2:
			print("\n── 階段 2: 驗證英文 (en) 多語系文字與樣式 ──")
			var btn_go := _dlg.find_child("BtnGoEquip", true, false) as Button
			var btn_close := _dlg.find_child("BtnBottomClose", true, false) as Button
			assert(btn_go != null, "缺少 BtnGoEquip")
			assert(btn_close != null, "缺少 BtnBottomClose")
			assert(btn_go.text == "Gear Up", "英文前往整頓文字錯誤: %s" % btn_go.text)
			assert(btn_close.text in ["OK", "Confirm", "Close"], "英文確認/關閉文字錯誤: %s" % btn_close.text)
			print("  ✓ 英文多語系文字驗證通過 (Gear Up / %s)" % btn_close.text)

			var p2 := OUT_DIR + "/proof_02_power_stat_shortcuts_en.png"
			_save_and_record_hash(p2)
			print("  ✓ [2/3] 已儲存 PowerStatDialog (en) 截圖: ", p2)

			# 切回繁中並移除彈窗
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")
			_dlg.queue_free()
			_dlg = null
			_wait = 5
			_step = 3

		3:
			print("\n── 階段 3: 驗證大廳開啟 PowerStatDialog 與點擊『前往整頓』連動切換角色 Tab ──")
			_lobby = MobileLobbyScript.new()
			root.add_child(_lobby)
			_wait = 5
			_step = 4

		4:
			assert(int(_lobby.get("_current_tab")) == 0, "初始分頁應為主城 VILLAGE (0)")
			_opened_dlg = _lobby.call("open_power_stat_dialog") as Control
			assert(_opened_dlg != null, "大廳未能開啟 PowerStatDialog")
			_wait = 5
			_step = 5

		5:
			var btn_go2 := _opened_dlg.find_child("BtnGoEquip", true, false) as Button
			assert(btn_go2 != null, "大廳開啟之彈窗缺少 BtnGoEquip")
			print("  ✓ 模擬點擊『前往整頓』按鈕")
			btn_go2.pressed.emit()
			_wait = 6
			_step = 6

		6:
			assert(int(_lobby.get("_current_tab")) == 1, "點擊前往整頓後未切換至角色分頁 Tab.CHARACTER (1)，當前: %s" % str(_lobby.get("_current_tab")))
			print("  ✓ 大廳成功自動切換至角色裝備分頁 (Tab.CHARACTER)")

			var p3 := OUT_DIR + "/proof_03_lobby_char_tab_switched.png"
			_save_and_record_hash(p3)
			print("  ✓ [3/3] 已儲存大廳切換角色頁截圖: ", p3)

			_verify_all_hashes()

			print("\n==================================================")
			print("  REGRESSION_T_56BDA80D_OK: 全部主線回歸驗收測試通過！")
			print("==================================================")
			quit(0)
			return true

	return false


func _verify_dialog_buttons() -> void:
	var btn_go := _dlg.find_child("BtnGoEquip", true, false) as Button
	var btn_close := _dlg.find_child("BtnBottomClose", true, false) as Button
	assert(btn_go != null, "缺少前往整頓按鈕 BtnGoEquip")
	assert(btn_close != null, "缺少確定/關閉按鈕 BtnBottomClose")

	assert(btn_go.custom_minimum_size.x >= 48 and btn_go.custom_minimum_size.y >= 48, "BtnGoEquip 熱區必須 >= 48px")
	assert(btn_close.custom_minimum_size.x >= 48 and btn_close.custom_minimum_size.y >= 48, "BtnBottomClose 熱區必須 >= 48px")
	assert(btn_go.text == "前往整頓", "繁中前往整頓文字錯誤: %s" % btn_go.text)
	assert(btn_close.text in ["確定", "確認", "關閉"], "繁中確定/關閉文字錯誤: %s" % btn_close.text)

	_assert_no_emoji(_dlg)
	print("  ✓ 雙按鈕熱區 (140x48 >= 48px)、文案與零系統 Emoji 檢查通過")


func _assert_no_emoji(node: Node) -> void:
	for child in node.find_children("*", "Label", true, false):
		var text := (child as Label).text
		for ch in text:
			var code := ch.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
				if ch != "✕":
					assert(false, "UI 違規包含系統 Emoji: '%s' in %s" % [ch, (child as Label).name])
	for child in node.find_children("*", "Button", true, false):
		var text := (child as Button).text
		for ch in text:
			var code := ch.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
				if ch != "✕":
					assert(false, "按鈕違規包含系統 Emoji: '%s' in %s" % [ch, (child as Button).name])


func _save_and_record_hash(path: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	assert(tex != null, "無法取得 Viewport 紋理")
	var img := tex.get_image()
	assert(img != null and not img.is_empty(), "Viewport 截圖為空")

	# 檢查是否為純色黑屏
	var is_solid := true
	var p0 := img.get_pixel(0, 0)
	for sy in [60, 200, 360, 520, 660]:
		for sx in [60, 320, 640, 960, 1220]:
			if img.get_pixel(sx, sy) != p0:
				is_solid = false
				break
		if not is_solid:
			break
	assert(not is_solid, "截圖為純色無效畫面: %s" % path)

	var err := img.save_png(path)
	assert(err == OK, "儲存 PNG 失敗: %s" % path)

	var f := FileAccess.open(path, FileAccess.READ)
	assert(f != null, "無法讀取已儲存之 PNG: %s" % path)
	var bytes := f.get_buffer(f.get_length())
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(bytes)
	var digest := ctx.finish().hex_encode()
	_hashes.append(digest)
	print("    -> 存證截圖雜湊: ", digest)


func _verify_all_hashes() -> void:
	assert(_hashes.size() == 3, "應產生 3 張有效截圖，實際: %d" % _hashes.size())
	for i in range(_hashes.size()):
		for j in range(i + 1, _hashes.size()):
			assert(_hashes[i] != _hashes[j], "截圖雜湊不得重複: [%d] vs [%d] = %s" % [i, j, _hashes[i]])
	print("  ✓ 全部 3 張存證截圖 SHA256 驗證完成，互不相同無重複存證！")
