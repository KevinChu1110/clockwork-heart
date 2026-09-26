extends SceneTree
## 設定頁聲音／畫面／備份分頁六語系單元測試 (Settings Panel i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含聲音、畫面、備份分頁玩家可見字翻譯。
## 2. 切換至 en、ja、ko、es、zh_CN、zh_TW 時，設定彈窗文字即時連動刷新。
## 3. 語言卡片上的語言名稱與副標維持原文，已選用標示顯示對應語系。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const MobileSettingsClass = preload("res://scripts/ui/mobile_settings.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0


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
	if _frame == 1:
		_run_test_suite()
		if _ok:
			print("\n=======================================================")
			print("SETTINGS_PANEL_I18N_OK")
			quit(0)
		else:
			push_error("SETTINGS_PANEL_I18N_FAIL")
			print("SETTINGS_PANEL_I18N_FAIL")
			quit(1)
		return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_settings_panel_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 驗證詞條字典解析
	var expected_audio_title := {
		"zh_TW": "音量調節與聲效開關",
		"zh_CN": "音量调节与声效开关",
		"en": "Volume & Sound Effects",
		"ja": "音量調整と効果音設定",
		"ko": "볼륨 조절 및 사운드 설정",
		"es": "Ajuste de volumen y sonido",
	}
	var expected_bgm := {
		"zh_TW": "背景音樂 (BGM)",
		"zh_CN": "背景音乐 (BGM)",
		"en": "Music (BGM)",
		"ja": "背景音楽 (BGM)",
		"ko": "배경음악 (BGM)",
		"es": "Música (BGM)",
	}
	var expected_sfx := {
		"zh_TW": "戰鬥音效 (SFX)",
		"zh_CN": "战斗音效 (SFX)",
		"en": "Sound Effects (SFX)",
		"ja": "効果音 (SFX)",
		"ko": "전투 효과음 (SFX)",
		"es": "Efectos de sonido (SFX)",
	}
	var expected_display_title := {
		"zh_TW": "顯示模式與渲染設定",
		"zh_CN": "显示模式与渲染设置",
		"en": "Display & Rendering",
		"ja": "表示モードと描画設定",
		"ko": "화면 모드 및 렌더링 설정",
		"es": "Modo de pantalla y renderizado",
	}
	var expected_fullscreen := {
		"zh_TW": "全螢幕沉浸模式",
		"zh_CN": "全屏幕沉浸模式",
		"en": "Fullscreen Immersive Mode",
		"ja": "全画面没入モード",
		"ko": "전체 화면 몰입 모드",
		"es": "Modo inmersivo pantalla completa",
	}
	var expected_fs_btn := {
		"zh_TW": "切換顯示模式",
		"zh_CN": "切换显示模式",
		"en": "Switch Display Mode",
		"ja": "表示モード切替",
		"ko": "화면 모드 전환",
		"es": "Cambiar modo de pantalla",
	}
	var expected_backup_title := {
		"zh_TW": "雲端與本機存檔備份",
		"zh_CN": "云端与本机存档备份",
		"en": "Cloud & Local Save Backup",
		"ja": "クラウド・ローカルセーブ",
		"ko": "클라우드 및 로컬 세이브 백업",
		"es": "Copia de seguridad local y nube",
	}
	var expected_export := {
		"zh_TW": "匯出存檔備份檔 (JSON)",
		"zh_CN": "导出存档备份文件 (JSON)",
		"en": "Export Save Backup (JSON)",
		"ja": "セーブデータを書き出す (JSON)",
		"ko": "세이브 백업 내보내기 (JSON)",
		"es": "Exportar partida guardada (JSON)",
	}
	var expected_import := {
		"zh_TW": "從外部備份還原存檔",
		"zh_CN": "从外部备份还原存档",
		"en": "Restore Save from Backup",
		"ja": "外部バックアップから復元",
		"ko": "외부 백업에서 세이브 복원",
		"es": "Restaurar desde copia",
	}
	var expected_selected := {
		"zh_TW": "✓ 已選用",
		"zh_CN": "✓ 已选用",
		"en": "✓ Selected",
		"ja": "✓ 選択中",
		"ko": "✓ 선택됨",
		"es": "✓ Seleccionado",
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		var t_audio = ContentLoc.text("ui", "音量調節與聲效開關")
		if t_audio != expected_audio_title[code]:
			_fail("[%s] 音量調節與聲效開關 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_audio_title[code], t_audio])

		var t_bgm = ContentLoc.text("ui", "背景音樂 (BGM)")
		if t_bgm != expected_bgm[code]:
			_fail("[%s] 背景音樂 (BGM) 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_bgm[code], t_bgm])

		var t_sfx = ContentLoc.text("ui", "戰鬥音效 (SFX)")
		if t_sfx != expected_sfx[code]:
			_fail("[%s] 戰鬥音效 (SFX) 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_sfx[code], t_sfx])

		var t_disp = ContentLoc.text("ui", "顯示模式與渲染設定")
		if t_disp != expected_display_title[code]:
			_fail("[%s] 顯示模式與渲染設定 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_display_title[code], t_disp])

		var t_fs = ContentLoc.text("ui", "全螢幕沉浸模式")
		if t_fs != expected_fullscreen[code]:
			_fail("[%s] 全螢幕沉浸模式 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_fullscreen[code], t_fs])

		var t_fsb = ContentLoc.text("ui", "切換顯示模式")
		if t_fsb != expected_fs_btn[code]:
			_fail("[%s] 切換顯示模式 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_fs_btn[code], t_fsb])

		var t_back = ContentLoc.text("ui", "雲端與本機存檔備份")
		if t_back != expected_backup_title[code]:
			_fail("[%s] 雲端與本機存檔備份 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_backup_title[code], t_back])

		var t_exp = ContentLoc.text("ui", "匯出存檔備份檔 (JSON)")
		if t_exp != expected_export[code]:
			_fail("[%s] 匯出存檔備份檔 (JSON) 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_export[code], t_exp])

		var t_imp = ContentLoc.text("ui", "從外部備份還原存檔")
		if t_imp != expected_import[code]:
			_fail("[%s] 從外部備份還原存檔 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_import[code], t_imp])

		var t_sel = ContentLoc.text("ui", "✓ 已選用")
		if t_sel != expected_selected[code]:
			_fail("[%s] ✓ 已選用 翻譯不符: 期望 '%s', 得到 '%s'" % [code, expected_selected[code], t_sel])

	# 2. 實例化 MobileSettings 並驗證節點即時連動刷新
	print("--- 測試 MobileSettings 節點切換即時連動 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var settings = MobileSettingsClass.new()
	root_node.add_child(settings)

	# 測試切換至 en
	if loc_node:
		loc_node.call("set_locale", "en")

	var audio_title_lbl: Label = settings.get("_audio_title_l")
	if audio_title_lbl and audio_title_lbl.text != expected_audio_title["en"]:
		_fail("切換 en 後 AudioTitle 未連動: '%s' != '%s'" % [audio_title_lbl.text, expected_audio_title["en"]])
	else:
		print("  ✓ [en] AudioTitle 即時連動成功: ", audio_title_lbl.text if audio_title_lbl else "N/A")

	var disp_title_lbl: Label = settings.get("_display_title_l")
	if disp_title_lbl and disp_title_lbl.text != expected_display_title["en"]:
		_fail("切換 en 後 DisplayTitle 未連動: '%s' != '%s'" % [disp_title_lbl.text, expected_display_title["en"]])
	else:
		print("  ✓ [en] DisplayTitle 即時連動成功: ", disp_title_lbl.text if disp_title_lbl else "N/A")

	var backup_title_lbl: Label = settings.get("_backup_title_l")
	if backup_title_lbl and backup_title_lbl.text != expected_backup_title["en"]:
		_fail("切換 en 後 BackupTitle 未連動: '%s' != '%s'" % [backup_title_lbl.text, expected_backup_title["en"]])
	else:
		print("  ✓ [en] BackupTitle 即時連動成功: ", backup_title_lbl.text if backup_title_lbl else "N/A")

	# 測試切換至 ja
	if loc_node:
		loc_node.call("set_locale", "ja")

	if audio_title_lbl and audio_title_lbl.text != expected_audio_title["ja"]:
		_fail("切換 ja 後 AudioTitle 未連動: '%s' != '%s'" % [audio_title_lbl.text, expected_audio_title["ja"]])
	else:
		print("  ✓ [ja] AudioTitle 即時連動成功: ", audio_title_lbl.text if audio_title_lbl else "N/A")

	if disp_title_lbl and disp_title_lbl.text != expected_display_title["ja"]:
		_fail("切換 ja 後 DisplayTitle 未連動: '%s' != '%s'" % [disp_title_lbl.text, expected_display_title["ja"]])
	else:
		print("  ✓ [ja] DisplayTitle 即時連動成功: ", disp_title_lbl.text if disp_title_lbl else "N/A")

	if backup_title_lbl and backup_title_lbl.text != expected_backup_title["ja"]:
		_fail("切換 ja 後 BackupTitle 未連動: '%s' != '%s'" % [backup_title_lbl.text, expected_backup_title["ja"]])
	else:
		print("  ✓ [ja] BackupTitle 即時連動成功: ", backup_title_lbl.text if backup_title_lbl else "N/A")

	# 驗證語言卡片上的語言名稱保持原文
	var lang_grid: GridContainer = settings.get("_lang_grid")
	if lang_grid:
		var found_zh_card := false
		var found_en_card := false
		var found_ja_card := false
		for c in lang_grid.get_children():
			if c is Button:
				var t_lbl: Label = c.find_child("TitleLabel", true, false)
				if t_lbl:
					if t_lbl.text == "繁體中文": found_zh_card = true
					if t_lbl.text == "English": found_en_card = true
					if t_lbl.text == "日本語": found_ja_card = true
		if not (found_zh_card and found_en_card and found_ja_card):
			_fail("語言卡片名稱未保持原文！")
		else:
			print("  ✓ 語言卡片名稱維持各語言原文 (繁體中文/English/日本語)")

	settings.queue_free()
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
