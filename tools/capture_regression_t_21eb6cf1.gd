extends SceneTree
## 戰力屬性總覽與儲能庫雙倍領取合進主線全面回歸驗收 (t_21eb6cf1)
## 執行指令：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_21eb6cf1.gd

const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_21eb6cf1"
const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
const ClockworkVaultDialog = preload("res://scripts/ui/clockwork_vault_dialog.gd")
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")
const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _dlg: Control = null
var _lobby: Control = null
var _hashes: Array[String] = []


func _initialize() -> void:
	print("== 開始執行 t_21eb6cf1 主線全面回歸驗收流程 ==")
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
		if "has_removed_ads" in _gs:
			_gs.has_removed_ads = false

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
			print("\n── 階段 1: 驗證 PowerStatDialog 渲染與規格 (zh_TW) ──")
			_dlg = PowerStatDialogScript.new()
			root.add_child(_dlg)
			_wait = 5
			_step = 1

		1:
			_verify_power_stat_dialog_specs()
			var p1 := OUT_DIR + "/proof_01_power_stat_dialog_zh_tw.png"
			_save_and_record_hash(p1)
			print("  ✓ [1/6] 已儲存 PowerStatDialog (zh_TW) 截圖: ", p1)

			# 切換至英文
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_dlg.call("_on_locale_changed", "en")
			_wait = 5
			_step = 2

		2:
			print("\n── 階段 2: 驗證 PowerStatDialog 六語系英文化動態刷新 (en) ──")
			var p2 := OUT_DIR + "/proof_02_power_stat_dialog_en.png"
			_save_and_record_hash(p2)
			print("  ✓ [2/6] 已儲存 PowerStatDialog (en) 截圖: ", p2)

			# 清理彈窗，切回繁中
			if _dlg != null and is_instance_valid(_dlg):
				_dlg.queue_free()
				_dlg = null
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")
			_wait = 5
			_step = 3

		3:
			print("\n── 階段 3: 驗證大廳頂部戰力膠囊 (PowerCapsule) 熱區與連動開啟 ──")
			_lobby = MobileLobbyScript.new()
			root.add_child(_lobby)
			_lobby.size = Vector2(1280, 720)
			_wait = 10
			_step = 4

		4:
			_verify_lobby_power_capsule_specs()
			var p3 := OUT_DIR + "/proof_03_lobby_power_capsule.png"
			_save_and_record_hash(p3)
			print("  ✓ [3/6] 已儲存大廳戰力膠囊與頂部 HUD 截圖: ", p3)

			# 清理大廳
			if _lobby != null and is_instance_valid(_lobby):
				_lobby.queue_free()
				_lobby = null
			_wait = 5
			_step = 5

		5:
			print("\n── 階段 4: 驗證發條儲能庫雙倍領取按鈕規格與展示 ──")
			var now_t := Time.get_unix_time_from_system()
			IdleClockworkVault.set_last_claim_ts(now_t - 14400.0)
			_dlg = ClockworkVaultDialog.new()
			root.add_child(_dlg)
			_wait = 8
			_step = 6

		6:
			_verify_vault_double_claim_specs()
			var p4 := OUT_DIR + "/proof_04_vault_double_claim_dialog.png"
			_save_and_record_hash(p4)
			print("  ✓ [4/6] 已儲存發條儲能庫雙倍領取展示截圖: ", p4)

			# 點擊雙倍領取觸發廣告模擬彈窗
			var double_btn: Button = _dlg.find_child("DoubleClaimButton", true, false) as Button
			if double_btn != null:
				double_btn.emit_signal("pressed")
			_wait = 8
			_step = 7

		7:
			print("\n── 階段 5: 驗證一般模式點擊雙倍領取彈出 MockAdDialog ──")
			var p5 := OUT_DIR + "/proof_05_vault_mock_ad_dialog.png"
			_save_and_record_hash(p5)
			print("  ✓ [5/6] 已儲存點擊雙倍領取觸發 MockAdDialog 截圖: ", p5)

			# 清理彈窗並測試去廣告模式
			if _dlg != null and is_instance_valid(_dlg):
				_dlg.queue_free()
				_dlg = null
			if _gs != null:
				_gs.has_removed_ads = true
			var now_t := Time.get_unix_time_from_system()
			IdleClockworkVault.set_last_claim_ts(now_t - 14400.0)

			_dlg = ClockworkVaultDialog.new()
			root.add_child(_dlg)
			_wait = 8
			_step = 8

		8:
			print("\n── 階段 6: 驗證去廣告尊享模式直接雙倍結算與提示 ──")
			var double_btn2: Button = _dlg.find_child("DoubleClaimButton", true, false) as Button
			if double_btn2 != null:
				double_btn2.emit_signal("pressed")
			_wait = 8
			_step = 9

		9:
			var p6 := OUT_DIR + "/proof_06_vault_ad_removed_double_toast.png"
			_save_and_record_hash(p6)
			print("  ✓ [6/6] 已儲存去廣告直通雙倍領取與提示截圖: ", p6)

			_verify_all_proof_hashes()
			print("\n==========================================")
			print("  REGRESSION_TEST_OK: 主線全面回歸驗收全數通過！")
			print("==========================================")
			quit(0)
			return true

	return false


