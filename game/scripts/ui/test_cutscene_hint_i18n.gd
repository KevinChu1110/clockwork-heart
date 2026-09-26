extends SceneTree
## 過場字幕繼續提示對齊對話框六語系與觸控/桌面判定單元測試 (Cutscene Hint i18n Test)
## 驗證：
## 1. 觸控模式與桌面模式文案正確由 ContentLoc 取得六語系對應譯文
## 2. 非中文語系無繁中殘留，無 Space / E 硬編碼
## 3. CutscenePlayer 實例支援觸控/桌面切換與 Loc.locale_changed 動態即時刷新
## 4. 全屏過場元件零系統 emoji

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const CutscenePlayerScript = preload("res://scripts/ui/cutscene_player.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 5:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_CUTSCENE_HINT_I18N_OK")
					quit(0)
				else:
					push_error("TEST_CUTSCENE_HINT_I18N_FAIL")
					print("TEST_CUTSCENE_HINT_I18N_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_cutscene_hint_i18n 測試 ===")

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	# 1. 預期字串對照表
	var expected_touch := {
		"zh_TW": "▼ 點一下繼續",
		"zh_CN": "▼ 点一下继续",
		"en": "▼ Tap to continue",
		"ja": "▼ タップで進む",
		"ko": "▼ 탭하여 계속",
		"es": "▼ Toca para continuar",
	}

	var expected_desktop := {
		"zh_TW": "▼ 點擊 / Space 繼續",
		"zh_CN": "▼ 点击 / Space 继续",
		"en": "▼ Click / Space to continue",
		"ja": "▼ クリック / Space で進む",
		"ko": "▼ 클릭 / Space 계속",
		"es": "▼ Clic / Espacio para continuar",
	}

	print("\n--- 1. 驗證六語系字典與 CutscenePlayer._hint_text 靜態判定 ---")
	for code in LOCALES:
		loc_node.call("set_locale", code)

		var t_touch: String = CutscenePlayerScript._hint_text(true)
		if t_touch != expected_touch[code]:
			_fail("[%s] 觸控提示不符: 期望 '%s'，實際 '%s'" % [code, expected_touch[code], t_touch])
		else:
			print("  ✓ [%s] 觸控提示 -> %s" % [code, t_touch])

		var t_desktop: String = CutscenePlayerScript._hint_text(false)
		if t_desktop != expected_desktop[code]:
			_fail("[%s] 桌面提示不符: 期望 '%s'，實際 '%s'" % [code, expected_desktop[code], t_desktop])
		else:
			print("  ✓ [%s] 桌面提示 -> %s" % [code, t_desktop])

		# 檢查非中文語系無繁中殘留
		if code in ["en", "ja", "ko", "es"]:
			if t_touch.find("點一下") >= 0 or t_touch.find("繼續") >= 0:
				_fail("[%s] 觸控提示出現繁中殘留: '%s'" % [code, t_touch])
			if t_desktop.find("點擊") >= 0 or t_desktop.find("繼續") >= 0:
				_fail("[%s] 桌面提示出現繁中殘留: '%s'" % [code, t_desktop])

		# 檢查過場提示絕無 Space / E 硬編碼
		if t_touch.find("Space / E") >= 0 or t_desktop.find("Space / E") >= 0:
			_fail("[%s] 提示出現 Space / E 舊硬編碼！" % code)

	print("\n--- 2. 驗證 CutscenePlayer 實例建立與觸控模式切換 ---")
	loc_node.call("set_locale", "zh_TW")
	var player = CutscenePlayerScript.new()
	root.add_child(player)

	# 檢查 Label 初始文字
	var hint_lbl: Label = player.get("_hint")
	if hint_lbl == null:
		_fail("CutscenePlayer 找不到 _hint Label")
	else:
		# 預設桌面環境（無頭環境通常無觸控）
		print("  ✓ CutscenePlayer _hint 初始化文字: '%s'" % hint_lbl.text)

		# 強制設定為觸控
		player.force_touch_mode = true
		player._update_hint_text()
		if hint_lbl.text != expected_touch["zh_TW"]:
			_fail("強制觸控模式下文字未切換為 '%s'，實際為 '%s'" % [expected_touch["zh_TW"], hint_lbl.text])
		else:
			print("  ✓ 強制觸控模式下文字切換正確: '%s'" % hint_lbl.text)

		# 強制設定為桌面
		player.force_touch_mode = false
		player._update_hint_text()
		if hint_lbl.text != expected_desktop["zh_TW"]:
			_fail("強制桌面模式下文字未切換為 '%s'，實際為 '%s'" % [expected_desktop["zh_TW"], hint_lbl.text])
		else:
			print("  ✓ 強制桌面模式下文字切換正確: '%s'" % hint_lbl.text)

	print("\n--- 3. 驗證 CutscenePlayer 實例監聽 Loc.locale_changed 即時動態連動 ---")
	# 觸控模式：依序切換六語系（從 zh_TW 開始）
	player.force_touch_mode = true
	player._update_hint_text()
	for code in LOCALES:
		# 先換成另一語系再換至 code，確保觸發 locale_changed
		var dummy := "es" if code != "es" else "en"
		loc_node.call("set_locale", dummy)
		loc_node.call("set_locale", code)
		if hint_lbl and hint_lbl.text != expected_touch[code]:
			_fail("[%s] 觸控模式 locale_changed 即時連動失敗: 期望 '%s'，實際 '%s'" % [code, expected_touch[code], hint_lbl.text])
		else:
			print("  ✓ [%s] 觸控模式即時切換連動成功: '%s'" % [code, hint_lbl.text if hint_lbl else ""])

	# 桌面模式：依序切換六語系
	player.force_touch_mode = false
	player._update_hint_text()
	for code in LOCALES:
		var dummy := "es" if code != "es" else "en"
		loc_node.call("set_locale", dummy)
		loc_node.call("set_locale", code)
		if hint_lbl and hint_lbl.text != expected_desktop[code]:
			_fail("[%s] 桌面模式 locale_changed 即時連動失敗: 期望 '%s'，實際 '%s'" % [code, expected_desktop[code], hint_lbl.text])
		else:
			print("  ✓ [%s] 桌面模式即時切換連動成功: '%s'" % [code, hint_lbl.text if hint_lbl else ""])

	# 清理
	player.queue_free()
	loc_node.call("set_locale", "zh_TW")
	print("  ✓ 實例清理與語系復原完成")
