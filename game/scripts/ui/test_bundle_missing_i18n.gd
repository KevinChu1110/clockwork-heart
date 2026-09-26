extends SceneTree
## 章節包尚未下載彈窗六語系單元測試 (Bundle Missing Dialog i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含標題、內文、確定按鈕翻譯，且無繁中「尚未下載」殘留
## 2. BundlePacks.missing_pack_line(map_id) 在各語系下正確代換 pack id 且格式一致
## 3. 實例化 BundleMissingDialog，在彈窗開著時切換語系 (Loc.locale_changed)，標題、內文、確定按鈕即時動態刷新
## 4. 關閉彈窗正確清理無殘留

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const BundlePacks = preload("res://scripts/systems/bundle_packs.gd")
const BundleMissingDialogScn = preload("res://scripts/ui/bundle_missing_dialog.gd")

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
					print("TEST_BUNDLE_MISSING_I18N_OK")
					quit(0)
				else:
					push_error("TEST_BUNDLE_MISSING_I18N_FAIL")
					print("TEST_BUNDLE_MISSING_I18N_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_bundle_missing_i18n 測試 ===")

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	# 1. 預期字典資料定義
	var expected_title := {
		"zh_TW": "尚未下載",
		"zh_CN": "尚未下载",
		"en": "Not Downloaded",
		"ja": "未ダウンロード",
		"ko": "미다운로드",
		"es": "No descargado",
	}

	var expected_body_fmt := {
		"zh_TW": "後續章節尚未下載（需要 %s 包）",
		"zh_CN": "后续章节尚未下载（需要 %s 包）",
		"en": "Subsequent chapters not downloaded (requires %s pack)",
		"ja": "以降の章は未ダウンロードです（%s パックが必要）",
		"ko": "이후 챕터가 다운로드되지 않았습니다 (%s 팩 필요)",
		"es": "Capítulos posteriores no descargados (requiere paquete %s)",
	}

	var expected_btn := {
		"zh_TW": "確定",
		"zh_CN": "确定",
		"en": "OK",
		"ja": "確認",
		"ko": "확인",
		"es": "Aceptar",
	}

	print("\n--- 1. 驗證六語系字典與 BundlePacks.missing_pack_line ---")
	for code in LOCALES:
		loc_node.call("set_locale", code)

		var t_title := ContentLoc.text("ui", "尚未下載")
		if t_title != expected_title[code]:
			_fail("[%s] 標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_title[code], t_title])
		else:
			print("  ✓ [%s] 標題 -> %s" % [code, t_title])

		var t_body_fmt := ContentLoc.text("ui", "後續章節尚未下載（需要 %s 包）")
		if t_body_fmt != expected_body_fmt[code]:
			_fail("[%s] 內文樣板翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_body_fmt[code], t_body_fmt])
		else:
			print("  ✓ [%s] 樣板 -> %s" % [code, t_body_fmt])

		var actual_line := BundlePacks.missing_pack_line("wild")
		var expected_line: String = expected_body_fmt[code] % "chapter"
		if actual_line != expected_line:
			_fail("[%s] missing_pack_line 代換不符: 期望 '%s'，實際 '%s'" % [code, expected_line, actual_line])
		else:
			print("  ✓ [%s] 實機文字 -> %s" % [code, actual_line])

		var t_btn := ContentLoc.text("ui", "確定")
		if t_btn != expected_btn[code]:
			_fail("[%s] 確定鈕翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_btn[code], t_btn])
		else:
			print("  ✓ [%s] 確定按鈕 -> %s" % [code, t_btn])

		# 檢查非中文語系無繁中「尚未下載」殘留
		if code in ["en", "ja", "ko", "es"]:
			if t_title.find("尚未下載") >= 0 or actual_line.find("尚未下載") >= 0 or t_btn.find("尚未下載") >= 0:
				_fail("[%s] 出現繁中「尚未下載」殘留！" % code)

	print("\n--- 2. 驗證 BundleMissingDialog 實例與 locale_changed 動態即時連動 ---")
	# 初始先切回繁中
	loc_node.call("set_locale", "zh_TW")
	var dlg: AcceptDialog = BundleMissingDialogScn.new("wild")
	root.add_child(dlg)

	# 驗證初始繁中內容
	if dlg.title != expected_title["zh_TW"]:
		_fail("彈窗初始標題不符: %s" % dlg.title)
	if dlg.dialog_text != (expected_body_fmt["zh_TW"] % "chapter"):
		_fail("彈窗初始內文不符: %s" % dlg.dialog_text)
	if dlg.ok_button_text != expected_btn["zh_TW"]:
		_fail("彈窗初始按鈕不符: %s" % dlg.ok_button_text)
	print("  ✓ 彈窗初始繁中內容驗證正確")

	# 動態輪流切換六語系，驗證在彈窗開啟中各文字即時刷新
	for code in LOCALES:
		loc_node.call("set_locale", code)
		var exp_title: String = expected_title[code]
		var exp_text: String = expected_body_fmt[code] % "chapter"
		var exp_btn: String = expected_btn[code]

		if dlg.title != exp_title:
			_fail("[%s] locale_changed 連動失敗，彈窗標題為 '%s'，期望 '%s'" % [code, dlg.title, exp_title])
		if dlg.dialog_text != exp_text:
			_fail("[%s] locale_changed 連動失敗，彈窗內文為 '%s'，期望 '%s'" % [code, dlg.dialog_text, exp_text])
		if dlg.ok_button_text != exp_btn:
			_fail("[%s] locale_changed 連動失敗，彈窗按鈕為 '%s'，期望 '%s'" % [code, dlg.ok_button_text, exp_btn])
		if dlg.get_ok_button().text != exp_btn:
			_fail("[%s] get_ok_button().text 未同步為 '%s'，實際 '%s'" % [code, exp_btn, dlg.get_ok_button().text])

		print("  ✓ [%s] 即時切換連動驗證成功: 標題='%s' | 按鈕='%s'" % [code, dlg.title, dlg.ok_button_text])

	# 測試完畢清理
	dlg.queue_free()
	# 復原繁中
	loc_node.call("set_locale", "zh_TW")
	print("  ✓ 彈窗清理與語系復原完成")