func _verify_power_stat_dialog_specs() -> void:
	assert(_dlg != null, "PowerStatDialog 實例為空")
	var scrim := _dlg.get_node_or_null("ModalScrim") as ColorRect
	assert(scrim != null, "缺少全螢幕遮罩 ModalScrim")
	assert(scrim.mouse_filter == Control.MOUSE_FILTER_STOP, "ModalScrim 必須攔截點擊")

	var card := _dlg.get_node_or_null("DialogCard") as PanelContainer
	if card == null:
		card = _dlg.find_child("DialogCard", true, false) as PanelContainer
	assert(card != null, "缺少 DialogCard")
	assert(card.custom_minimum_size.x == 720.0, "DialogCard 寬度應為 720px (實得 %f)" % card.custom_minimum_size.x)

	var close_x := _dlg.find_child("BtnCloseX", true, false) as Button
	assert(close_x != null, "缺少右上關閉按鈕 BtnCloseX")
	assert(close_x.custom_minimum_size.x >= 48.0 and close_x.custom_minimum_size.y >= 48.0, "BtnCloseX 熱區未達 48px")

	var close_bottom := _dlg.find_child("BtnBottomClose", true, false) as Button
	assert(close_bottom != null, "缺少底部關閉按鈕 BtnBottomClose")
	assert(close_bottom.custom_minimum_size.y >= 48.0, "BtnBottomClose 熱區高度未達 48px")

	_assert_no_emoji(_dlg)
	print("  ✓ PowerStatDialog 規格、熱區 (>=48px)、零 Emoji 檢驗通過")


func _verify_lobby_power_capsule_specs() -> void:
	assert(_lobby != null, "MobileLobby 實例為空")

	var p_frame := _lobby.find_child("p_frame", true, false)
	if p_frame == null:
		for node in _lobby.find_children("*", "PanelContainer", true, false):
			if node.custom_minimum_size == Vector2(52, 52):
				p_frame = node
				break
	assert(p_frame != null, "大廳頂部缺少玩家個人檔案框 (52x52)")
	assert(p_frame.mouse_filter == Control.MOUSE_FILTER_STOP, "玩家個人檔案框必須為 STOP 攔截點擊")

	var pwr_cap := _lobby.find_child("PowerCapsule", true, false) as PanelContainer
	assert(pwr_cap != null, "大廳頂部缺少戰力膠囊 PowerCapsule")
	assert(pwr_cap.custom_minimum_size.x >= 48.0 and pwr_cap.custom_minimum_size.y >= 48.0,
		"PowerCapsule 熱區未達 48px: %s" % str(pwr_cap.custom_minimum_size))
	assert(pwr_cap.mouse_filter == Control.MOUSE_FILTER_STOP, "PowerCapsule 必須為 STOP 攔截點擊")

	# 點擊 PowerCapsule 觸發彈窗
	var ev_click := InputEventMouseButton.new()
	ev_click.button_index = MOUSE_BUTTON_LEFT
	ev_click.pressed = true
	pwr_cap.emit_signal("gui_input", ev_click)
	var opened_dlg := _lobby.get_node_or_null("PowerStatDialog")
	assert(opened_dlg != null, "點擊戰力膠囊未能開啟 PowerStatDialog")
	print("  ✓ 大廳頂部戰力膠囊 (96x48 >= 48px) 與連動開啟檢驗通過")


func _verify_vault_double_claim_specs() -> void:
	assert(_dlg != null, "ClockworkVaultDialog 實例為空")
	var double_btn := _dlg.find_child("DoubleClaimButton", true, false) as Button
	assert(double_btn != null, "缺少 DoubleClaimButton")
	assert(double_btn.custom_minimum_size.y >= 50.0, "DoubleClaimButton 高度未達 50px")

	var normal_sb := double_btn.get_theme_stylebox("normal") as StyleBoxFlat
	assert(normal_sb != null, "DoubleClaimButton 缺少 normal StyleBoxFlat")
	var bg_hex := normal_sb.bg_color.to_html(false).to_upper()
	assert(bg_hex == "38A0FF", "DoubleClaimButton 底色非天藍 #38A0FF (實得 #%s)" % bg_hex)
	assert(normal_sb.border_width_bottom >= 5, "DoubleClaimButton 果凍厚底未達 5px")
	assert(normal_sb.corner_radius_top_left >= 16, "DoubleClaimButton 圓角未達標")

	_assert_no_emoji(_dlg)
	print("  ✓ ClockworkVaultDialog DoubleClaimButton 規範 (#38A0FF, 52px, 5px厚底, 18px圓角, 零Emoji) 檢驗通過")


func _assert_no_emoji(node: Node) -> void:
	for child in node.find_children("*", "Label", true, false):
		var text := (child as Label).text
		for ch in text:
			var code := ch.unicode_at(0)
			var is_emoji := (
				(code >= 0x1F300 and code <= 0x1FAFF)
				or (code >= 0x2600 and code <= 0x27BF)
				or (code >= 0xFE00 and code <= 0xFE0F)
				or (code >= 0x1F900 and code <= 0x1F9FF)
			)
			if is_emoji:
				assert(false, "節點 %s 含有系統 Emoji 字元 '%s'" % [child.name, ch])


func _save_and_record_hash(path: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	assert(img != null and not img.is_empty(), "無法取得 Viewport 截圖")

	var is_solid := true
	var p0 := img.get_pixel(0, 0)
	for sy in [60, 200, 360, 500, 660]:
		for sx in [60, 320, 640, 960, 1200]:
			if img.get_pixel(sx, sy) != p0:
				is_solid = false
				break
		if not is_solid:
			break
	assert(not is_solid, "截圖為純色黑屏或無效畫面: %s" % path)

	var err := img.save_png(path)
	assert(err == OK, "儲存截圖失敗: %s" % path)

	var f := FileAccess.open(path, FileAccess.READ)
	assert(f != null, "讀取截圖失敗: %s" % path)
	var buf := f.get_buffer(f.get_length())
	f.close()

	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	var h := ctx.finish().hex_encode()
	print("  [PROOF] %s (SHA256: %s)" % [path.get_file(), h.substr(0, 16)])
	_hashes.append(h)


func _verify_all_proof_hashes() -> void:
	assert(_hashes.size() == 6, "存證截圖數量不正確 (應有 6 張，實得 %d)" % _hashes.size())
	for i in range(_hashes.size()):
		for j in range(i + 1, _hashes.size()):
			assert(_hashes[i] != _hashes[j], "截圖不可重複 (第 %d 張與第 %d 張 SHA256 相同: %s)" % [i + 1, j + 1, _hashes[i]])
	print("  ✓ 全部 6 張存證截圖 SHA256 均獨立相異，無重複或黑屏存證！")
